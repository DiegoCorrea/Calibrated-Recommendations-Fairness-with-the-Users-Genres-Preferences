import numpy as np
import pandas as pd

from src.config import RECOMMENDATION_LIST_SIZE, KL_LABEL, HE_LABEL, CHI_LABEL, FAIRNESS_METRIC_LABEL, \
    VARIANCE_TRADE_OFF_LABEL, \
    COUNT_GENRES_TRADE_OFF_LABEL, TRADE_OFF_LABEL, evaluation_label, MACE_LABEL, FIXED_LABEL, MAP_LABEL, \
    MRR_LABEL, order_label, MC_LABEL, item_label
from src.conversions.pandas_to_models import items_to_pandas
from src.evaluation.mace import ace
from src.evaluation.map import average_precision
from src.evaluation.misscalibration import mc
from src.evaluation.mrr import mrr
from src.language_strings import LANGUAGE_CHI, LANGUAGE_HE, LANGUAGE_KL, LANGUAGE_COUNT_GENRES, LANGUAGE_VARIANCE
from src.posprocessing.greedy_algorithms import surrogate_submodular
from src.posprocessing.lambda_value import count_genres, variance


def personalized_trade_off(user_preference_distribution, reco_items, config, n=RECOMMENDATION_LIST_SIZE):
    lmbda = 0.0
    if config[TRADE_OFF_LABEL] == COUNT_GENRES_TRADE_OFF_LABEL:
        lmbda = count_genres(user_preference_distribution)
    else:
        lmbda = variance(user_preference_distribution)
    return surrogate_submodular(user_preference_distribution, reco_items, config, n, lmbda=lmbda)


def postprocessing_calibration(user_prefs_distr_df, candidates_items_mapping, test_items_ids, baseline_label):
    # print('Pos processing - Start')
    config = dict()
    evaluation_results_df = pd.DataFrame()
    for distance_metric, distance_metric_lang in zip([KL_LABEL, HE_LABEL, CHI_LABEL],
                                                     [LANGUAGE_KL, LANGUAGE_HE, LANGUAGE_CHI]):
        # print("* * " + distance_metric_lang + " * *")
        config[FAIRNESS_METRIC_LABEL] = distance_metric
        # Fixed lambda value
        for lambda_value in np.arange(0, 1.1, 0.1):
            lambda_value = round(lambda_value, 1)
            final_reco_df = items_to_pandas(
                dict(surrogate_submodular(user_prefs_distr_df, candidates_items_mapping, config, lmbda=lambda_value)))
            final_reco_df.sort_values(by=[order_label], ascending=True, inplace=True)
            ace_result = ace(user_prefs_distr_df, final_reco_df, candidates_items_mapping)
            ap_result = average_precision(final_reco_df, test_items_ids)
            rr_result = mrr(final_reco_df, test_items_ids)
            mc_value = mc(user_prefs_distr_df, final_reco_df, candidates_items_mapping, config)
            evaluation_results_df = pd.concat([evaluation_results_df,
                                               pd.DataFrame(
                                                   [[baseline_label,
                                                     distance_metric,
                                                     FIXED_LABEL,
                                                     lambda_value,
                                                     MACE_LABEL,
                                                     ace_result]],
                                                   columns=evaluation_label
                                               )])
            evaluation_results_df = pd.concat([evaluation_results_df,
                                               pd.DataFrame(
                                                   [[baseline_label,
                                                     distance_metric,
                                                     FIXED_LABEL,
                                                     lambda_value,
                                                     MAP_LABEL,
                                                     ap_result]],
                                                   columns=evaluation_label
                                               )])
            evaluation_results_df = pd.concat([evaluation_results_df,
                                               pd.DataFrame(
                                                   [[baseline_label,
                                                     distance_metric,
                                                     FIXED_LABEL,
                                                     lambda_value,
                                                     MRR_LABEL,
                                                     rr_result]],
                                                   columns=evaluation_label
                                               )])
            evaluation_results_df = pd.concat([evaluation_results_df,
                                               pd.DataFrame(
                                                   [[baseline_label,
                                                     distance_metric,
                                                     FIXED_LABEL,
                                                     lambda_value,
                                                     MC_LABEL,
                                                     mc_value]],
                                                   columns=evaluation_label
                                               )])
        # Personalized lambda
        for trade_off, trade_off_lang, lambda_value in zip([COUNT_GENRES_TRADE_OFF_LABEL, VARIANCE_TRADE_OFF_LABEL],
                                                           [LANGUAGE_COUNT_GENRES, LANGUAGE_VARIANCE],
                                                           ['CGR', 'VAR']):
            config[TRADE_OFF_LABEL] = trade_off
            final_reco_df = items_to_pandas(
                dict(personalized_trade_off(user_prefs_distr_df, candidates_items_mapping, config)))
            final_reco_df.sort_values(by=[order_label], ascending=True, inplace=True)
            ace_result = ace(user_prefs_distr_df, final_reco_df, candidates_items_mapping)
            map_result = average_precision(final_reco_df, test_items_ids)
            mrr_result = mrr(final_reco_df, test_items_ids)
            mc_value = mc(user_prefs_distr_df, final_reco_df, candidates_items_mapping, config)
            evaluation_results_df = pd.concat([evaluation_results_df,
                                               pd.DataFrame(
                                                   [[baseline_label,
                                                     distance_metric,
                                                     trade_off,
                                                     lambda_value,
                                                     MACE_LABEL,
                                                     ace_result]],
                                                   columns=evaluation_label
                                               )])
            evaluation_results_df = pd.concat([evaluation_results_df,
                                               pd.DataFrame(
                                                   [[baseline_label,
                                                     distance_metric,
                                                     trade_off,
                                                     lambda_value,
                                                     MAP_LABEL,
                                                     map_result]],
                                                   columns=evaluation_label
                                               )])
            evaluation_results_df = pd.concat([evaluation_results_df,
                                               pd.DataFrame(
                                                   [[baseline_label,
                                                     distance_metric,
                                                     trade_off,
                                                     lambda_value,
                                                     MRR_LABEL,
                                                     mrr_result]],
                                                   columns=evaluation_label
                                               )])
            evaluation_results_df = pd.concat([evaluation_results_df,
                                               pd.DataFrame(
                                                   [[baseline_label,
                                                     distance_metric,
                                                     trade_off,
                                                     lambda_value,
                                                     MC_LABEL,
                                                     mc_value]],
                                                   columns=evaluation_label
                                               )])
    return evaluation_results_df
