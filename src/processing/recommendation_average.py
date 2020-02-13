import pandas as pd

from src.config import FAIRNESS_METRIC_LABEL, LAMBDA_LABEL, LAMBDA_VALUE_LABEL, EVALUATION_METRIC_LABEL, \
    EVALUATION_VALUE_LABEL, evaluation_label


def users_results_mean(evaluation_results_df, baseline_label):
    recommender_results_df = pd.DataFrame()
    for distance_metric in evaluation_results_df[FAIRNESS_METRIC_LABEL].unique().tolist():
        fairness_subset_df = evaluation_results_df[evaluation_results_df[FAIRNESS_METRIC_LABEL] == distance_metric]
        for lambda_type in fairness_subset_df[LAMBDA_LABEL].unique().tolist():
            lambda_subset_df = fairness_subset_df[fairness_subset_df[LAMBDA_LABEL] == lambda_type]
            for lambda_value in lambda_subset_df[LAMBDA_VALUE_LABEL].unique().tolist():
                lambda_value_subset_df = lambda_subset_df[lambda_subset_df[LAMBDA_VALUE_LABEL] == lambda_value]
                for evaluation_metric in lambda_value_subset_df[EVALUATION_METRIC_LABEL].unique().tolist():
                    evaluation_subset_df = lambda_value_subset_df[
                        lambda_value_subset_df[EVALUATION_METRIC_LABEL] == evaluation_metric]
                    value = evaluation_subset_df[EVALUATION_VALUE_LABEL].mean()
                    recommender_results_df = pd.concat([recommender_results_df,
                                                        pd.DataFrame(
                                                            [[baseline_label,
                                                              distance_metric,
                                                              lambda_type,
                                                              lambda_value,
                                                              evaluation_metric,
                                                              value]],
                                                            columns=evaluation_label
                                                        )
                                                        ])
    return recommender_results_df


def print_results(evaluation_results_df):
    for evaluation_metric in evaluation_results_df[EVALUATION_METRIC_LABEL].unique().tolist():
        evaluation_subset_df = evaluation_results_df[
            evaluation_results_df[EVALUATION_METRIC_LABEL] == evaluation_metric]
        print(evaluation_subset_df.sort_values(by=[EVALUATION_VALUE_LABEL]))
