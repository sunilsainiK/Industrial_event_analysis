from app import pd


class feature_selection():
    def __init__(self, org_df):
        self.org_df = org_df
        print('inside')
        self.int_df = org_df

    def Select_Features(org_df,*col_name):
        col = col_name[0]
        print(col)

        df_data = org_df[col]
        org_df = df_data

        #df  = pd.DataFrame(col)
        selected_feature_df = org_df
        return selected_feature_df


def run(org_df,*col):
    print(org_df.head())
    result = feature_selection.Select_Features(org_df,*col)
    print(result.head())
    return result
