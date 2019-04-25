import pandas as pd


class Merge():
    def __init__(self, org_df):
        self.org_df = org_df
        self.int_df = org_df

    def merge(org_df,*col_name):
        df_3 = org_df
        col = col_name[1]
        print(len(col))
        for i,values in col.items():
            if i=='col':
                col_val = values
                print(col_val)
            if i== 'opti_text':
                print(values)
                Merge_value = values
                print(Merge_value)


        for j in range(len(col_val)):
            print(j,col_val)
            if j==0:
                df_3[Merge_value] = df_3[col_val[j]].map(str)

                print(df_3.head())
            else:
                df_3[Merge_value] = df_3[Merge_value]+"___ " + df_3[col_val[j]].map(str)
                print(df_3[Merge_value])
        print(col_val)
        Merge_df =df_3.drop(col_val,axis=1)
        

        return Merge_df


def run(org_df,*col_name):
    result = Merge.merge(org_df,*col_name)
    return result
