import pandas as pd

from src.language_strings import LANGUAGE_RECOMMENDER_ALGORITHMS_STOP, \
    LANGUAGE_RECOMMENDER_ALGORITHMS_START
from src.posprocessing.distributions import multiprocess_get_distribution
from src.processing.multiprocessing_recommender import item_knn_recommender_multiprocess, \
    user_knn_recommender_multiprocess, svdpp_recommender_multiprocess, svd_recommender_multiprocess, \
    nmf_recommender_multiprocess, slope_one_recommender_multiprocess, all_recommenders_multiprocessing
from src.processing.singleprocessing_recommender import item_knn_recommender, user_knn_recommender, svd_recommender, \
    svdpp_recommender, nmf_recommender, slope_one_recommender


# #################################################################################################################### #
# ################################################# Single Process ################################################### #
# #################################################################################################################### #


def collaborative_filtering_singleprocess(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping):
    evaluation_results_df = pd.DataFrame()

    # # Item KNN
    recommender_results_df = item_knn_recommender(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping)
    evaluation_results_df = pd.concat([evaluation_results_df, recommender_results_df], sort=False)

    # # User KNN
    recommender_results_df = user_knn_recommender(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping)
    evaluation_results_df = pd.concat([evaluation_results_df, recommender_results_df], sort=False)

    # # SVD
    recommender_results_df = svd_recommender(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping)
    evaluation_results_df = pd.concat([evaluation_results_df, recommender_results_df], sort=False)

    # # SVDpp
    recommender_results_df = svdpp_recommender(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping)
    evaluation_results_df = pd.concat([evaluation_results_df, recommender_results_df], sort=False)

    # # NMF
    recommender_results_df = nmf_recommender(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping)
    evaluation_results_df = pd.concat([evaluation_results_df, recommender_results_df], sort=False)

    # # Sloope One
    recommender_results_df = slope_one_recommender(trainset, users_prefs_distr_df, trainset_df, testset_df,
                                                   item_mapping)
    evaluation_results_df = pd.concat([evaluation_results_df, recommender_results_df], sort=False)

    return evaluation_results_df


# #################################################################################################################### #
# ################################################# Multi Process #################################################### #
# #################################################################################################################### #

def collaborative_filtering_multiprocess(trainset, users_prefs_distr_df, trainset_df, testset_df, item_mapping):
    evaluation_results_df = pd.DataFrame()

    # # Item KNN
    recommender_results_df = item_knn_recommender_multiprocess(trainset, users_prefs_distr_df, trainset_df, testset_df,
                                                               item_mapping)
    evaluation_results_df = pd.concat([evaluation_results_df, recommender_results_df], sort=False)

    # # User KNN
    recommender_results_df = user_knn_recommender_multiprocess(trainset, users_prefs_distr_df, trainset_df, testset_df,
                                                               item_mapping)
    evaluation_results_df = pd.concat([evaluation_results_df, recommender_results_df], sort=False)

    # # SVD
    recommender_results_df = svd_recommender_multiprocess(trainset, users_prefs_distr_df, trainset_df, testset_df,
                                                          item_mapping)
    evaluation_results_df = pd.concat([evaluation_results_df, recommender_results_df], sort=False)

    # # SVDpp
    recommender_results_df = svdpp_recommender_multiprocess(trainset, users_prefs_distr_df, trainset_df, testset_df,
                                                            item_mapping)
    evaluation_results_df = pd.concat([evaluation_results_df, recommender_results_df], sort=False)

    # # NMF
    recommender_results_df = nmf_recommender_multiprocess(trainset, users_prefs_distr_df, trainset_df, testset_df,
                                                          item_mapping)
    evaluation_results_df = pd.concat([evaluation_results_df, recommender_results_df], sort=False)

    # # Sloope One
    recommender_results_df = slope_one_recommender_multiprocess(trainset, users_prefs_distr_df, trainset_df, testset_df,
                                                                item_mapping)
    evaluation_results_df = pd.concat([evaluation_results_df, recommender_results_df], sort=False)

    return evaluation_results_df


# #################################################################################################################### #
# ############################################### Recommender Caller ################################################# #
# #################################################################################################################### #


def recommender_algorithms(trainset, trainset_df, testset_df, item_mapping):
    # users_prefs_distr_df = get_distribution(trainset_df, item_mapping)
    users_prefs_distr_df = multiprocess_get_distribution(trainset_df, item_mapping)
    print(LANGUAGE_RECOMMENDER_ALGORITHMS_START)
    # evaluation_results_df = collaborative_filtering_singleprocess(trainset, users_prefs_distr_df, trainset_df,
    #                                                               testset_df, item_mapping)
    # evaluation_results_df = collaborative_filtering_multiprocess(trainset, users_prefs_distr_df, trainset_df,
    #                                                              testset_df, item_mapping)
    evaluation_results_df = all_recommenders_multiprocessing(trainset, users_prefs_distr_df, trainset_df, testset_df,
                                                             item_mapping)

    print(LANGUAGE_RECOMMENDER_ALGORITHMS_STOP)
    return evaluation_results_df
