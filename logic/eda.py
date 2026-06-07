import pandas as pd


class DataEDA:

    def get_missing_stats(self, df):
        return pd.DataFrame({
            "Column": df.columns,
            "Missing Count": df.isnull().sum().values,
            "Missing %": (df.isnull().sum().values / len(df) * 100).round(2)
        }).sort_values("Missing Count", ascending=False)

    def get_unique_stats(self, df):
        return pd.DataFrame({
            "Column": df.columns,
            "Unique Count": df.nunique().values,
            "Unique %": (df.nunique().values / len(df) * 100).round(2)
        }).sort_values("Unique Count", ascending=False)

    def get_descriptive_stats(self, df):
        return df.describe().round(2)

    def get_total_missing(self, df):
        return df.isnull().sum().sum()

    def get_missing_col_count(self, df):
        return (df.isnull().sum() > 0).sum()

    def get_duplicate_count(self, df):
        return df.duplicated().sum()

    def get_constant_columns(self, df):
        return [col for col in df.columns if df[col].nunique() <= 1]

    def get_quality_score(self, df):
        return round(100 - (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100, 2)

    def get_correlation(self, df, method="pearson"):
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        return df[numeric_cols].corr(method=method).round(3)

    def get_top_correlated_pairs(self, corr_matrix, n=10):
        corr_pairs = corr_matrix.unstack().reset_index()
        corr_pairs.columns = ["Column 1", "Column 2", "Correlation"]
        corr_pairs = corr_pairs[corr_pairs["Column 1"] != corr_pairs["Column 2"]]
        corr_pairs["Abs Correlation"] = corr_pairs["Correlation"].abs()
        corr_pairs = corr_pairs.drop_duplicates(subset=["Abs Correlation"])
        return corr_pairs.sort_values("Abs Correlation", ascending=False).head(n)

    def get_column_insights(self, df, col):
        info = {
            "dtype": str(df[col].dtype),
            "missing": df[col].isnull().sum(),
            "unique": df[col].nunique(),
            "missing_pct": round(df[col].isnull().sum() / len(df) * 100, 2)
        }
        if df[col].dtype in ['float64', 'int64']:
            info.update({
                "mean": round(df[col].mean(), 3),
                "median": round(df[col].median(), 3),
                "std": round(df[col].std(), 3),
                "skewness": round(df[col].skew(), 3)
            })
        else:
            val_counts = df[col].value_counts().head(10).reset_index()
            val_counts.columns = [col, "Count"]
            info["value_counts"] = val_counts
        return info