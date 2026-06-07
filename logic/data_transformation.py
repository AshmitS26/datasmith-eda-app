import pandas as pd
from sklearn.preprocessing import LabelEncoder


class DataTransformer:

    def get_categorical_columns(self, df):
        return df.select_dtypes(include=['object', 'category']).columns.tolist()

    def get_all_columns(self, df):
        return df.columns.tolist()

    def get_numeric_columns(self, df):
        return df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    def label_encode(self, df, col):
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        return df

    def one_hot_encode(self, df, col, drop_first=True):
        df = pd.get_dummies(df, columns=[col], drop_first=drop_first)
        return df

    def ordinal_encode(self, df, col, order_list):
        order_map = {val: idx for idx, val in enumerate(order_list)}
        df[col] = df[col].map(order_map)
        return df, order_map

    def convert_dtype(self, df, col, target_dtype):
        df[col] = df[col].astype(target_dtype)
        return df

    def rename_column(self, df, old_name, new_name):
        return df.rename(columns={old_name: new_name})

    def drop_columns(self, df, cols):
        return df.drop(columns=cols)