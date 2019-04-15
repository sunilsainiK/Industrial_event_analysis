from app import pd
def Select_Features(*col_name):
    print(type(col_name))
    col = col_name[0]
    df  = pd.DataFrame(col)
    print(df)
    return 'hi'
