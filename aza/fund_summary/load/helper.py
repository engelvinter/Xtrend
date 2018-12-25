from pandas import to_numeric


def replace_all_slashes(df, column_name):
    func = lambda str: str.replace("/", "_")
    df[column_name] = df[column_name].map(func)
    return df


def convert_col_to_percent(df, column_name):
    if df[column_name].dtype == "O":  # Object column
        # The column may contain '-' and consists of strings
        # remove all "-" (no value) in column and make a copy
        # containing only funds which has made more than a year.
        df = df[df[column_name] != '-'].copy()
        # Convert the column to numeric
        df[column_name] = to_numeric(df[column_name])

    # Divide by 100 to get 0.00 - 1.00
    df[column_name] = df[column_name].div(100)

    return df


def remove_duplicates(df):
    return df[~df.index.duplicated()]