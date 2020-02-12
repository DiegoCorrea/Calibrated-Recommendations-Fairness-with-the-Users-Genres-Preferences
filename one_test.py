import pandas as pd
from surprise import SVD

from src.conversions.pandas_to_models import transform_trainset, transform_testset
from src.preprocessing.load_database import movielens_load_data

trainset_df, testset_df, items_df = movielens_load_data(1)

trainset = transform_trainset(trainset_df)

trainset_df.sort_values(by='userId')
users_ids_list = trainset_df['userId'].unique().tolist()[:3]

# instance = NMF()
instance = SVD(random_state=42)
instance.fit(trainset)

for user_id in users_ids_list:
    print(user_id)
    user_trainset_df = trainset_df[trainset_df['userId'] == user_id]

    all_items_ids = items_df['itemId'].unique().tolist()
    know_items = user_trainset_df['itemId'].unique().tolist()
    unknow_items = set(all_items_ids) - set(know_items)
    data = {'itemId': list(unknow_items)}
    user_testset = pd.DataFrame.from_dict(data)
    user_testset['userId'] = user_id
    user_testset['rating'] = 0.0
    print(user_testset)
    # candidates_items_prediction = [instance.predict(user_id, item_id) for item_id in list(unknow_items)]
    candidates_items_prediction = instance.test(transform_testset(user_testset))
    print(candidates_items_prediction[:10])
