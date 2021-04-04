import os

import pandas as pd

from code.config import DATASET_USAGE, item_label, title_label, genre_label, \
    results_path, N_CORES
from code.conversions.pandas_to_models import transform_trainset
from code.graphics.experimental_evaluation import evaluation_linear_fairness_by_algo_over_lambda, evaluation_map_by_mc
from code.language_strings import LANGUAGE_LOAD_DATA_SET, LANGUAGE_MOVIELENS_SELECTED, LANGUAGE_OMS_SELECTED, \
    LANGUAGE_DATA_SET_MEMORY, LANGUAGE_PROCESSING_STEP_START, LANGUAGE_PROCESSING_STEP_STOP
from code.models.item import create_item_mapping
from code.preprocessing.load_database import movielens_load_data, oms_load_data
from code.processing.step import recommender_algorithms


def save_results(evaluation_results_df, k):
    save_dir = None
    if k == 0:
        save_dir = results_path + '/all/'
    else:
        save_dir = results_path + '/' + str(k)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    rating_path = os.path.join(save_dir, 'result_' + str(k) + '.csv')
    evaluation_results_df.to_csv(rating_path, index=False)


def run_one_time(k=1):
    print(LANGUAGE_LOAD_DATA_SET)
    print('*' * 30)
    print(str('-' * 13) + str(k) + str('-' * 13))
    print('*' * 30)
    trainset_df = pd.DataFrame()
    testset_df = pd.DataFrame()
    items_df = pd.DataFrame()
    if DATASET_USAGE == 0:
        print(LANGUAGE_MOVIELENS_SELECTED)
        trainset_df, testset_df, items_df = movielens_load_data(k)
    else:
        print(LANGUAGE_OMS_SELECTED)
        trainset_df, testset_df, items_df = oms_load_data(k)
    print(LANGUAGE_DATA_SET_MEMORY)
    trainset = transform_trainset(trainset_df)
    item_mapping = create_item_mapping(items_df, item_label, title_label, genre_label)
    print(LANGUAGE_PROCESSING_STEP_START)
    evaluation_results_df = recommender_algorithms(trainset, trainset_df, testset_df, item_mapping)
    print(LANGUAGE_PROCESSING_STEP_STOP)
    save_results(evaluation_results_df, k)
    evaluation_linear_fairness_by_algo_over_lambda(evaluation_results_df, k)
    evaluation_map_by_mc(evaluation_results_df, k)
    return evaluation_results_df


if __name__ == '__main__':
    print("Cores: " + str(N_CORES))
    fold_number = 1
    run_one_time(k=fold_number)
