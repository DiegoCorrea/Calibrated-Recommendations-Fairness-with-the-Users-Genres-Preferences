import os
from multiprocessing import Pool

import numpy as np
import pandas as pd

from code.config import (movielens_raw_dir, movielens_rating, value_label, PROFILE_LEN_CUT_VALUE,
                         movielens_clean_dir, movielens_items, oms_raw_dir, oms_rating, item_label, track_label,
                         title_label, artist_label, oms_genre, majority_genre, minority_genre, oms_clean_dir, oms_item,
                         album_label, year_label, genre_label, user_label, N_CORES, K_FOLDS_VALUES, RATING_CUT_VALUE,
                         train_file, test_file, time_label, rating_file, movielens_rating_dat, movielens_items_dat)
from code.language_strings import LANGUAGE_CREATING_FOLDS, LANGUAGE_MINING_PREFERENCES, LANGUAGE_SAVE_TEST, \
    LANGUAGE_SAVE_TRAIN, LANGUAGE_SPLIT_DATA, LANGUAGE_FOLD, LANGUAGE_MINING_ITEMS, LANGUAGE_OMS_SELECTED, \
    LANGUAGE_MOVIELENS_SELECTED
from code.preprocessing.split import split_df, cross_split

GLOBAL_preferences_df = None


def create_kfolds(preferences_df, clean_dir):
    trainset_df, testset_df = cross_split(preferences_df)
    for k in range(0, K_FOLDS_VALUES):
        print(LANGUAGE_FOLD + ': ' + str(k))
        print(LANGUAGE_SPLIT_DATA)
        fold_dir = clean_dir + '/' + str(k)
        if not os.path.exists(fold_dir):
            os.makedirs(fold_dir)
        print(LANGUAGE_SAVE_TRAIN)
        rating_path = os.path.join(fold_dir, train_file)
        trainset_df[k].to_csv(rating_path, index=False)
        print(LANGUAGE_SAVE_TEST)
        rating_path = os.path.join(fold_dir, test_file)
        testset_df[k].to_csv(rating_path, index=False)


def create_folds(preferences_df, clean_dir):
    for k in range(0, K_FOLDS_VALUES):
        print(LANGUAGE_FOLD + ': ' + str(k))
        print(LANGUAGE_SPLIT_DATA)
        trainset_df, testset_df = split_df(preferences_df)
        fold_dir = clean_dir + '/' + str(k)
        if not os.path.exists(fold_dir):
            os.makedirs(fold_dir)
        print(LANGUAGE_SAVE_TRAIN)
        rating_path = os.path.join(fold_dir, train_file)
        trainset_df.to_csv(rating_path, index=False)
        print(LANGUAGE_SAVE_TEST)
        rating_path = os.path.join(fold_dir, test_file)
        testset_df.to_csv(rating_path, index=False)


def cut_users(df):
    user_counts = df[user_label].value_counts()
    return df[df[user_label].isin([k for k, v in user_counts.items() if v >= PROFILE_LEN_CUT_VALUE])].copy()


# ################################################################# #
# Movielens Data
# ################################################################# #

def movielens_preferences_numbers(preference_df):
    print("Users: ", int(preference_df[user_label].nunique()))
    print("Preferences: ", len(preference_df))


def movielens_items_numbers(item_df):
    print("Items: ", int(item_df[item_label].nunique()))
    vec = item_df[genre_label].tolist()
    genres = []
    for item_genre in vec:
        splitted = item_genre.split('|')
        genre_list = [genre for genre in splitted]
        genres = genres + genre_list
    print("Genres: ", int(len(list(set(genres)))))


def mining_movielens_preference_set(item_df):
    rating_path = os.path.join(movielens_raw_dir, movielens_rating_dat)
    df_raw_ratings = pd.read_csv(rating_path, sep="::", engine='python', names=[user_label, item_label, value_label, time_label])
    df_raw_ratings.drop([time_label], axis=1, inplace=True)
    # df_raw_ratings.rename(columns={"movieId": item_label}, inplace=True)
    # df_raw_ratings[[value_label]] = df_raw_ratings[[value_label]].fillna('')
    #
    movielens_preferences_numbers(df_raw_ratings)
    #
    df_raw_ratings = df_raw_ratings[df_raw_ratings[item_label].isin(
        item_df[item_label].tolist())]
    df_rating = df_raw_ratings[df_raw_ratings[value_label] >= RATING_CUT_VALUE].copy()
    preferences_df = cut_users(df_rating)

    item_df = item_df[item_df[item_label].isin(
        df_rating[item_label].tolist())]
    if not os.path.exists(movielens_clean_dir):
        os.makedirs(movielens_clean_dir)
    preferences_df.to_csv(os.path.join(movielens_clean_dir, movielens_rating),
                          index=False)
    rating_path = os.path.join(movielens_clean_dir, movielens_items)
    item_df.to_csv(rating_path, index=False)
    movielens_preferences_numbers(preferences_df)
    return preferences_df, item_df


def mining_movielens_items():
    item_path_file = os.path.join(movielens_raw_dir, movielens_items_dat)
    item_df = pd.read_csv(item_path_file, sep="::", names=[item_label, title_label, genre_label], engine='python')
    # item_df.rename(columns={"movieId": item_label}, inplace=True)
    #
    movielens_items_numbers(item_df)
    #
    item_df = item_df[item_df[genre_label] != '(no genres listed)']
    if not os.path.exists(movielens_clean_dir):
        os.makedirs(movielens_clean_dir)
    rating_path = os.path.join(movielens_clean_dir, movielens_items)
    item_df.to_csv(rating_path, index=False)
    return item_df


def movielens_mining_data_and_create_fold():
    print(LANGUAGE_MOVIELENS_SELECTED)
    print(LANGUAGE_MINING_PREFERENCES)
    print(LANGUAGE_MINING_ITEMS)
    item_df = mining_movielens_items()
    preferences_df, item_df = mining_movielens_preference_set(item_df)
    print(LANGUAGE_CREATING_FOLDS)
    # create_folds(preferences_df, movielens_clean_dir)
    create_kfolds(preferences_df, movielens_clean_dir)
    movielens_preferences_numbers(preferences_df)
    movielens_items_numbers(item_df)


# ################################################################# #
# One Million Songs Data
# ################################################################# #
count = 0
Global_item_ds = None


def map_get_user_item(user):
    global GLOBAL_preferences_df
    user_df = GLOBAL_preferences_df[GLOBAL_preferences_df[user_label] == user]
    quartil = user_df[value_label].quantile(q=0.6)
    return user_df[user_df[value_label] >= quartil]


def oms_preference_filter(raw_ratings_df):
    global GLOBAL_preferences_df
    GLOBAL_preferences_df = raw_ratings_df
    unique_users = raw_ratings_df[user_label].unique().tolist()
    pool = Pool(N_CORES)
    profiles_df = pool.map(map_get_user_item, unique_users)
    pool.close()
    pool.join()
    profiles_df = pd.concat(profiles_df, sort=False)
    return profiles_df


def isin_parallel_map(raw_ratings_df):
    global Global_item_ds
    return raw_ratings_df[
        raw_ratings_df[item_label].isin(Global_item_ds)
    ]


def isin_parallel(raw_ratings_df, items_ids):
    # splits = np.array_split(raw_ratings_df, N_CORES)
    # print(splits)
    # pool = Pool(N_CORES)
    # profiles_df = pool.map(isin_parallel_map, splits)
    # pool.close()
    # pool.join()
    # profiles_df = pd.concat(profiles_df, sort=False)
    profiles_df = raw_ratings_df[
        raw_ratings_df[item_label].isin(items_ids)
    ]
    return profiles_df


def mining_oms_preference_set(item_df):
    rating_file_path = os.path.join(oms_raw_dir, oms_rating)
    raw_ratings_df = pd.read_csv(rating_file_path,
                                 names=[user_label, item_label, value_label], sep='\t')
    raw_ratings_df.rename(columns={"movieId": item_label}, inplace=True)
    oms_preferences_numbers(raw_ratings_df)
    ratings_filter_itens_df = isin_parallel(raw_ratings_df, item_df[item_label].tolist())
    # ratings_df = oms_preference_filter(ratings_df)
    ratings_df = cut_users(ratings_filter_itens_df)
    if not os.path.exists(oms_clean_dir):
        os.makedirs(oms_clean_dir)
    rating_file_path = os.path.join(oms_clean_dir, oms_rating)
    ratings_df.to_csv(rating_file_path, index=False)
    items_ids = ratings_df[item_label].unique()
    new_item_df = item_df[
        item_df[item_label].isin(items_ids)
    ]
    oms_preferences_numbers(ratings_df)
    item_path_file = os.path.join(oms_clean_dir, oms_item)
    new_item_df.to_csv(item_path_file, index=False)
    return ratings_df, new_item_df


def load_raw_track():
    song_by_track_df = pd.read_csv(oms_raw_dir + 'unique_tracks.txt', engine='python',
                                   sep='<SEP>', names=[track_label, item_label, title_label, artist_label])
    return song_by_track_df.drop([title_label, artist_label], axis=1)


def load_raw_gender():
    return pd.read_csv(oms_raw_dir + oms_genre,
                       sep='\t', names=[track_label, majority_genre, minority_genre], na_values=' ')


def oms_filter_columns(item_df):
    item_df = item_df.replace(np.nan, '', regex=True)
    item_df[genre_label] = item_df.apply(
        lambda r: r[majority_genre] + '|' + r[minority_genre] if r[minority_genre] != '' else r[majority_genre], axis=1)
    item_df.drop([artist_label, album_label, year_label, majority_genre, minority_genre], inplace=True, axis=1)
    return item_df


def mining_oms_items():
    item_path_file = os.path.join(oms_raw_dir, oms_item)
    item_df = pd.read_csv(item_path_file, names=[item_label, title_label, artist_label, album_label, year_label])
    item_df.drop_duplicates([item_label], inplace=True)
    item_df = pd.merge(
        pd.merge(item_df, load_raw_track(),
                 how='left', left_on=item_label, right_on=item_label
                 ),
        load_raw_gender(), how='inner', left_on=track_label, right_on=track_label
    )
    item_df.drop_duplicates([item_label], inplace=True)
    item_df.set_index(track_label, inplace=True, drop=True)
    if not os.path.exists(oms_clean_dir):
        os.makedirs(oms_clean_dir)
    item_path_file = os.path.join(oms_clean_dir, oms_item)
    item_df = oms_filter_columns(item_df)
    item_df.to_csv(item_path_file, index=False)
    print("#" * 30)
    oms_items_numbers(item_df)
    return item_df


def oms_preferences_numbers(preference_df):
    print("Users: ", int(preference_df[user_label].nunique()))
    print("Preferences: ", len(preference_df))


def oms_items_numbers(item_df):
    print("Items: ", int(item_df[item_label].nunique()))
    vec = item_df[genre_label].tolist()
    genres = []
    for item_genre in vec:
        splitted = item_genre.split('|')
        genre_list = [genre for genre in splitted]
        genres = genres + genre_list
    print("Genres: ", int(len(list(set(genres)))))


def oms_mining_data_and_create_folds():
    print(LANGUAGE_OMS_SELECTED)
    print(LANGUAGE_MINING_ITEMS)
    items_df = mining_oms_items()
    print(LANGUAGE_MINING_PREFERENCES)
    preferences_df, new_item_df = mining_oms_preference_set(items_df)
    oms_items_numbers(new_item_df)
    print(LANGUAGE_CREATING_FOLDS)
    create_folds(preferences_df, oms_clean_dir)
