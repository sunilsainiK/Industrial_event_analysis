from app import pd, session


class replace_null():
    def __init__(self, org_df):
        self.org_df = org_df
        self.int_df = org_df

    def Replace_null(org_df,*col_name, **kwargs):
        col = col_name[0]
        df_2 = org_df
        for i,values in col.items():
            if i=='col':
                print(values)
                col_val = values[0]
                print(col_val)
            if i== 'opti_text':
                print(values)
                replceing_val = values
                print(replceing_val)

        df_2[col_val].fillna(replceing_val, inplace = True)
        print(df_2.head())
        org_df = df_2
        replaced_null_df = org_df
        return replaced_null_df

def run(org_df,options=['mean','median','avg'],*col_name, **kwargs):
    result = replace_null.Replace_null(org_df,*col_name, **kwargs)
    print(result.head())
    return result
