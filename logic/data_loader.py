import pandas as pd
import io


class DataLoader:

    def __init__(self):
        self.supported_formats = ['.csv', '.xlsx']
        self.last_loaded_filename = None
        self.last_loaded_shape = None

    def load_file(self, file):
        self.last_loaded_filename = file.name
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        self.last_loaded_shape = df.shape
        return df

    def export_csv(self, df):
        return df.to_csv(index=False).encode('utf-8')

    def export_excel(self, df):
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Cleaned Data')
        return buffer.getvalue()

    def get_file_info(self):
        return {
            'filename': self.last_loaded_filename,
            'rows': self.last_loaded_shape[0],
            'columns': self.last_loaded_shape[1],
            'format': self.last_loaded_filename.split('.')[-1].upper()
        }