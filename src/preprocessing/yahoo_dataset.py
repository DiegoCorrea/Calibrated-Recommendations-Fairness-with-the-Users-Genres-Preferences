from src.config import yahoo_raw_dir, yahoo_clean_dir, yahoo_raw_training_rating, yahoo_raw_testing_rating, user_label, \
    item_label, value_label, original_value_label, RATING_CUT_VALUE, rating_file, items_file, genre_label, title_label
import pandas as pd
import os

from src.preprocessing.clean_and_mining_data import cut_users, create_kfolds


class YahooMovie:
    def __init__(self, raw_path=yahoo_raw_dir, clean_path=yahoo_clean_dir):
        self.raw_path = raw_path
        self.clean_path = clean_path

        self.raw_testing_dt = None
        self.raw_training_dt = None
        self.raw_items_dt = None
        self.clean_items_dt = None

        self.full_raw_rating = None
        self.full_clean_rating = None

    def load_raw_preference(self):
        self.raw_training_dt = pd.read_csv(os.path.join(self.raw_path, yahoo_raw_training_rating),
                                           names=[user_label, item_label, original_value_label, value_label], sep='\t')
        self.raw_testing_dt = pd.read_csv(os.path.join(self.raw_path, yahoo_raw_testing_rating),
                                          names=[user_label, item_label, original_value_label, value_label], sep='\t')
        self.full_raw_rating = pd.concat([self.raw_training_dt, self.raw_testing_dt])
        self.full_raw_rating.drop([original_value_label], axis=1, inplace=True)

    def load_raw_items(self):
        item_path_file = os.path.join(self.raw_path, items_file)
        self.raw_items_dt = pd.read_csv(item_path_file, dtype=str)

    def link_movielens_and_yahoo(self):
        yahoo_items_dt = pd.read_csv(os.path.join(self.raw_path, "ydata-ymovies-mapping-to-movielens-v1_0.txt"),
                                     names=[item_label, title_label, "movieId"], sep='\t', encoding='ISO-8859-1',
                                     dtype=str)
        yahoo_items_dt.drop([title_label], axis=1, inplace=True)
        yahoo_items_dt.dropna(inplace=True)

        self.clean_items_dt = pd.merge(yahoo_items_dt, self.raw_items_dt,
                                       how='left', left_on="movieId", right_on="movieId"
                                       )
        self.clean_items_dt = self.clean_items_dt.drop(["movieId"], axis=1)

    def preprocessing_and_save_data(self):
        self.clean_items_dt = self.clean_items_dt[self.clean_items_dt[genre_label] != '(no genres listed)']
        self.clean_items_dt.dropna(inplace=True)

        self.full_raw_rating = self.full_raw_rating[self.full_raw_rating[item_label].isin(
            self.clean_items_dt[item_label].tolist())]
        self.full_raw_rating = self.full_raw_rating[self.full_raw_rating[value_label] >= RATING_CUT_VALUE].copy()
        self.full_clean_rating = cut_users(self.full_raw_rating)

        self.full_clean_rating[item_label] = self.full_clean_rating[item_label].astype(str)
        self.clean_items_dt = self.clean_items_dt[self.clean_items_dt[item_label].isin(
            self.full_clean_rating[item_label].unique().tolist())]

        if not os.path.exists(self.clean_path):
            os.makedirs(self.clean_path)
        self.full_clean_rating.to_csv(os.path.join(self.clean_path, rating_file),
                                      index=False, encoding='UTF-8')
        self.clean_items_dt.to_csv(os.path.join(self.clean_path, items_file),
                                   index=False, encoding='UTF-8')

    def create_clean_dataset(self):
        self.load_raw_preference()
        self.load_raw_items()
        self.link_movielens_and_yahoo()
        self.preprocessing_and_save_data()
        create_kfolds(self.full_clean_rating, self.clean_path)

    def print_raw_data(self):
        print("Users: ", int(self.full_raw_rating[user_label].nunique()))
        print("Preferences: ", len(self.full_raw_rating))
        print("Items: ", int(self.full_raw_rating[item_label].nunique()))
