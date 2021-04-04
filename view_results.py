import os

import pandas as pd

from code.config import results_path
from code.graphics.experimental_evaluation import evaluation_map_by_mc, evaluation_linear_fairness_by_algo_over_lambda, \
    evaluation_map_by_mace

if __name__ == '__main__':
    evaluation_results_df = pd.read_csv(os.path.join(results_path, 'all.csv'))
    evaluation_linear_fairness_by_algo_over_lambda(evaluation_results_df, 'all')
    evaluation_map_by_mc(evaluation_results_df, 'all')
    evaluation_map_by_mace(evaluation_results_df, 'all')
