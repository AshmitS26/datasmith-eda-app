import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler


class DataScaler:

    def get_numeric_columns(self, df):
        return df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    def get_scaler(self, method):
        if "Standard" in method:
            return StandardScaler()
        elif "MinMax" in method:
            return MinMaxScaler()
        else:
            return RobustScaler()

    def scale(self, df, cols, method):
        scaler = self.get_scaler(method)
        df[cols] = scaler.fit_transform(df[cols])
        return df

    def get_scaled_summary(self, df, cols):
        return df[cols].describe().round(4)