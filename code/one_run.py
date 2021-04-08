import os

import pandas as pd

from main import k_fold_results_concat, run_one_time, save_results
from graphics.experimental_evaluation import evaluation_linear_fairness_by_algo_over_lambda, evaluation_map_by_mc, \
    evaluation_map_by_mace
from settings.config import N_CORES, EVALUATION_METRIC_LABEL, EVALUATION_VALUE_LABEL

if __name__ == '__main__':
    print("Cores: " + str(N_CORES))
    fold_number = 1
    k_results_df = k_fold_results_concat(pd.concat([run_one_time(k=fold_number)]))
    os.system('cls' if os.name == 'nt' else 'clear')
    for evaluation_metric in k_results_df[EVALUATION_METRIC_LABEL].unique().tolist():
        evaluation_subset_df = k_results_df[
            k_results_df[EVALUATION_METRIC_LABEL] == evaluation_metric]
        print(evaluation_subset_df.sort_values(by=[EVALUATION_VALUE_LABEL]))
    save_results(k_results_df, fold_number)
    print('Creating graphics...')
    evaluation_linear_fairness_by_algo_over_lambda(k_results_df, fold_number)
    evaluation_map_by_mc(k_results_df, fold_number)
    evaluation_map_by_mace(k_results_df, fold_number)
