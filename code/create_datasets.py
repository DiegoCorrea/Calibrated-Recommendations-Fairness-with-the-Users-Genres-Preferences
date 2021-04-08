from preprocessing.clean_and_mining_data import oms_mining_data_and_create_folds, \
    movielens_mining_data_and_create_fold
from preprocessing.yahoo_dataset import YahooMovie

movielens_mining_data_and_create_fold()
oms_mining_data_and_create_folds()
ym = YahooMovie()
ym.create_clean_dataset()
