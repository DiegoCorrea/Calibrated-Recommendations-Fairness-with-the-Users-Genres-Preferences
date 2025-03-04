import multiprocessing

from .language_strings import lang

DATASET_USAGE = 2  # 0 Movielens... 1 One Million Songs... 2 Yahoo Movie
K_FOLDS_VALUES = 5
N_CORES = multiprocessing.cpu_count()
RECOMMENDATION_LIST_SIZE = 10
TEST_SIZE = 0.3
PROFILE_LEN_CUT_VALUE = 50
CANDIDATES_LIST_SIZE = 100
RATING_CUT_VALUE = 4.0
ALPHA_VALUE = 0.01
TIME_LIMIT = 300
K_NEIGHBOR = 30

# General Data Set variables
title_label = 'title'
genre_label = 'genres'
user_label = 'userId'
item_label = 'itemId'
value_label = 'rating'
time_label = 'timestamp'
est_label = 'est'
order_label = 'order'
original_value_label = 'original_rating'

train_file = 'train.csv'
test_file = 'test.csv'
rating_file = 'rating.csv'
items_file = 'movie.csv'

# ######################### #
#    Movielens Variables    #
# ######################### #

# Movielens config variables
movielens_rating_col_names = [user_label, item_label, value_label, time_label]
item_col_names = [title_label, genre_label]

# Data Set and Results Directory and Files
movielens_results_dir = 'movielens-20m-dataset/'
movielens_raw_dir = "../data/raw/movielens-20m-dataset/"
movielens_clean_dir = "../data/clean/movielens-20m-dataset/"
movielens_rating = 'rating.csv'
movielens_rating_dat = 'ratings.dat'
movielens_items = 'movie.csv'
movielens_items_dat = 'movies.dat'

# ######################### #
#      Yahoo Variables      #
# ######################### #
yahoo_raw_dir = "../data/raw/yahoo-movie/"
yahoo_clean_dir = "../data/clean/yahoo-movie/"
yahoo_raw_training_rating = "ydata-ymovies-user-movie-ratings-train-v1_0.txt"
yahoo_raw_testing_rating = "ydata-ymovies-user-movie-ratings-test-v1_0.txt"
yahoo_results_dir = 'yahoo-movie/'

# ######################### #
#       OMS Variables       #
# ######################### #

# Data Set and Results Directory and Files
oms_results_dir = 'oms/'
oms_raw_dir = "../data/raw/oms/"
oms_clean_dir = "../data/clean/oms/"
oms_rating = 'train_triplets.txt'
oms_genre = 'msd_tagtraum_cd2.cls'
oms_item = 'songs.csv'

# Data Set Variables
artist_label = 'artist'
album_label = 'album'
year_label = 'year'
track_label = 'track_id'
majority_genre = 'majority-genre'
minority_genre = 'minority-genre'

# ######################### #
#    Graphics Variables     #
# ######################### #
# DataFrame Label
total_times = 'total_times'
profile_size = 'profile_size'
number_popular_items = 'nPopular'
number_unpopular_items = 'nUnPopular'
percentage_popular = 'percentage_popular'
percentage_unpopular = 'percentage_unpopular'
number_of_genres = "nGenre"
group_of_users = "gUsers"

# Colors, Hatch
color_list = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray',
              'tab:olive', 'tab:cyan', '#0F0F0F0F']
niche_graph_color = 'tab:blue'
focused_graph_color = 'tab:cyan'
diverse_graph_color = 'tab:olive'
popularity_graph_color = 'tab:purple'

# Markers
markers_list = ['o', '^', 's', 'D', 'x', 'p', '.', '1', '|', '*', '2']

# Line Style
line_style_list = [':', '--', ':', '-', '-', '-', '--', ':', '--', '-.', '-.']

# Constant Values
FONT_SIZE_VALUE = 16
BAR_WIDTH_VALUE = 0.25
DPI_VALUE = 300
QUALITY_VALUE = 100

# ######################### #
#   Algorithms Variables    #
# ######################### #
# Structure Labels
USERKNN_LABEL = 'USERKNN'
ITEMKNN_LABEL = 'ITEMKNN'
SVD_LABEL = 'SVD'
SVDpp_LABEL = 'SVDpp'
NMF_LABEL = 'NMF'
SLOPE_LABEL = 'SLOPE'

reco_popularity_label = "reco_popularity"
normalized_reco_popu_label = 'normalized_reco_popularity'
preference_popularity_label = "preference_popularity"
normalized_preference_popu_label = 'normalized_preference_popularity'

# Print Language Variables
USERKNN_PRINT = 'UserKNN'
ITEMKNN_PRINT = 'ItemKNN'
SVD_PRINT = 'SVD'
SVDpp_PRINT = 'SVD++'
NMF_PRINT = 'NMF'
SLOPE_PRINT = 'Slope One'

# List of Strings
LANGUAGE_ALGORITHM_list = [USERKNN_PRINT, ITEMKNN_PRINT, SVD_PRINT,
                           SVDpp_PRINT,
                           NMF_PRINT, SLOPE_PRINT]

# ######################### #
#    Evaluate Variables     #
# ######################### #
# Structure Labels
algorithm_label = 'algorithm'
algorithms_label = 'algorithms'
mae_label = 'mae'
mse_label = 'mse'
rmse_label = 'rmse'
MACE_LABEL = 'MACE'
MAP_LABEL = 'MAP'
MRR_LABEL = 'MRR'
MC_LABEL = 'MC'

#
at_label = "at_"

# List of Strings
error_list_label = [mae_label, mse_label, rmse_label]

FAIRNESS_METRIC_LABEL = 'FAIRNESS_METRIC'
FIXED_LABEL = 'FIXED'
LAMBDA_LABEL = 'LAMBDA'
LAMBDA_VALUE_LABEL = 'LAMBDA_VALUE'
EVALUATION_METRIC_LABEL = 'EVALUATION_METRIC'
EVALUATION_VALUE_LABEL = 'EVALUATION_VALUE'

evaluation_label = [algorithm_label, FAIRNESS_METRIC_LABEL, LAMBDA_LABEL, LAMBDA_VALUE_LABEL, EVALUATION_METRIC_LABEL,
                    EVALUATION_VALUE_LABEL]


def dataset_to_use():
    results_path = '../results/analytics/' + lang + '/'
    if DATASET_USAGE == 0:
        results_path = results_path + movielens_results_dir
    elif DATASET_USAGE == 1:
        results_path = results_path + oms_results_dir
    else:
        results_path = results_path + yahoo_results_dir
    return results_path


def baselines_dataset():
    results_path = '../results/baselines/' + lang + '/'
    if DATASET_USAGE == 0:
        results_path = results_path + movielens_results_dir
    elif DATASET_USAGE == 1:
        results_path = results_path + oms_results_dir
    else:
        results_path = results_path + yahoo_results_dir
    return results_path


def postprocessing_results():
    results_path = '../results/postprocessing/' + lang + '/'
    if DATASET_USAGE == 0:
        results_path = results_path + movielens_results_dir
    elif DATASET_USAGE == 1:
        results_path = results_path + oms_results_dir
    else:
        results_path = results_path + yahoo_results_dir
    return results_path


def data_results():
    results_path = '../results/data/' + lang + '/'
    if DATASET_USAGE == 0:
        results_path = results_path + movielens_results_dir
    elif DATASET_USAGE == 1:
        results_path = results_path + oms_results_dir
    else:
        results_path = results_path + yahoo_results_dir
    return results_path


results_path = data_results()
analytics_results_path = dataset_to_use()
baselines_results_path = baselines_dataset()
postprocessing_results_path = postprocessing_results()

# ####################################### #
#    Config Post Processing Variables     #
# ####################################### #
FAIRNESS_METRIC_LABEL = 'FAIRNESS_METRIC'
KL_LABEL = 'KL'
HE_LABEL = 'HE'
CHI_LABEL = 'CHI'

GREEDY_ALGORITHM_LABEL = 'GREEDY_ALGORITHM'
SURROGATE_LABEL = 'SURROGATE'

TRADE_OFF_LABEL = 'TRADE_OFF'
COUNT_GENRES_TRADE_OFF_LABEL = 'COUNT_GENRES'
SUN_GENRES_PROBABILITY_TRADE_OFF_LABEL = 'SUN_GENRES_PROBABILITY'
VARIANCE_TRADE_OFF_LABEL = 'VARIANCE'
MANUAL_VALUE_LABEL = 'MANUAL_VALUE'

CALIBRATION_LABEL = 'CALIBRATION'
LINEAR_CALIBRATION_LABEL = 'LINEAR_CALIBRATION'
LOGARITHMIC_CALIBRATION_LABEL = 'LOGARITHMIC_CALIBRATION'

FIXED_LAMBDA_LABEL = 'FIXED_LAMBDA_LABEL'
PERSON_LAMBDA_LABEL = 'PERSON_LAMBDA_LABEL'
