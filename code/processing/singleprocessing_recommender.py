import pandas as pd
from surprise import KNNWithMeans, SVD, SVDpp, NMF
from surprise.prediction_algorithms.slope_one import SlopeOne

from code.config import user_label, NMF_LABEL, \
    SVDpp_LABEL, SVD_LABEL, SLOPE_LABEL, ITEMKNN_LABEL, USERKNN_LABEL, item_label, value_label, K_NEIGHBOR
from code.conversions.pandas_to_models import transform_testset, user_transactions_df_to_item_mapping
from code.conversions.suprise_and_pandas import surprise_to_pandas_get_candidates_items
from code.language_strings import LANGUAGE_USER_KNN_START, LANGUAGE_ITEM_KNN_START, \
    LANGUAGE_SVD_START, LANGUAGE_SVD_STOP, LANGUAGE_SVDPP_START, LANGUAGE_SVDPP_STOP, \
    LANGUAGE_NMF_START, LANGUAGE_NMF_STOP, LANGUAGE_SLOPE_ONE_START, LANGUAGE_SLOPE_ONE_STOP
from code.posprocessing.step import postprocessing_calibration
from code.processing.recommendation_average import users_results_mean


def recommendation_and_posprocessing(user_id, user_trainset_df, user_prefs_distr_df, user_testset_df, item_mapping,
                                     instance, baseline_label):
    keys_list = item_mapping.keys()
    know_items = user_trainset_df[item_label].unique().tolist()
    unknow_items = set(keys_list) - set(know_items)
    data = {item_label: list(unknow_items)}

    user_testset = pd.DataFrame.from_dict(data)
    user_testset[user_label] = user_id
    user_testset[value_label] = 0.0

    candidates_items_prediction = instance.test(transform_testset(user_testset))
    user_candidates_items_df = surprise_to_pandas_get_candidates_items(candidates_items_prediction)
    user_candidates_items_df.sort_values(by=[value_label], ascending=False, inplace=True)

    candidates_items_mapping = user_transactions_df_to_item_mapping(user_candidates_items_df, item_mapping)
    result_df = postprocessing_calibration(user_prefs_distr_df=user_prefs_distr_df,
                                           candidates_items_mapping=candidates_items_mapping,
                                           test_items_ids=user_testset_df[item_label].tolist(),
                                           baseline_label=baseline_label)
    return result_df


# #################################################################################################################### #
# #################################################################################################################### #
# #################################################################################################################### #


def user_knn_recommender(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping):
    # Recommender Prediction
    print(LANGUAGE_USER_KNN_START)
    instance = KNNWithMeans(k=K_NEIGHBOR, sim_options={'name': 'pearson_baseline', 'user_based': True})
    instance.fit(trainset)
    print(LANGUAGE_USER_KNN_START)

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
    instance = KNNWithMeans(k=K_NEIGHBOR, sim_options={'name': 'pearson_baseline', 'user_based': False})
    instance.fit(trainset)
    print(LANGUAGE_ITEM_KNN_START)

    evaluation_results_df = [
        recommendation_and_posprocessing(user_id, trainset_df[trainset_df[user_label] == user_id], user_prefs_distr_df,
                                         testset_df[testset_df[user_label] == user_id], item_mapping, instance,
                                         ITEMKNN_LABEL)
        for user_id, user_prefs_distr_df in users_prefs_distr_df.iterrows()]
    evaluation_results_df = pd.concat(evaluation_results_df)
    recommender_results_df = users_results_mean(evaluation_results_df, ITEMKNN_LABEL)
    return recommender_results_df


def svd_recommender(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping):
    print(LANGUAGE_SVD_START)
    instance = SVD()
    instance.fit(trainset)
    print(LANGUAGE_SVD_STOP)

    evaluation_results_df = [
        recommendation_and_posprocessing(user_id, trainset_df[trainset_df[user_label] == user_id], user_prefs_distr_df,
                                         testset_df[testset_df[user_label] == user_id], item_mapping, instance,
                                         SVD_LABEL)
        for user_id, user_prefs_distr_df in users_prefs_distr_df.iterrows()]
    evaluation_results_df = pd.concat(evaluation_results_df)
    recommender_results_df = users_results_mean(evaluation_results_df, SVD_LABEL)
    return recommender_results_df


def svdpp_recommender(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping):
    print(LANGUAGE_SVDPP_START)
    instance = SVDpp()
    instance.fit(trainset)
    print(LANGUAGE_SVDPP_STOP)

    evaluation_results_df = [
        recommendation_and_posprocessing(user_id, user_prefs_distr_df, SVDpp_LABEL, testset_df, instance, item_mapping)
        for user_id, user_prefs_distr_df in users_prefs_distr_df.iterrows()]
    evaluation_results_df = pd.concat(evaluation_results_df)
    recommender_results_df = users_results_mean(evaluation_results_df, SVDpp_LABEL)
    return recommender_results_df


def nmf_recommender(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping):
    print(LANGUAGE_NMF_START)
    instance = NMF()
    instance.fit(trainset)
    print(LANGUAGE_NMF_STOP)

    evaluation_results_df = [
        recommendation_and_posprocessing(user_id, trainset_df[trainset_df[user_label] == user_id], user_prefs_distr_df,
                                         testset_df[testset_df[user_label] == user_id], item_mapping, instance,
                                         NMF_LABEL)
        for user_id, user_prefs_distr_df in users_prefs_distr_df.iterrows()]
    evaluation_results_df = pd.concat(evaluation_results_df)
    recommender_results_df = users_results_mean(evaluation_results_df, NMF_LABEL)
    return recommender_results_df


def slope_one_recommender(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping):
    print(LANGUAGE_SLOPE_ONE_START)
    instance = SlopeOne()
    instance.fit(trainset)
    print(LANGUAGE_SLOPE_ONE_STOP)

    evaluation_results_df = [
        recommendation_and_posprocessing(user_id, user_prefs_distr_df, SLOPE_LABEL,
                                         trainset_df[trainset_df[user_label] == user_id], testset_df, instance,
                                         item_mapping)
        for user_id, user_prefs_distr_df in users_prefs_distr_df.iterrows()]
    evaluation_results_df = pd.concat(evaluation_results_df)
    recommender_results_df = users_results_mean(evaluation_results_df, SLOPE_LABEL)
    return recommender_results_df
