from app import pd, session
def Replace_null(options=['mean','median','avg'],*col_name, **kwargs):
    col = col_name[0]
    df_2 = pd.read_csv('df_raw')
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
    df_2.to_csv('df_raw',index=False)
    replaced_null_df = df_2.head(50)
    return replaced_null_df.to_json()
