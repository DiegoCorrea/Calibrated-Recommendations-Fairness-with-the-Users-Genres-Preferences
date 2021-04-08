import os

import pandas as pd

from settings.config import DATASET_USAGE, movielens_clean_dir, movielens_rating, movielens_items, oms_item, oms_rating, \
    oms_clean_dir, yahoo_clean_dir, items_file, rating_file
from settings.language_strings import LANGUAGE_MOVIELENS_SELECTED, LANGUAGE_OMS_SELECTED
from preprocessing.clean_and_mining_data import oms_items_numbers, oms_preferences_numbers, \
    movielens_preferences_numbers, movielens_items_numbers
from preprocessing.yahoo_dataset import YahooMovie

if __name__ == '__main__':
    prefers_df = pd.DataFrame()
    items_df = pd.DataFrame()
    if DATASET_USAGE == 0:
        print(LANGUAGE_MOVIELENS_SELECTED)
        prefers_df = pd.read_csv(os.path.join(movielens_clean_dir, movielens_rating))
        items_df = pd.read_csv(os.path.join(movielens_clean_dir, movielens_items))
        movielens_preferences_numbers(prefers_df)
        movielens_items_numbers(items_df)
    elif DATASET_USAGE == 1:
        print(LANGUAGE_OMS_SELECTED)
        prefers_df = pd.read_csv(os.path.join(oms_clean_dir, oms_rating))
        items_df = pd.read_csv(os.path.join(oms_clean_dir, oms_item))
        oms_items_numbers(items_df)
        oms_preferences_numbers(prefers_df)
    else:
        print('Yahoo Movies')
        print('Raw')
        dataset = YahooMovie()
        dataset.load_raw_preference()
        dataset.load_raw_items()
        dataset.print_raw_data()
        print('*'*50)
        print('Clean')
        prefers_df = pd.read_csv(os.path.join(yahoo_clean_dir, rating_file))
        items_df = pd.read_csv(os.path.join(yahoo_clean_dir, items_file))
        movielens_preferences_numbers(prefers_df)
        movielens_items_numbers(items_df)
