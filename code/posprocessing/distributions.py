from multiprocessing import Pool

import pandas as pd

from settings.config import user_label, N_CORES
from conversions.pandas_to_models import user_transactions_df_to_item_mapping

LOCAL_DF = None
LOCAL_ITEM_MAPPING = None


def compute_genre_distr_with_weigth(items):
    """Compute the genre distribution for a given list of Items."""
    distr = dict()
    weigth = dict()
    for item in items:
        item_class = items[item]
        item_weigth = item_class.score
        for genre, score in item_class.genres.items():
            genre_score = distr.get(genre, 0.)
            distr[genre] = genre_score + (score * item_weigth)
            weigth_rating = weigth.get(genre, 0.)
            weigth[genre] = weigth_rating + item_weigth

    for genre, genre_score in distr.items():
        w = genre_score / weigth[genre]
        normed_genre_score = round(w, 3)
        distr[genre] = normed_genre_score
    return distr


def compute_genre_distr(items):
    """Compute the genre distribution for a given list of Items."""
    distr = {}
    for item in items:
        for genre, score in item.genres.items():
            genre_score = distr.get(genre, 0.)
            distr[genre] = genre_score + score

    # we normalize the summed up probability so it sums up to 1
    # and round it to three decimal places, adding more precision
    # doesn't add much value and clutters the output
    for item, genre_score in distr.items():
        normed_genre_score = round(genre_score / len(items), 3)
        distr[item] = normed_genre_score

    return distr


def map_get_user_items(user_id):
    global LOCAL_DF, LOCAL_ITEM_MAPPING
    df = LOCAL_DF[LOCAL_DF[user_label] == user_id]
    items = user_transactions_df_to_item_mapping(df, LOCAL_ITEM_MAPPING)
    interacted_distr = compute_genre_distr_with_weigth(items)
    return pd.DataFrame(interacted_distr, index=[user_id])


def multiprocess_get_distribution(df, item_mapping):
    global LOCAL_DF, LOCAL_ITEM_MAPPING
    LOCAL_ITEM_MAPPING = item_mapping
    LOCAL_DF = df
    ids = df[user_label].unique().tolist()
    pool = Pool(N_CORES)
    map_results_df = pool.map(map_get_user_items, ids)
    pool.close()
    pool.join()
    result_df = pd.concat(map_results_df, sort=False)
    result_df.fillna(0.0, inplace=True)
    return result_df


def get_distribution(df, item_mapping):
    global LOCAL_DF, LOCAL_ITEM_MAPPING
    LOCAL_ITEM_MAPPING = item_mapping
    LOCAL_DF = df
    ids = df[user_label].unique().tolist()
    map_results_df = [map_get_user_items(user_id) for user_id in ids]
    result_df = pd.concat(map_results_df, sort=False)
    result_df.fillna(0.0, inplace=True)
    return result_df


def user_get_distribution(df, item_mapping):
    items = user_transactions_df_to_item_mapping(df, item_mapping)
    interacted_distr = compute_genre_distr_with_weigth(items)
    return interacted_distr
