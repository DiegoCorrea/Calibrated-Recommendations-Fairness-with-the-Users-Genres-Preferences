from code.config import HE_LABEL, CHI_LABEL, FAIRNESS_METRIC_LABEL
from code.posprocessing.distance_measures import compute_kullback_leibler, compute_person_chi_square, compute_hellinger
from code.posprocessing.distributions import compute_genre_distr_with_weigth


# ################################################################# #
# ###################### Linear Calibration ####################### #
# ################################################################# #
def linear_calibration(reco_items, interacted_distr, config, lmbda=0.5):
    """
    Our objective function for computing the utility score for
    the list of recommended items.

    lmbda : float, 0.0 ~ 1.0, default 0.5
        Lambda term controls the score and calibration tradeoff,
        the higher the lambda the higher the resulting recommendation
        will be calibrated. Lambda is keyword in Python, so it's
        lmbda instead ^^
    """
    reco_distr = compute_genre_distr_with_weigth(reco_items)

    div_value = 0.0
    if config[FAIRNESS_METRIC_LABEL] == CHI_LABEL:
        div_value = compute_person_chi_square(interacted_distr, reco_distr)
    elif config[FAIRNESS_METRIC_LABEL] == HE_LABEL:
        div_value = compute_hellinger(interacted_distr, reco_distr)
    else:
        div_value = compute_kullback_leibler(interacted_distr, reco_distr)

    total_score = 0.0
    for i_id, item in reco_items.items():
        total_score += item.score

    # kl divergence is the lower the better, while score is
    # the higher the better so remember to negate it in the calculation
    utility = (1 - lmbda) * total_score - lmbda * div_value
    return utility
