from src.config import item_label


def get_ap_from_list(relevance_array):
    relevance_list_size = len(relevance_array)
    if relevance_list_size == 0:
        return 0.0
    hit_list = []
    relevant = 0
    for i in range(relevance_list_size):
        if relevance_array[i]:
            relevant += 1
        hit_list.append(relevant / (i + 1))
    ap = sum(hit_list)
    if ap > 0.0:
        return ap / relevance_list_size
    else:
        return 0.0


def average_precision(reco_items_df, test_items_ids):
    # reco_items_df[item_label] = reco_items_df[item_label].astype(str)
    precision = [True if x in test_items_ids else False for x in reco_items_df[item_label].tolist()]
    #
    # if set(reco_items_df[item_label].tolist()) & set(test_items_ids):
    #     print('MAPPPPPPPPPPPPPPPPPPPPp')
    #     print(set(reco_items_df[item_label].tolist()) & set(test_items_ids))
    #     print('precision: ' + str(precision))
    return get_ap_from_list(precision)
