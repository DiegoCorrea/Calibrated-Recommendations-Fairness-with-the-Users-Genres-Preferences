from copy import deepcopy
from multiprocessing import Process, Queue, Semaphore

import pandas as pd
from surprise import KNNWithMeans, SVD, SVDpp, NMF
from surprise.prediction_algorithms.slope_one import SlopeOne

from src.config import user_label, NMF_LABEL, \
    SVDpp_LABEL, SVD_LABEL, SLOPE_LABEL, FAIRNESS_METRIC_LABEL, LAMBDA_LABEL, EVALUATION_METRIC_LABEL, \
    EVALUATION_VALUE_LABEL, evaluation_label, ITEMKNN_LABEL, USERKNN_LABEL, item_label, value_label, \
    CANDIDATES_LIST_SIZE, N_CORES, LAMBDA_VALUE_LABEL, TIME_LIMIT
from src.conversions.pandas_to_models import transform_testset, user_transactions_df_to_item_mapping
from src.conversions.suprise_and_pandas import surprise_to_pandas_get_candidates_items
from src.language_strings import LANGUAGE_RECOMMENDER_ALGORITHMS_STOP, \
    LANGUAGE_RECOMMENDER_ALGORITHMS_START, LANGUAGE_USER_KNN_START, LANGUAGE_ITEM_KNN_START, \
    LANGUAGE_SVD_START, LANGUAGE_SVD_STOP, LANGUAGE_SVDPP_START, LANGUAGE_SVDPP_STOP, \
    LANGUAGE_NMF_START, LANGUAGE_NMF_STOP, LANGUAGE_SLOPE_ONE_START, LANGUAGE_SLOPE_ONE_STOP, LANGUAGE_ITEM_KNN_STOP, \
    LANGUAGE_USER_KNN_STOP
from src.posprocessing.distributions import get_distribution
from src.posprocessing.step import postprocessing_calibration


def print_results(evaluation_results_df):
    for evaluation_metric in evaluation_results_df[EVALUATION_METRIC_LABEL].unique().tolist():
        evaluation_subset_df = evaluation_results_df[
            evaluation_results_df[EVALUATION_METRIC_LABEL] == evaluation_metric]
        print(evaluation_subset_df.sort_values(by=[EVALUATION_VALUE_LABEL]))


def get_unknown_items(user_id, user_trainset_df, item_mapping):
    items_ids = item_mapping.keys()
    know_items_ids = user_trainset_df[item_label].unique().tolist()
    data = {item_label: list(set(items_ids) - set(know_items_ids))}
    user_testset_df = pd.DataFrame(data)
    user_testset_df[user_label] = user_id
    user_testset_df[value_label] = 0.0
    return user_testset_df


def recommender_prediction(instance, user_unknown_items_df):
    # Aplicar Lock
    candidates_items = instance.test(transform_testset(user_unknown_items_df))
    # Desfazer Lock
    return surprise_to_pandas_get_candidates_items(candidates_items, n=CANDIDATES_LIST_SIZE)


def recommendation_and_posprocessing(user_id, user_trainset_df, user_prefs_distr_df, user_testset_df, item_mapping,
                                     instance, baseline_label):
    keys_list = item_mapping.keys()
    know_items = user_trainset_df[item_label].unique().tolist()
    unknow_items = set(keys_list) - set(know_items)
    data = {item_label: list(unknow_items)}
    user_testset = pd.DataFrame.from_dict(data)
    user_testset[user_label] = user_id
    user_testset[value_label] = 0.0
    # candidates_items_prediction = [instance.predict(user_id, item_id) for item_id in list(unknow_items)]
    candidates_items_prediction = instance.test(transform_testset(user_testset))
    user_candidates_items_df = surprise_to_pandas_get_candidates_items(candidates_items_prediction)
    user_candidates_items_df.sort_values(by=[value_label], ascending=False, inplace=True)
    candidates_items_mapping = user_transactions_df_to_item_mapping(user_candidates_items_df, item_mapping)
    result_df = postprocessing_calibration(user_prefs_distr_df=user_prefs_distr_df,
                                           candidates_items_mapping=candidates_items_mapping,
                                           test_items_ids=user_testset_df[item_label].tolist(),
                                           baseline_label=baseline_label)
    return result_df


def users_results_mean(evaluation_results_df, baseline_label):
    recommender_results_df = pd.DataFrame()
    for distance_metric in evaluation_results_df[FAIRNESS_METRIC_LABEL].unique().tolist():
        fairness_subset_df = evaluation_results_df[evaluation_results_df[FAIRNESS_METRIC_LABEL] == distance_metric]
        for lambda_type in fairness_subset_df[LAMBDA_LABEL].unique().tolist():
            lambda_subset_df = fairness_subset_df[fairness_subset_df[LAMBDA_LABEL] == lambda_type]
            for lambda_value in lambda_subset_df[LAMBDA_VALUE_LABEL].unique().tolist():
                lambda_value_subset_df = lambda_subset_df[lambda_subset_df[LAMBDA_VALUE_LABEL] == lambda_value]
                for evaluation_metric in lambda_value_subset_df[EVALUATION_METRIC_LABEL].unique().tolist():
                    evaluation_subset_df = lambda_value_subset_df[
                        lambda_value_subset_df[EVALUATION_METRIC_LABEL] == evaluation_metric]
                    value = evaluation_subset_df[EVALUATION_VALUE_LABEL].mean()
                    recommender_results_df = pd.concat([recommender_results_df,
                                                        pd.DataFrame(
                                                            [[baseline_label,
                                                              distance_metric,
                                                              lambda_type,
                                                              lambda_value,
                                                              evaluation_metric,
                                                              value]],
                                                            columns=evaluation_label
                                                        )
                                                        ])
    return recommender_results_df


# ####################################################################################################


def user_knn_recommender(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping):
    # Recommender Prediction
    print(LANGUAGE_USER_KNN_START)
    instance = KNNWithMeans(k=30, sim_options={'name': 'pearson_baseline', 'user_based': True})
    instance.fit(trainset)
    print(LANGUAGE_USER_KNN_START)

    users_prefs_distr_df.sort_index(inplace=True)
    users_prefs_distr_df = users_prefs_distr_df.sample(n=3, random_state=1)
    evaluation_results_df = [
        recommendation_and_posprocessing(user_id, trainset_df[trainset_df[user_label] == user_id], user_prefs_distr_df,
                                         testset_df[testset_df[user_label] == user_id], item_mapping, instance,
                                         USERKNN_LABEL)
        for user_id, user_prefs_distr_df in users_prefs_distr_df.iterrows()]
    evaluation_results_df = pd.concat(evaluation_results_df)
    recommender_results_df = users_results_mean(evaluation_results_df, USERKNN_LABEL)
    return recommender_results_df


def item_knn_recommender(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping):
    # Recommender Prediction
    print(LANGUAGE_ITEM_KNN_START)
    instance = KNNWithMeans(k=30, sim_options={'name': 'pearson_baseline', 'user_based': False})
    instance.fit(trainset)
    print(LANGUAGE_ITEM_KNN_START)

    users_prefs_distr_df.sort_index(inplace=True)
    users_prefs_distr_df = users_prefs_distr_df.sample(n=3, random_state=1)
    evaluation_results_df = [
        recommendation_and_posprocessing(user_id, trainset_df[trainset_df[user_label] == user_id], user_prefs_distr_df,
                                         testset_df[testset_df[user_label] == user_id], item_mapping, instance,
                                         ITEMKNN_LABEL)
        for user_id, user_prefs_distr_df in users_prefs_distr_df.iterrows()]
    evaluation_results_df = pd.concat(evaluation_results_df)
    recommender_results_df = users_results_mean(evaluation_results_df, ITEMKNN_LABEL)
    return recommender_results_df


def svd_recommender(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping):
    # Recommender Prediction
    print(LANGUAGE_SVD_START)
    instance = SVD(random_state=42)
    instance.fit(trainset)
    print(LANGUAGE_SVD_STOP)

    users_prefs_distr_df.sort_index(inplace=True)
    users_prefs_distr_df = users_prefs_distr_df.sample(n=100, random_state=1)

    evaluation_results_df = [
        recommendation_and_posprocessing(user_id, trainset_df[trainset_df[user_label] == user_id], user_prefs_distr_df,
                                         testset_df[testset_df[user_label] == user_id], item_mapping, instance,
                                         SVD_LABEL)
        for user_id, user_prefs_distr_df in users_prefs_distr_df.iterrows()]
    evaluation_results_df = pd.concat(evaluation_results_df)
    recommender_results_df = users_results_mean(evaluation_results_df, SVD_LABEL)
    # print_results(recommender_results_df)
    return recommender_results_df


def svdpp_recommender(trainset, users_prefs_distr_df, testset_df, item_mapping):
    # Recommender Prediction
    print(LANGUAGE_SVDPP_START)
    instance = SVDpp()
    instance.fit(trainset)
    print(LANGUAGE_SVDPP_STOP)

    users_prefs_distr_df = users_prefs_distr_df[:20]
    evaluation_results_df = [
        recommendation_and_posprocessing(user_id, user_prefs_distr_df, SVDpp_LABEL, testset_df, instance, item_mapping)
        for user_id, user_prefs_distr_df in users_prefs_distr_df.iterrows()]
    evaluation_results_df = pd.concat(evaluation_results_df)
    recommender_results_df = users_results_mean(evaluation_results_df, SVDpp_LABEL)
    print(recommender_results_df)
    return recommender_results_df


def nmf_recommender(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping):
    # Recommender Prediction
    print(LANGUAGE_NMF_START)
    instance = NMF(random_state=42)
    instance.fit(trainset)
    print(LANGUAGE_NMF_STOP)

    users_prefs_distr_df.sort_index(inplace=True)
    users_prefs_distr_df = users_prefs_distr_df.sample(n=100, random_state=1)

    evaluation_results_df = [
        recommendation_and_posprocessing(user_id, trainset_df[trainset_df[user_label] == user_id], user_prefs_distr_df,
                                         testset_df[testset_df[user_label] == user_id], item_mapping, instance,
                                         NMF_LABEL)
        for user_id, user_prefs_distr_df in users_prefs_distr_df.iterrows()]
    evaluation_results_df = pd.concat(evaluation_results_df)
    recommender_results_df = users_results_mean(evaluation_results_df, NMF_LABEL)
    # print_results(recommender_results_df)
    return recommender_results_df


def slope_one_recommender(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping):
    # Recommender Prediction
    print(LANGUAGE_SLOPE_ONE_START)
    instance = SlopeOne()
    instance.fit(trainset)
    print(LANGUAGE_SLOPE_ONE_STOP)

    users_prefs_distr_df = users_prefs_distr_df[:20]
    evaluation_results_df = [
        recommendation_and_posprocessing(user_id, user_prefs_distr_df, SLOPE_LABEL,
                                         trainset_df[trainset_df[user_label] == user_id], testset_df, instance,
                                         item_mapping)
        for user_id, user_prefs_distr_df in users_prefs_distr_df.iterrows()]
    evaluation_results_df = pd.concat(evaluation_results_df)
    recommender_results_df = users_results_mean(evaluation_results_df, SLOPE_LABEL)
    print(recommender_results_df)
    return recommender_results_df


# #################################################################################################################### #
# #################################################################################################################### #
# #################################################################################################################### #


def rec(user_id, user_trainset_df, user_prefs_distr_df, user_testset_df, item_mapping, instance, baseline_label, q,
        sem):
    user_unknown_items_df = get_unknown_items(user_id, user_trainset_df, item_mapping)

    user_candidates_items_df = recommender_prediction(instance, user_unknown_items_df)

    candidates_items_mapping = user_transactions_df_to_item_mapping(user_candidates_items_df, item_mapping)
    user_evaluation_results_df = postprocessing_calibration(user_prefs_distr_df=user_prefs_distr_df,
                                                            candidates_items_mapping=candidates_items_mapping,
                                                            test_items_ids=user_testset_df[item_label].tolist(),
                                                            baseline_label=baseline_label)
    sem.acquire()
    q.put(deepcopy(user_evaluation_results_df))
    sem.release()


def user_knn_recommender_multiprocess(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping):
    # Algorithm Prediction
    print(LANGUAGE_USER_KNN_START)
    instance = KNNWithMeans(k=30, sim_options={'name': 'pearson_baseline', 'user_based': True})
    instance.fit(trainset)
    print(LANGUAGE_USER_KNN_STOP)

    users_ids = users_prefs_distr_df.index.values.tolist()
    evaluation_results_df = pd.DataFrame()
    q = Queue()
    sem = Semaphore(TIME_LIMIT)
    while users_ids:
        process_control = list(range(0, N_CORES))
        all_processes = []
        while users_ids and process_control:
            process_control.pop(0)
            user_id = users_ids.pop(0)
            user_trainset_df = trainset_df[trainset_df[user_label] == user_id]
            user_testset_df = testset_df[testset_df[user_label] == user_id]
            user_prefs_distr_df = users_prefs_distr_df.loc[user_id]
            p = Process(target=rec,
                        args=(user_id, user_trainset_df, user_prefs_distr_df, user_testset_df, item_mapping, instance,
                              USERKNN_LABEL, q, sem,))
            all_processes.append(p)
            p.start()
        for p in all_processes:
            p.join(TIME_LIMIT)
            p.close()
        user_evaluation_results = []
        while not q.empty():
            sem.acquire()
            user_evaluation_results.append(q.get(timeout=TIME_LIMIT))
            sem.release()
        user_evaluation_results = pd.concat(user_evaluation_results)
        evaluation_results_df = pd.concat([evaluation_results_df, user_evaluation_results])
    recommender_results_df = users_results_mean(evaluation_results_df, USERKNN_LABEL)
    return recommender_results_df


def item_knn_recommender_multiprocess(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping):
    # Algorithm Prediction
    print(LANGUAGE_ITEM_KNN_START)
    instance = KNNWithMeans(k=30, sim_options={'name': 'pearson_baseline', 'user_based': False})
    instance.fit(trainset)
    print(LANGUAGE_ITEM_KNN_STOP)

    users_ids = users_prefs_distr_df.index.values.tolist()
    evaluation_results_df = pd.DataFrame()
    q = Queue()
    sem = Semaphore(TIME_LIMIT)
    while users_ids:
        process_control = list(range(0, N_CORES))
        all_processes = []
        while users_ids and process_control:
            process_control.pop(0)
            user_id = users_ids.pop(0)
            user_trainset_df = trainset_df[trainset_df[user_label] == user_id]
            user_testset_df = testset_df[testset_df[user_label] == user_id]
            user_prefs_distr_df = users_prefs_distr_df.loc[user_id]
            p = Process(target=rec,
                        args=(user_id, user_trainset_df, user_prefs_distr_df, user_testset_df, item_mapping, instance,
                              ITEMKNN_LABEL, q, sem,))
            all_processes.append(p)
            p.start()
        for p in all_processes:
            p.join(TIME_LIMIT)
            p.close()
        user_evaluation_results = []
        while not q.empty():
            sem.acquire()
            user_evaluation_results.append(q.get(timeout=TIME_LIMIT))
            sem.release()
        user_evaluation_results = pd.concat(user_evaluation_results)
        evaluation_results_df = pd.concat([evaluation_results_df, user_evaluation_results])
    recommender_results_df = users_results_mean(evaluation_results_df, ITEMKNN_LABEL)
    return recommender_results_df


def svd_recommender_multiprocess(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping):
    # Algorithm Prediction
    print(LANGUAGE_SVD_START)
    instance = SVD()
    instance.fit(trainset)
    print(LANGUAGE_SVD_STOP)

    users_ids = users_prefs_distr_df.index.values.tolist()
    evaluation_results_df = pd.DataFrame()
    q = Queue()
    sem = Semaphore(TIME_LIMIT)
    while users_ids:
        process_control = list(range(0, N_CORES))
        all_processes = []
        while users_ids and process_control:
            process_control.pop(0)
            user_id = users_ids.pop(0)
            user_trainset_df = trainset_df[trainset_df[user_label] == user_id]
            user_testset_df = testset_df[testset_df[user_label] == user_id]
            user_prefs_distr_df = users_prefs_distr_df.loc[user_id]
            p = Process(target=rec,
                        args=(user_id, user_trainset_df, user_prefs_distr_df, user_testset_df, item_mapping, instance,
                              SVD_LABEL, q, sem,))
            all_processes.append(p)
            p.start()
        for p in all_processes:
            p.join(TIME_LIMIT)
            p.close()
        user_evaluation_results = []
        while not q.empty():
            sem.acquire()
            user_evaluation_results.append(q.get(timeout=TIME_LIMIT))
            sem.release()
        user_evaluation_results = pd.concat(user_evaluation_results)
        evaluation_results_df = pd.concat([evaluation_results_df, user_evaluation_results])
    recommender_results_df = users_results_mean(evaluation_results_df, SVD_LABEL)
    return recommender_results_df


def svdpp_recommender_multiprocess(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping):
    # Algorithm Prediction
    print(LANGUAGE_SVDPP_START)
    instance = SVDpp()
    instance.fit(trainset)
    print(LANGUAGE_SVDPP_STOP)

    users_ids = users_prefs_distr_df.index.values.tolist()
    evaluation_results_df = pd.DataFrame()
    q = Queue()
    sem = Semaphore(TIME_LIMIT)
    while users_ids:
        process_control = list(range(0, N_CORES))
        all_processes = []
        while users_ids and process_control:
            process_control.pop(0)
            user_id = users_ids.pop(0)
            user_trainset_df = trainset_df[trainset_df[user_label] == user_id]
            user_testset_df = testset_df[testset_df[user_label] == user_id]
            user_prefs_distr_df = users_prefs_distr_df.loc[user_id]
            p = Process(target=rec,
                        args=(user_id, user_trainset_df, user_prefs_distr_df, user_testset_df, item_mapping, instance,
                              SVDpp_LABEL, q, sem,))
            all_processes.append(p)
            p.start()
        for p in all_processes:
            p.join(TIME_LIMIT)
            p.close()
        user_evaluation_results = []
        while not q.empty():
            sem.acquire()
            user_evaluation_results.append(q.get(timeout=TIME_LIMIT))
            sem.release()
        user_evaluation_results = pd.concat(user_evaluation_results)
        evaluation_results_df = pd.concat([evaluation_results_df, user_evaluation_results])
    recommender_results_df = users_results_mean(evaluation_results_df, SVDpp_LABEL)
    return recommender_results_df


def nmf_recommender_multiprocess(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping):
    # Algorithm Prediction
    print(LANGUAGE_NMF_START)
    instance = NMF()
    instance.fit(trainset)
    print(LANGUAGE_NMF_STOP)

    users_ids = users_prefs_distr_df.index.values.tolist()
    evaluation_results_df = pd.DataFrame()
    q = Queue()
    sem = Semaphore(TIME_LIMIT)
    while users_ids:
        process_control = list(range(0, N_CORES))
        all_processes = []
        while users_ids and process_control:
            process_control.pop(0)
            user_id = users_ids.pop(0)
            user_trainset_df = trainset_df[trainset_df[user_label] == user_id]
            user_testset_df = testset_df[testset_df[user_label] == user_id]
            user_prefs_distr_df = users_prefs_distr_df.loc[user_id]
            p = Process(target=rec,
                        args=(user_id, user_trainset_df, user_prefs_distr_df, user_testset_df, item_mapping, instance,
                              NMF_LABEL, q, sem,))
            all_processes.append(p)
            p.start()
        for p in all_processes:
            p.join(TIME_LIMIT)
            p.close()
        user_evaluation_results = []
        while not q.empty():
            sem.acquire()
            user_evaluation_results.append(q.get(timeout=TIME_LIMIT))
            sem.release()
        user_evaluation_results = pd.concat(user_evaluation_results)
        evaluation_results_df = pd.concat([evaluation_results_df, user_evaluation_results])
    recommender_results_df = users_results_mean(evaluation_results_df, NMF_LABEL)
    return recommender_results_df


def slope_one_recommender_multiprocess(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping):
    # Algorithm Prediction
    print(LANGUAGE_SLOPE_ONE_START)
    instance = SlopeOne()
    instance.fit(trainset)
    print(LANGUAGE_SLOPE_ONE_STOP)

    users_ids = users_prefs_distr_df.index.values.tolist()
    evaluation_results_df = pd.DataFrame()
    q = Queue()
    sem = Semaphore(TIME_LIMIT)
    while users_ids:
        process_control = list(range(0, N_CORES))
        all_processes = []
        while users_ids and process_control:
            process_control.pop(0)
            user_id = users_ids.pop(0)
            user_trainset_df = trainset_df[trainset_df[user_label] == user_id]
            user_testset_df = testset_df[testset_df[user_label] == user_id]
            user_prefs_distr_df = users_prefs_distr_df.loc[user_id]
            p = Process(target=rec,
                        args=(user_id, user_trainset_df, user_prefs_distr_df, user_testset_df, item_mapping, instance,
                              SLOPE_LABEL, q, sem,))
            all_processes.append(p)
            p.start()
        for p in all_processes:
            p.join(TIME_LIMIT)
            p.close()
        user_evaluation_results = []
        while not q.empty():
            sem.acquire()
            user_evaluation_results.append(q.get(timeout=TIME_LIMIT))
            sem.release()
        user_evaluation_results = pd.concat(user_evaluation_results)
        evaluation_results_df = pd.concat([evaluation_results_df, user_evaluation_results])
    recommender_results_df = users_results_mean(evaluation_results_df, SLOPE_LABEL)
    return recommender_results_df


# #################################################################################################################### #
# #################################################################################################################### #
# #################################################################################################################### #


def colaborative_filtering(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping):
    evaluation_results_df = pd.DataFrame()

    # # # Item KNN
    # recommender_results_df = item_knn_recommender(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping)
    # evaluation_results_df = pd.concat([evaluation_results_df, recommender_results_df], sort=False)
    #
    # # # User KNN
    # recommender_results_df = user_knn_recommender(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping)
    # evaluation_results_df = pd.concat([evaluation_results_df, recommender_results_df], sort=False)

    # # SVD
    recommender_results_df = svd_recommender_multiprocess(trainset, users_prefs_distr_df, trainset_df, testset_df,
                                                          item_mapping)
    evaluation_results_df = pd.concat([evaluation_results_df, recommender_results_df], sort=False)

    # # # SVDpp
    # recommender_results_df = svdpp_recommender_multiprocess(trainset, users_prefs_distr_df, trainset_df, testset_df,
    #                                                         item_mapping)
    # evaluation_results_df = pd.concat([evaluation_results_df, recommender_results_df], sort=False)

    # # NMF
    recommender_results_df = nmf_recommender_multiprocess(trainset, users_prefs_distr_df, trainset_df, testset_df,
                                                          item_mapping)
    evaluation_results_df = pd.concat([evaluation_results_df, recommender_results_df], sort=False)

    # # # Sloope One
    # recommender_results_df = slope_one_recommender_multiprocess(trainset, users_prefs_distr_df, trainset_df, testset_df,
    #                                                             item_mapping)
    # evaluation_results_df = pd.concat([evaluation_results_df, recommender_results_df], sort=False)

    return evaluation_results_df


def recommender_algorithms(trainset, trainset_df, testset_df, item_mapping):
    users_prefs_distr_df = get_distribution(trainset_df, item_mapping)
    print(LANGUAGE_RECOMMENDER_ALGORITHMS_START)
    evaluation_results_df = colaborative_filtering(trainset, users_prefs_distr_df, trainset_df, testset_df,
                                                   item_mapping)
    print(LANGUAGE_RECOMMENDER_ALGORITHMS_STOP)
    return evaluation_results_df
