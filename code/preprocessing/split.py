import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from multiprocessing import Pool

from settings.config import user_label, TEST_SIZE, N_CORES, K_FOLDS_VALUES
from settings.language_strings import LANGUAGE_TOTAL_USERS, LANGUAGE_MERGE_PREFERENCES_INTO_DF

LOCAL_DF = None


def map_user_split(user_id):
    global LOCAL_DF
    df = LOCAL_DF[LOCAL_DF[user_label] == user_id].copy()
    train, test = train_test_split(df, test_size=TEST_SIZE)
    return (train, test)


def split_df(df):
    global LOCAL_DF
    LOCAL_DF = df
    users_ids = df[user_label].unique().tolist()
    print(LANGUAGE_TOTAL_USERS + ': ' + str(len(users_ids)))
    map_results_df = [map_user_split(user_id) for user_id in users_ids]

    print(LANGUAGE_MERGE_PREFERENCES_INTO_DF)
    list1 = [x[0] for x in map_results_df]
    list2 = [x[1] for x in map_results_df]
    train_results_df = pd.concat(list1, sort=False)
    test_results_df = pd.concat(list2, sort=False)
    return train_results_df, test_results_df


def kfold_split(user_df):
    kf = KFold(n_splits=K_FOLDS_VALUES)
    training = []
    testing = []
    for train, test in kf.split(user_df):
        training.append(user_df.iloc[train])
        testing.append(user_df.iloc[test])
    return (training, testing)


def cross_split(transactions_df):
    users_ids = transactions_df[user_label].unique().tolist()
    print(LANGUAGE_TOTAL_USERS + ': ' + str(len(users_ids)))
    grouped_by_user = [df_region for _, df_region in transactions_df.groupby(user_label)]
    pool = Pool(N_CORES)
    profiles_df = pool.map(kfold_split, grouped_by_user)
    pool.close()
    pool.join()
    training = [[] for _ in range(0, K_FOLDS_VALUES)]
    testing = [[] for _ in range(0, K_FOLDS_VALUES)]
    for train, test in profiles_df:
        for i in range(0, K_FOLDS_VALUES):
            training[i].append(train[i])
            testing[i].append(test[i])
    training_df = [[] for _ in range(0, K_FOLDS_VALUES)]
    testing_df = [[] for _ in range(0, K_FOLDS_VALUES)]
    for i in range(0, K_FOLDS_VALUES):
        training_df[i] = pd.concat(training[i], sort=False)
        testing_df[i] = pd.concat(testing[i], sort=False)
    return training_df, testing_df
