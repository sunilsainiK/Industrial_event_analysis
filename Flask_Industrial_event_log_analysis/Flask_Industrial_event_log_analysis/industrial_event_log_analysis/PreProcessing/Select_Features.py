from app import pd, session
def Select_Features(*col_name):
    col = col_name[0]
    print(col)
    df_data = pd.read_csv('C:/Users/DESUSAI/Desktop/Thesis/any.csv')

    df_1 = df_data[col]
    df_1.to_csv('df_raw',index=False)
    #df  = pd.DataFrame(col)
    selected_feature_df = df_1.head(50)
    return selected_feature_df.to_json()
