from copy import deepcopy

import numpy as np

from settings.config import RECOMMENDATION_LIST_SIZE
from posprocessing.calibrated_methods import linear_calibration


# ################################################################# #
# ############### Surrogate Submodular Optimization ############### #
# ################################################################# #
def surrogate_submodular(user_preference_distribution, reco_items, config, n=RECOMMENDATION_LIST_SIZE,
                         lmbda=0.5):
    """
    start with an empty recommendation list,
    loop over the topn cardinality, during each iteration
    update the list with the item that maximizes the utility function.
    """
    calib_reco_dict = {}
    for _ in range(n):
        max_utility = -np.inf
        best_item = None
        best_id = None
        for i_id, item in reco_items.items():
            if i_id in calib_reco_dict.keys():
                continue
            temp = deepcopy(calib_reco_dict)
            temp[i_id] = item

            utility = linear_calibration(temp, user_preference_distribution, config, lmbda)

            if utility > max_utility:
                max_utility = utility
                best_item = item
                best_id = i_id
        calib_reco_dict[best_id] = best_item
    return calib_reco_dict
