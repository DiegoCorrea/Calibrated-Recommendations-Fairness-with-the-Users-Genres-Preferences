
import os

import pandas as pd

from src.config import DATASET_USAGE, K_FOLDS_VALUES, item_label, title_label, genre_label, algorithm_label, \
    FAIRNESS_METRIC_LABEL, LAMBDA_LABEL, EVALUATION_METRIC_LABEL, EVALUATION_VALUE_LABEL, evaluation_label, \
    LAMBDA_VALUE_LABEL, results_path, N_CORES
from src.conversions.pandas_to_models import transform_trainset
from src.graphics.experimental_evaluation import evaluation_linear_fairness_by_algo_over_lambda, evaluation_map_by_mc, \
    evaluation_map_by_mace
from src.language_strings import LANGUAGE_LOAD_DATA_SET, LANGUAGE_MOVIELENS_SELECTED, LANGUAGE_OMS_SELECTED, \
    LANGUAGE_DATA_SET_MEMORY, LANGUAGE_PROCESSING_STEP_START, LANGUAGE_PROCESSING_STEP_STOP
from src.models.item import create_item_mapping
from src.preprocessing.load_database import movielens_load_data, oms_load_data, yahoo_load_data
from src.processing.step import recommender_algorithms


def save_recommender_results(evaluation_results_df, k):
    for recommender in evaluation_results_df[algorithm_label].unique().tolist():
        recommender_subset_df = evaluation_results_df[evaluation_results_df[algorithm_label] == recommender]
        ave_dir = results_path + '/' + str(recommender)
        if not os.path.exists(ave_dir):
            os.makedirs(ave_dir)
        rating_path = os.path.join(ave_dir, str(k) + '.csv')
        recommender_subset_df.to_csv(rating_path, index=False)


def save_results(evaluation_results_df, k):
    if not os.path.exists(results_path):
        os.makedirs(results_path)
    rating_path = os.path.join(results_path, str(k) + '.csv')
    evaluation_results_df.to_csv(rating_path, index=False)


def k_fold_results_concat(evaluation_results_df):
    k_results_df = pd.DataFrame()
    print(evaluation_results_df)
    for recommender in evaluation_results_df[algorithm_label].unique().tolist():
        recommender_subset_df = evaluation_results_df[evaluation_results_df[algorithm_label] == recommender]
        for distance_metric in recommender_subset_df[FAIRNESS_METRIC_LABEL].unique().tolist():
            fairness_subset_df = recommender_subset_df[recommender_subset_df[FAIRNESS_METRIC_LABEL] == distance_metric]
            for lambda_type in fairness_subset_df[LAMBDA_LABEL].unique().tolist():
                lambda_subset_df = fairness_subset_df[fairness_subset_df[LAMBDA_LABEL] == lambda_type]
                for lambda_value in lambda_subset_df[LAMBDA_VALUE_LABEL].unique().tolist():
                    lambda_value_subset_df = lambda_subset_df[lambda_subset_df[LAMBDA_VALUE_LABEL] == lambda_value]
                    for evaluation_metric in lambda_value_subset_df[EVALUATION_METRIC_LABEL].unique().tolist():
                        evaluation_subset_df = lambda_value_subset_df[
                            lambda_value_subset_df[EVALUATION_METRIC_LABEL] == evaluation_metric]
                        result = evaluation_subset_df[EVALUATION_VALUE_LABEL].mean()
                        k_results_df = pd.concat([k_results_df,
                                                  pd.DataFrame(
                                                      [[recommender,
                                                        distance_metric,
                                                        lambda_type,
                                                        lambda_value,
                                                        evaluation_metric,
                                                        result]],
                                                      columns=evaluation_label
                                                  )
                                                  ])
    print(k_results_df)
    return k_results_df


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
    elif DATASET_USAGE == 1:
        print(LANGUAGE_OMS_SELECTED)
        trainset_df, testset_df, items_df = oms_load_data(k)
    else:
        print("Yahoo dataset")
        trainset_df, testset_df, items_df = yahoo_load_data(k)

    print(LANGUAGE_DATA_SET_MEMORY)
    trainset = transform_trainset(trainset_df)
    item_mapping = create_item_mapping(items_df, item_label, title_label, genre_label)
    print(LANGUAGE_PROCESSING_STEP_START)
    evaluation_results_df = recommender_algorithms(trainset, trainset_df, testset_df, item_mapping)
    print(LANGUAGE_PROCESSING_STEP_STOP)
    save_recommender_results(evaluation_results_df, k)
    return evaluation_results_df


def run_k_fold_times():
    k_results_list = [run_one_time(k) for k in range(0, K_FOLDS_VALUES)]
    k_results_df = k_fold_results_concat(pd.concat(k_results_list))
    os.system('cls' if os.name == 'nt' else 'clear')

    for evaluation_metric in k_results_df[EVALUATION_METRIC_LABEL].unique().tolist():
        evaluation_subset_df = k_results_df[
            k_results_df[EVALUATION_METRIC_LABEL] == evaluation_metric]
        print(evaluation_subset_df.sort_values(by=[EVALUATION_VALUE_LABEL]))
    save_results(k_results_df, 'all')
    print('Creating graphics...')
    evaluation_linear_fairness_by_algo_over_lambda(k_results_df, 'all')
    evaluation_map_by_mc(k_results_df, 'all')
    evaluation_map_by_mace(k_results_df, 'all')


if __name__ == '__main__':
    print("Cores: " + str(N_CORES))
    run_k_fold_times()
