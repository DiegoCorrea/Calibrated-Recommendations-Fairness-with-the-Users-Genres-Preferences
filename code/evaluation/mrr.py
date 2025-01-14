from settings.config import item_label


def get_rr_from_list(relevance_array):
    relevance_list_size = len(relevance_array)
    if relevance_list_size == 0:
        return 0.0
    for i in range(relevance_list_size):
        if relevance_array[i]:
            return 1 / (i + 1)
    return 0.0


def mrr(reco_items_df, test_items_ids):
    # for x in reco_items_df[item_label].tolist():
    #     for y in test_items_ids:
    #         if int(x) == int(y):
    #             print('int int int int')
    #         if str(x) == str(y):
    #             print('str  str str str str')
    precision = [True if x in test_items_ids else False for x in reco_items_df[item_label].tolist()]
    # if True in precision:
    #     print('MMMMRRRRRRRRRRRRRRRRRRRR')
    #     print(set(reco_items_df[item_label].tolist()) & set(test_items_ids))
    return get_rr_from_list(precision)
