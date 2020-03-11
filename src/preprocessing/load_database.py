import os

import pandas as pd

from src.config import (movielens_clean_dir, movielens_rating, movielens_items, oms_clean_dir, oms_rating, oms_item,
                        item_label, user_label, train_file, test_file)


# ################################################################# #
# Movielens Data
# ################################################################# #


def movielens_load_full_dataset():
    return pd.read_csv(os.path.join(movielens_clean_dir, movielens_rating))


def movielens_load_preference_trainset(fold):
    return pd.read_csv(os.path.join(movielens_clean_dir + '/' + str(fold), train_file))


def movielens_load_preference_testset(fold):
    return pd.read_csv(os.path.join(movielens_clean_dir + '/' + str(fold), test_file))


def movielens_load_items():
    return pd.read_csv(os.path.join(movielens_clean_dir, movielens_items))


def movielens_load_data(fold):
    trainset_df = movielens_load_preference_trainset(fold)
    testset_df = movielens_load_preference_testset(fold)
    item_df = movielens_load_items()
    trainset_df = trainset_df.merge(item_df, on=item_label)
    testset_df = testset_df.merge(item_df, on=item_label)
    for col in (user_label, item_label):
        trainset_df[col] = trainset_df[col].astype('category')
        testset_df[col] = testset_df[col].astype('category')
    return trainset_df, testset_df, item_df


def movielens_load_full_data():
    rating_df = movielens_load_full_dataset()
    items_df = movielens_load_items()
    preferences_df = rating_df.merge(items_df, on=item_label)
    for col in (user_label, item_label):
        preferences_df[col] = preferences_df[col].astype('category')
    return preferences_df, items_df


# ################################################################# #
# One Million Songs Data
# ################################################################# #
def oms_load_full_preference():
    return pd.read_csv(os.path.join(oms_clean_dir, oms_rating))


def oms_load_preference_trainset(fold):
    return pd.read_csv(os.path.join(oms_clean_dir + str(fold), train_file))


def oms_load_preference_testset(fold):
    return pd.read_csv(os.path.join(oms_clean_dir + str(fold), test_file))


def oms_load_items():
    return pd.read_csv(os.path.join(oms_clean_dir, oms_item))


def oms_load_data(fold=1):
    trainset_df = oms_load_preference_trainset(fold)
    testset_df = oms_load_preference_testset(fold)
    item_df = oms_load_items()
    trainset_df = trainset_df.merge(item_df, on=item_label)
    testset_df = testset_df.merge(item_df, on=item_label)
    for col in (user_label, item_label):
        trainset_df[col] = trainset_df[col].astype('category')
        testset_df[col] = testset_df[col].astype('category')
    return trainset_df, testset_df, item_df


def oms_load_full_data():
    rating_df = oms_load_full_preference()
    items_df = oms_load_items()
    preferences_df = rating_df.merge(items_df, on=item_label)
    for col in (user_label, item_label):
        preferences_df[col] = preferences_df[col].astype('category')
    return preferences_df, items_df
