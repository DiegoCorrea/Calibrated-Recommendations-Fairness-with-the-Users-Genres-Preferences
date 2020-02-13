import gc
from copy import deepcopy
from multiprocessing import Process, Queue, Semaphore

import pandas as pd
from surprise import KNNWithMeans, SVD, SVDpp, NMF
from surprise.prediction_algorithms.slope_one import SlopeOne

from src.config import user_label, NMF_LABEL, \
    SVDpp_LABEL, SVD_LABEL, SLOPE_LABEL, ITEMKNN_LABEL, USERKNN_LABEL, item_label, value_label, \
    CANDIDATES_LIST_SIZE, N_CORES, TIME_LIMIT, K_NEIGHBOR
from src.conversions.pandas_to_models import transform_testset, user_transactions_df_to_item_mapping
from src.conversions.suprise_and_pandas import surprise_to_pandas_get_candidates_items
from src.language_strings import LANGUAGE_USER_KNN_START, LANGUAGE_ITEM_KNN_START, \
    LANGUAGE_SVD_START, LANGUAGE_SVD_STOP, LANGUAGE_SVDPP_START, LANGUAGE_SVDPP_STOP, \
    LANGUAGE_NMF_START, LANGUAGE_NMF_STOP, LANGUAGE_SLOPE_ONE_START, LANGUAGE_SLOPE_ONE_STOP, LANGUAGE_ITEM_KNN_STOP, \
    LANGUAGE_USER_KNN_STOP
from src.posprocessing.step import postprocessing_calibration
from src.processing.recommendation_average import users_results_mean


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


def generate_recommendation(user_id, user_trainset_df, user_prefs_distr_df, user_testset_df, item_mapping, instance,
                            baseline_label, shared_queue, sem):
    user_unknown_items_df = get_unknown_items(user_id, user_trainset_df, item_mapping)

    sem.acquire()
    user_candidates_items_df = recommender_prediction(instance, user_unknown_items_df)
    sem.release()

    candidates_items_mapping = user_transactions_df_to_item_mapping(user_candidates_items_df, item_mapping)
    user_evaluation_results_df = postprocessing_calibration(user_prefs_distr_df=user_prefs_distr_df,
                                                            candidates_items_mapping=candidates_items_mapping,
                                                            test_items_ids=user_testset_df[item_label].tolist(),
                                                            baseline_label=baseline_label)
    sem.acquire()
    shared_queue.put(deepcopy(user_evaluation_results_df))
    sem.release()


# #################################################################################################################### #
# #################################################################################################################### #
# #################################################################################################################### #


def multiprocessing_recommendations(instance, users_prefs_distr_df, trainset_df, testset_df, item_mapping,
                                    recommender_label):
    # Preparing: users, results dataframe, shared queue over processes and the semaphore
    users_ids = users_prefs_distr_df.index.values.tolist()
    evaluation_results_df = pd.DataFrame()
    shared_queue = Queue()
    sem = Semaphore(TIME_LIMIT)
    # While has users to process
    while users_ids:
        cores_control = list(range(0, N_CORES))
        all_processes = []
        # As long as there are users on the list to process and cores to allocate, do
        while users_ids and cores_control:
            cores_control.pop(0)
            user_id = users_ids.pop(0)
            # Preparing user data
            user_trainset_df = trainset_df[trainset_df[user_label] == user_id]
            user_testset_df = testset_df[testset_df[user_label] == user_id]
            user_prefs_distr_df = users_prefs_distr_df.loc[user_id]
            # Creating the process
            p = Process(target=generate_recommendation,
                        args=(user_id, user_trainset_df, user_prefs_distr_df, user_testset_df, item_mapping, instance,
                              recommender_label, shared_queue, sem,))
            all_processes.append(p)
        # Start all process
        for p in all_processes:
            p.start()
        # Wait and close the all processes
        for p in all_processes:
            p.join(TIME_LIMIT)
            # p.close()
        # Get results from all processes
        user_evaluation_results = []
        while not shared_queue.empty():
            sem.acquire()
            user_evaluation_results.append(shared_queue.get(timeout=TIME_LIMIT))
            sem.release()
        # Concat and resume the results
        user_evaluation_results = pd.concat(user_evaluation_results)
        evaluation_results_df = pd.concat([evaluation_results_df, user_evaluation_results])
    recommender_results_df = users_results_mean(evaluation_results_df, recommender_label)
    return recommender_results_df


# #################################################################################################################### #
# #################################################################################################################### #
# #################################################################################################################### #


def user_knn_recommender_multiprocess(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping):
    # Algorithm Prediction
    print(LANGUAGE_USER_KNN_START)
    instance = KNNWithMeans(k=K_NEIGHBOR, sim_options={'name': 'pearson_baseline', 'user_based': True})
    instance.fit(trainset)
    print(LANGUAGE_USER_KNN_STOP)

    recommender_label = USERKNN_LABEL
    return multiprocessing_recommendations(instance, users_prefs_distr_df, trainset_df, testset_df, item_mapping,
                                           recommender_label)


def item_knn_recommender_multiprocess(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping):
    # Algorithm Prediction
    print(LANGUAGE_ITEM_KNN_START)
    instance = KNNWithMeans(k=K_NEIGHBOR, sim_options={'name': 'pearson_baseline', 'user_based': False})
    instance.fit(trainset)
    print(LANGUAGE_ITEM_KNN_STOP)

    recommender_label = ITEMKNN_LABEL
    return multiprocessing_recommendations(instance, users_prefs_distr_df, trainset_df, testset_df, item_mapping,
                                           recommender_label)


def svd_recommender_multiprocess(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping):
    # Algorithm Prediction
    print(LANGUAGE_SVD_START)
    instance = SVD()
    instance.fit(trainset)
    print(LANGUAGE_SVD_STOP)

    recommender_label = SVD_LABEL
    return multiprocessing_recommendations(instance, users_prefs_distr_df, trainset_df, testset_df, item_mapping,
                                           recommender_label)


def svdpp_recommender_multiprocess(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping):
    # Algorithm Prediction
    print(LANGUAGE_SVDPP_START)
    instance = SVDpp()
    instance.fit(trainset)
    print(LANGUAGE_SVDPP_STOP)

    recommender_label = SVDpp_LABEL
    return multiprocessing_recommendations(instance, users_prefs_distr_df, trainset_df, testset_df, item_mapping,
                                           recommender_label)


def nmf_recommender_multiprocess(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping):
    # Algorithm Prediction
    print(LANGUAGE_NMF_START)
    instance = NMF()
    instance.fit(trainset)
    print(LANGUAGE_NMF_STOP)

    recommender_label = NMF_LABEL
    return multiprocessing_recommendations(instance, users_prefs_distr_df, trainset_df, testset_df, item_mapping,
                                           recommender_label)


def slope_one_recommender_multiprocess(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping):
    # Algorithm Prediction
    print(LANGUAGE_SLOPE_ONE_START)
    instance = SlopeOne()
    instance.fit(trainset)
    print(LANGUAGE_SLOPE_ONE_STOP)

    recommender_label = SLOPE_LABEL
    return multiprocessing_recommendations(instance, users_prefs_distr_df, trainset_df, testset_df, item_mapping,
                                           recommender_label)


def all_recommenders_multiprocessing(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping):
    # recommenders_instance = [
    #     KNNWithMeans(k=K_NEIGHBOR, sim_options={'name': 'pearson_baseline', 'user_based': True}),
    #     KNNWithMeans(k=K_NEIGHBOR, sim_options={'name': 'pearson_baseline', 'user_based': False}),
    #     SVD(),
    #     SVDpp(),
    #     NMF(),
    #     SlopeOne()
    # ]
    # recommenders_labels = [
    #     USERKNN_LABEL,
    #     ITEMKNN_LABEL,
    #     SVD_LABEL,
    #     SVDpp_LABEL,
    #     NMF_LABEL,
    #     SLOPE_LABEL
    # ]
    recommenders_instance = [
        SVD(),
        NMF()
    ]
    recommenders_labels = [
        SVD_LABEL,
        NMF_LABEL
    ]
    evaluation_results_df = pd.DataFrame()
    for instance, label in zip(recommenders_instance, recommenders_labels):
        print('-' * 50)
        print("Start Recommender: " + label)
        print('-' * 50)
        instance.fit(trainset)
        results_df = multiprocessing_recommendations(instance, users_prefs_distr_df, trainset_df, testset_df,
                                                     item_mapping, label)
        evaluation_results_df = pd.concat([evaluation_results_df, results_df], sort=False)
        gc.collect()
    return evaluation_results_df
