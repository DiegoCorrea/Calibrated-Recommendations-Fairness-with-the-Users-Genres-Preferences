import os

import pandas as pd

from src.config import results_path
from src.graphics.experimental_evaluation import evaluation_map_by_mc, evaluation_linear_fairness_by_algo_over_lambda

if __name__ == '__main__':
    evaluation_results_df = pd.read_csv(os.path.join(str(results_path + '/1/'), 'result_1.csv'))
    evaluation_linear_fairness_by_algo_over_lambda(evaluation_results_df, 1)
    evaluation_map_by_mc(evaluation_results_df, 1)
