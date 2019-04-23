import pandas as pd
def Merge(*col_name):
    df_3 = pd.read_csv('df_raw')
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



    df_3 =df_3.drop(col_val,axis=1)
    Merge_df = df_3.head(50)
    df_3.to_csv('df_raw',index=False)
    return Merge_df.to_json()
