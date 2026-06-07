import pandas as pd


class DataCleaner:

    def __init__(self):
        self.last_action = None

    def fill_mean(self, df, col):
        fill_val = round(df[col].mean(), 2)
        df[col] = df[col].fillna(fill_val)
        self.last_action = f"Filled '{col}' with Mean ({fill_val})"
        return df

    def fill_median(self, df, col):
        fill_val = round(df[col].median(), 2)
        df[col] = df[col].fillna(fill_val)
        self.last_action = f"Filled '{col}' with Median ({fill_val})"
        return df

    def fill_mode(self, df, col):
        fill_val = df[col].mode()[0]
        df[col] = df[col].fillna(fill_val)
        self.last_action = f"Filled '{col}' with Mode ({fill_val})"
        return df

    def fill_forward(self, df, col):
        df[col] = df[col].ffill()
        self.last_action = f"Applied Forward Fill on '{col}'"
        return df

    def fill_backward(self, df, col):
        df[col] = df[col].bfill()
        self.last_action = f"Applied Backward Fill on '{col}'"
        return df

    def fill_custom(self, df, col, value):
        df[col] = df[col].fillna(value)
        self.last_action = f"Filled '{col}' with custom value '{value}'"
        return df

    def remove_missing_rows(self, df, col):
        df = df.dropna(subset=[col])
        self.last_action = f"Removed rows with missing values in '{col}'"
        return df

    def remove_duplicates(self, df):
        count = df.duplicated().sum()
        df = df.drop_duplicates()
        self.last_action = f"Removed {count} duplicate rows"
        return df

    def get_missing_cols(self, df):
        return df.columns[df.isnull().any()].tolist()

    def get_duplicate_count(self, df):
        return df.duplicated().sum()