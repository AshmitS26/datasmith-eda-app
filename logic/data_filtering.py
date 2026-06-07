import pandas as pd


class DataFilter:

    def filter_numeric(self, df, col, min_val, max_val):
        return df[(df[col] >= min_val) & (df[col] <= max_val)]

    def filter_categorical(self, df, col, selected_vals):
        return df[df[col].isin(selected_vals)]

    def filter_date(self, df, col, start_date, end_date):
        df[col] = pd.to_datetime(df[col])
        return df[
            (df[col].dt.date >= start_date) &
            (df[col].dt.date <= end_date)
        ]

    def search_all_columns(self, df, search_term):
        mask = df.astype(str).apply(
            lambda col: col.str.contains(search_term, case=False, na=False)
        ).any(axis=1)
        return df[mask]

    def get_numeric_columns(self, df):
        return df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    def get_categorical_columns(self, df):
        return df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()

    def get_date_columns(self, df):
        date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        possible = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
        return list(set(date_cols + possible))
    