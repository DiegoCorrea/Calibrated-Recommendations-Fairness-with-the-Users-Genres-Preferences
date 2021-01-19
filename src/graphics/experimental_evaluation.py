import os
from copy import deepcopy

import matplotlib

from src.config import EVALUATION_METRIC_LABEL, FAIRNESS_METRIC_LABEL, algorithm_label, FONT_SIZE_VALUE, \
    LAMBDA_VALUE_LABEL, EVALUATION_VALUE_LABEL, DPI_VALUE, QUALITY_VALUE, markers_list, line_style_list, \
    postprocessing_results_path, MAP_LABEL, MC_LABEL, MACE_LABEL

matplotlib.use('Agg')
import matplotlib.pyplot as plt

matplotlib.style.use('ggplot')


def evaluation_linear_fairness_by_algo_over_lambda(evaluation_results_df, k):
    if k == 0:
        save_dir = postprocessing_results_path + 'all/'
    else:
        save_dir = postprocessing_results_path + '/' + str(k) + '/'
    for metric in evaluation_results_df[EVALUATION_METRIC_LABEL].unique().tolist():
        evaluation_subset_df = evaluation_results_df[evaluation_results_df[EVALUATION_METRIC_LABEL] == metric]
        for recommender in evaluation_subset_df[algorithm_label].unique().tolist():
            recommender_subset_df = evaluation_subset_df[evaluation_subset_df[algorithm_label] == recommender]
            plt.figure()
            plt.grid(True)
            plt.xlabel('Weight', fontsize=FONT_SIZE_VALUE)
            lambda_values = [str(x) for x in recommender_subset_df[LAMBDA_VALUE_LABEL].unique().tolist()]
            plt.xticks(range(0, len(lambda_values)), lambda_values)
            plt.ylabel(metric, fontsize=FONT_SIZE_VALUE)
            fairness_measures = recommender_subset_df[FAIRNESS_METRIC_LABEL].unique().tolist()
            n = len(fairness_measures)
            for distance_metric, m, l in zip(fairness_measures, markers_list[:n], line_style_list[:n]):
                distance_subset_df = recommender_subset_df[
                    recommender_subset_df[FAIRNESS_METRIC_LABEL] == distance_metric]
                plt.plot([str(x) for x in distance_subset_df[LAMBDA_VALUE_LABEL].tolist()],
                         distance_subset_df[EVALUATION_VALUE_LABEL].tolist(), alpha=0.5, linestyle=l, marker=m,
                         label=distance_metric)
            plt.legend(loc='best', borderaxespad=0.)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            plt.savefig(
                save_dir
                + metric
                + '_'
                + recommender
                + '.png',
                format='png',
                dpi=DPI_VALUE,
                quality=QUALITY_VALUE,
                bbox_inches='tight'
            )
            plt.close('all')


def evaluation_map_by_mc(evaluation_results_df, k):
    if k == 0:
        save_dir = postprocessing_results_path + 'all/'
    else:
        save_dir = postprocessing_results_path + '/' + str(k) + '/'
    for distance_metric in evaluation_results_df[FAIRNESS_METRIC_LABEL].unique().tolist():
        map_subset_df = evaluation_results_df[
            (evaluation_results_df[FAIRNESS_METRIC_LABEL] == distance_metric) & (evaluation_results_df[
                                                                                     EVALUATION_METRIC_LABEL] == MAP_LABEL)]
        mc_subset_df = evaluation_results_df[
            (evaluation_results_df[FAIRNESS_METRIC_LABEL] == distance_metric) & (
                    evaluation_results_df[EVALUATION_METRIC_LABEL] == MC_LABEL)]
        plt.figure()
        plt.grid(True)
        plt.xlabel(MAP_LABEL, fontsize=FONT_SIZE_VALUE)
        plt.ylabel(MC_LABEL, fontsize=FONT_SIZE_VALUE)
        algorithm_list = evaluation_results_df[algorithm_label].unique().tolist()
        n = len(algorithm_list)
        for algorithm, m, l in zip(algorithm_list, markers_list[:n], line_style_list[:n]):
            algorithm_map_subset_df = deepcopy(map_subset_df[
                                                   map_subset_df[algorithm_label] == algorithm])
            algorihm_mc_subset_df = deepcopy(mc_subset_df[
                                                 mc_subset_df[algorithm_label] == algorithm])
            algorithm_map_subset_df[LAMBDA_VALUE_LABEL] = algorithm_map_subset_df[LAMBDA_VALUE_LABEL].astype('category')
            algorithm_map_subset_df.sort_values(by=[LAMBDA_VALUE_LABEL], inplace=True)
            algorihm_mc_subset_df[LAMBDA_VALUE_LABEL] = algorihm_mc_subset_df[LAMBDA_VALUE_LABEL].astype('category')
            algorihm_mc_subset_df.sort_values(by=[LAMBDA_VALUE_LABEL], inplace=True)
            plt.plot(algorithm_map_subset_df[EVALUATION_VALUE_LABEL].tolist(),
                     algorihm_mc_subset_df[EVALUATION_VALUE_LABEL].tolist(), alpha=0.5, linestyle=l, marker=m,
                     label=algorithm)
        plt.legend(loc='best', borderaxespad=0.)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        plt.savefig(
            save_dir
            + MAP_LABEL
            + '_'
            + MC_LABEL
            + '_'
            + distance_metric
            + '.png',
            format='png',
            dpi=DPI_VALUE,
            quality=QUALITY_VALUE,
            bbox_inches='tight'
        )
        plt.close('all')


def evaluation_map_by_mace(evaluation_results_df, k):
    if k == 0:
        save_dir = postprocessing_results_path + 'all/'
    else:
        save_dir = postprocessing_results_path + '/' + str(k) + '/'
    for distance_metric in evaluation_results_df[FAIRNESS_METRIC_LABEL].unique().tolist():
        map_subset_df = evaluation_results_df[
            (evaluation_results_df[FAIRNESS_METRIC_LABEL] == distance_metric) & (evaluation_results_df[
                                                                                     EVALUATION_METRIC_LABEL] == MAP_LABEL)]
        mc_subset_df = evaluation_results_df[
            (evaluation_results_df[FAIRNESS_METRIC_LABEL] == distance_metric) & (
                    evaluation_results_df[EVALUATION_METRIC_LABEL] == MACE_LABEL)]
        plt.figure()
        plt.grid(True)
        plt.xlabel(MAP_LABEL, fontsize=FONT_SIZE_VALUE)
        plt.ylabel(MACE_LABEL, fontsize=FONT_SIZE_VALUE)
        algorithm_list = evaluation_results_df[algorithm_label].unique().tolist()
        n = len(algorithm_list)
        for algorithm, m, l in zip(algorithm_list, markers_list[:n], line_style_list[:n]):
            algorithm_map_subset_df = deepcopy(map_subset_df[
                                                   map_subset_df[algorithm_label] == algorithm])
            algorihm_mc_subset_df = deepcopy(mc_subset_df[
                                                 mc_subset_df[algorithm_label] == algorithm])
            algorithm_map_subset_df[LAMBDA_VALUE_LABEL] = algorithm_map_subset_df[LAMBDA_VALUE_LABEL].astype('category')
            algorithm_map_subset_df.sort_values(by=[LAMBDA_VALUE_LABEL], inplace=True)
            algorihm_mc_subset_df[LAMBDA_VALUE_LABEL] = algorihm_mc_subset_df[LAMBDA_VALUE_LABEL].astype('category')
            algorihm_mc_subset_df.sort_values(by=[LAMBDA_VALUE_LABEL], inplace=True)
            plt.plot(algorithm_map_subset_df[EVALUATION_VALUE_LABEL].tolist(),
                     algorihm_mc_subset_df[EVALUATION_VALUE_LABEL].tolist(), alpha=0.5, linestyle=l, marker=m,
                     label=algorithm)
        plt.legend(loc='best', borderaxespad=0.)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        plt.savefig(
            save_dir
            + MAP_LABEL
            + '_'
            + MACE_LABEL
            + '_'
            + distance_metric
            + '.png',
            format='png',
            dpi=DPI_VALUE,
            quality=QUALITY_VALUE,
            bbox_inches='tight'
        )
        plt.close('all')
