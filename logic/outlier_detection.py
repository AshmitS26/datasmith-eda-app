import numpy as np
import pandas as pd
from scipy import stats


class DataOutlier:

    def get_numeric_columns(self, df):
        return df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    def detect_iqr(self, df, col):
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outliers = df[(df[col] < lower) | (df[col] > upper)]
        return outliers, lower, upper, Q1, Q3, IQR

    def detect_zscore(self, df, col, threshold=3.0):
        z_scores = np.abs(stats.zscore(df[col].dropna()))
        outlier_indices = df[col].dropna().index[z_scores > threshold]
        outliers = df.loc[outlier_indices]
        return outliers, outlier_indices

    def remove_iqr(self, df, col, lower, upper):
        return df[(df[col] >= lower) & (df[col] <= upper)]

    def remove_zscore(self, df, outlier_indices):
        return df.drop(index=outlier_indices)

    def cap_iqr(self, df, col, lower, upper):
        df[col] = df[col].clip(lower=lower, upper=upper)
        return df

    def cap_zscore(self, df, col, threshold):
        mean = df[col].mean()
        std = df[col].std()
        df[col] = df[col].clip(
            lower=mean - threshold * std,
            upper=mean + threshold * std
        )
        return df

    def get_outlier_percentage(self, outliers, df):
        return round(len(outliers) / len(df) * 100, 2)