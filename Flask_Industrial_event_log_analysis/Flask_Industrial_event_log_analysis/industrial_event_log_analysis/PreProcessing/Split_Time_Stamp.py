from app import pd
def Split_Time_Stamp(options=['Hours','Quater','Day','Month'],*col_name, **kwargs):
    print(col_name)
    print(kwargs)
    df_4 = pd.read_csv('df_raw')
    print(col_name)
    col = col_name[0]
    print(len(col))
    for i,values in col.items():
        print(i,values)
        if i=='col':
            col_val = values[0]
            print(col_val)
        if i== 'opti_text':
            bucketName_value = values
            print(bucketName_value)
        if  i== 'opt':
            opt_value = values
            print(opt_value)



    if (opt_value=='hour'):
        bucket='<M8[h]'
    if (opt_value=='Day'):
        bucket='<M8[D]'
    if (opt_value=='sec'):
        bucket='<M8[s]'

    df_4[col_val] =  pd.to_datetime(df_4[col_val])

    df_4.index = df_4[col_val]

    df_4[bucketName_value] = df_4[col_val].values.astype(bucket)
    print(df_4.head())

    return df_4.to_json()
