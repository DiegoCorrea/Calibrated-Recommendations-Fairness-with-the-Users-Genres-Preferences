def count_genres(row_df):
    count = 0
    for i, number in row_df.iteritems():
        if number > 0.0:
            count += 1
    return count / len(row_df)


def variance(row_df):
    return 1 - row_df.var()
