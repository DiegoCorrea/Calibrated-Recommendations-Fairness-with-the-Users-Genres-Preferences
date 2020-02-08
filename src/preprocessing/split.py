import pandas as pd
from sklearn.model_selection import train_test_split

from src.config import user_label, TEST_SIZE
from src.language_strings import LANGUAGE_TOTAL_USERS, LANGUAGE_MERGE_PREFERENCES_INTO_DF

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
