from app import pd

class Precossing_Methods_class(object):
    """docstring for ."""

    def __init__(self, org_df):
        self.org_df = org_df
        self.int_df = org_df

    def Select_Features(self,*col_name):
        col = col_name[0]
        print(col)
        df_data = self.org_df
        self.int_df =  self.org_df[col]
        #df  = pd.DataFrame(col)
        selected_feature_df = self.int_df.head(50)
        return selected_feature_df.to_json()


def run(org_ef,*col):
    result = Precossing_Methods_class.Select_Features(org_ef,*col)
    return result.to_json()         
