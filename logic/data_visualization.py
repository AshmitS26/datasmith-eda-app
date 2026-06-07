import pandas as pd
import numpy as np


class DataVisualization:

    def get_numeric_columns(self, df):
        return df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    def get_categorical_columns(self, df):
        return df.select_dtypes(include=['object', 'category']).columns.tolist()

    def get_all_columns(self, df):
        return df.columns.tolist()

    def get_distribution_stats(self, df, col):
        data = df[col].dropna()
        return {
            "skewness": round(data.skew(), 4),
            "kurtosis": round(data.kurtosis(), 4),
            "std": round(data.std(), 4),
            "data": data.tolist()
        }

    def get_bar_data(self, df, x_col, y_col, agg_method):
        return df.groupby(x_col)[y_col].agg(agg_method).reset_index()

    def get_pie_data(self, df, col, top_n=15):
        pie_data = df[col].value_counts().reset_index()
        pie_data.columns = [col, "Count"]
        truncated = len(pie_data) > top_n
        return pie_data.head(top_n), truncated

    def get_surface_data(self, df):
        numeric_cols = self.get_numeric_columns(df)
        corr = df[numeric_cols].corr().values
        return corr, numeric_cols