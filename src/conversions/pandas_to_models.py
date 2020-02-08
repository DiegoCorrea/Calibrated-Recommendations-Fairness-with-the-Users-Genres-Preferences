from copy import deepcopy

import pandas as pd
from surprise import Reader, Dataset

from src.config import user_label, item_label, value_label, order_label, title_label, genre_label
from src.language_strings import LANGUAGE_PANDAS_TO_SURPRISE_DATA
from src.models.item import create_item_mapping


def user_transactions_df_to_item_mapping(user_transactions_df, item_mapping):
    user_items = {}
    for row in user_transactions_df.itertuples():
        item_id = getattr(row, item_label)
        user_items[item_id] = deepcopy(item_mapping[item_id])
        user_items[item_id].score = getattr(row, value_label)
    return user_items


def transform_all_transaction_df_to_item_mapping(transactions_df, item_mapping):
    print(LANGUAGE_PANDAS_TO_SURPRISE_DATA)
    transactions_item_mapping = {}
    for user_id in transactions_df[user_label].unique().tolist():
        user_transactions_df = transactions_df[transactions_df[user_label] == user_id]
        transactions_item_mapping[user_id] = user_transactions_df_to_item_mapping(user_transactions_df, item_mapping)
    return transactions_item_mapping


def items_to_pandas(users_items):
    results_df = pd.DataFrame()
    order = 0
    user_results = []
    for item_id, item in users_items.items():
        order += 1
        user_results += [pd.DataFrame(data=[[item_id, item.score, order]],
                                      columns=[item_label, value_label, order_label])]
    user_results = pd.concat(user_results, sort=False)
    results_df = pd.concat([results_df, user_results], sort=False)
    return results_df


def transform_dataset(trainset_df, testset_df, items_df):
    print(LANGUAGE_PANDAS_TO_SURPRISE_DATA)
    item_mapping = create_item_mapping(items_df, item_label, title_label, genre_label)

    reader_train = Reader()
    data_train = Dataset.load_from_df(trainset_df[[user_label, item_label, value_label]], reader_train)
    trainset = data_train.build_full_trainset()

    reader_test = Reader()
    data_test = Dataset.load_from_df(testset_df[[user_label, item_label, value_label]], reader_test)
    testset = data_test.build_full_trainset()
    testset = testset.build_testset()
    # testset = trainset.build_anti_testset(fill=0)

    return trainset, testset, item_mapping


def transform_trainset(trainset_df):
    reader_train = Reader()
    data_train = Dataset.load_from_df(trainset_df[[user_label, item_label, value_label]], reader_train)
    return data_train.build_full_trainset()


def transform_testset(testset_df):
    reader_test = Reader()
    data_test = Dataset.load_from_df(testset_df[[user_label, item_label, value_label]], reader_test)
    testset = data_test.build_full_trainset()
    return testset.build_testset()
