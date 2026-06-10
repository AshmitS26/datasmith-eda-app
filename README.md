# ⚒️ DataSmith — Interactive EDA & Data Preprocessing Tool

**DataSmith** is a fully interactive web application built with Python and Streamlit that enables users to upload datasets, explore and clean their data, apply transformations, and visualize insights — all without writing a single line of code. It is designed to prepare raw datasets for Machine Learning workflows.

---

## 🚀 Getting Started

### Prerequisites
Make sure you have **Python 3.10 or above** installed.

### Installation

**Step 1 — Clone or download the project**
```
eda_app/
├── app.py
├── requirements.txt
├── titanic.csv
├── titanic.xlsx
└── modules/
    ├── __init__.py
    ├── overview.py
    ├── statistics.py
    ├── quality.py
    ├── cleaning.py
    ├── transformation.py
    ├── scaling.py
    ├── outliers.py
    ├── filtering.py
    ├── visualization.py
    ├── correlation.py
    ├── insights.py
    ├── profiling.py
    └── export.py
```

**Step 2 — Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 3 — Run the app**
```bash
streamlit run app.py
```

**Step 4 — Open in browser**
```
http://localhost:8501
```

---

## 📋 Requirements

```
streamlit
pandas
numpy
plotly
matplotlib
seaborn
scikit-learn
scipy
openpyxl
xlsxwriter
ydata-profiling
```

---

## 🧭 How to Use

### 1. Upload Your Dataset
- Click **Browse files** or drag and drop your file
- Supported formats: `.csv` and `.xlsx`
- The app instantly shows a success message with the filename

### 2. Dataset Overview
- View total rows, columns, and file format
- See column-wise data types and a type summary
- Preview the first 5 rows of your dataset

### 3. Dataset Statistics and Analysis
- **Missing Values tab** — see which columns have nulls and how many
- **Unique Values tab** — see cardinality of each column
- **Descriptive Statistics tab** — mean, std, min, max, quartiles for numeric columns

### 4. Data Quality Summary
- Quality Score — overall data health percentage
- Count of missing cells, duplicate rows, and constant columns

### 5. Data Cleaning

**Missing Value Treatment:**
- Select a column with missing values
- Choose a fill method: Mean, Median, Mode, Forward Fill, Backward Fill, Custom Value, or Remove Rows
- Click **Apply Treatment**

**Duplicate Rows:**
- See count of duplicate rows
- Preview them and click **Remove Duplicates**

### 6. Data Transformation

| Tab | What it does |
|-----|-------------|
| Label Encoding | Converts text categories to numbers (best for target column) |
| One-Hot Encoding | Creates binary columns for each category |
| Ordinal Encoding | Assigns ordered numbers based on your defined sequence |
| Datatype Conversion | Change column dtype (int, float, str, bool) |
| Rename / Drop | Rename any column or drop multiple columns at once |

### 7. Feature Scaling
- Select one or more numeric columns
- Choose scaling method: Standard Scaler, MinMax Scaler, or Robust Scaler
- A method guide is shown to help you pick the right one

### 8. Outlier Detection and Treatment
- Select a numeric column
- Choose detection method: **IQR** or **Z-Score**
- View outlier count, percentage, and a box plot
- Choose to **Remove** or **Cap (Winsorize)** outliers

### 9. Data Filtering and Exploration
- **Numeric Filter** — slider to filter rows by value range
- **Categorical Filter** — multiselect to filter by category values
- **Date Filter** — date range picker for date columns
- **Global Search** — search any value across all columns

### 10. Visualization Dashboard

| Chart | Use case |
|-------|---------|
| Histogram | Distribution of a numeric column |
| Box Plot | Spread and outliers, optionally grouped |
| Scatter Plot | Relationship between two numeric columns |
| Line Chart | Trends over an axis |
| Bar Chart | Aggregated numeric value by category |
| Pie Chart | Proportion of categories |
| Distribution Plot | KDE curve with skewness and kurtosis |
| Correlation Heatmap | Visual correlation between all numeric columns |

### 11. Correlation Analysis
- Choose Pearson, Spearman, or Kendall method
- View full correlation matrix and heatmap side by side
- Top 10 most correlated column pairs listed

### 12. Column-wise Insights
- Select any column to get a full breakdown
- Numeric columns: mean, median, std, skewness + distribution chart
- Categorical columns: top 10 value counts + bar chart

### 13. Data Profiling Dashboard
- Click **Generate Profiling Report** for a full automated EDA report
- Download the report as an HTML file
- Note: Takes 15–30 seconds depending on dataset size

### 14. Export Dataset
- Download your cleaned and transformed data as **CSV** or **Excel**
- Metrics show current shape vs original shape

---

## 🗂️ Sidebar Features

| Feature | Description |
|---------|-------------|
| 🌙 / ☀️ Theme Toggle | Switch between dark and light mode |
| 🗂️ Quick Navigation | Click any section to jump directly to it |
| 📝 Transformation Log | Live log of last 5 operations with download option |
| 🔄 Reset Button | Restore dataset to original uploaded state |
| 🕘 Recent Files | History of last 5 uploaded filenames |

---

## 📁 Sample Datasets
Two sample datasets are included for testing:
- `titanic.csv` — 891 rows, 15 columns, mix of numeric and categorical, has missing values and outliers
- `titanic.xlsx` — same dataset in Excel format

---

## 🧩 Project Structure

```
eda_app/
├── app.py                  # Main application file
├── requirements.txt        # All dependencies
├── titanic.csv             # Sample dataset (CSV)
├── titanic.xlsx            # Sample dataset (Excel)
└── modules/                # Modular Python code
    ├── __init__.py         # Package initializer
    ├── overview.py         # Function 1 — Dataset Overview
    ├── statistics.py       # Function 2 — Statistics & Analysis
    ├── quality.py          # Function 3 — Data Quality Checks
    ├── cleaning.py         # Functions 4 & 5 — Missing Values & Duplicates
    ├── transformation.py   # Function 6 — Data Transformation
    ├── scaling.py          # Function 7 — Feature Scaling
    ├── outliers.py         # Function 8 — Outlier Detection & Treatment
    ├── filtering.py        # Function 9 — Data Filtering & Exploration
    ├── visualization.py    # Function 10 — Visualization Dashboard
    ├── correlation.py      # Function 11 — Correlation Analysis
    ├── insights.py         # Column-wise Insights (Optional)
    ├── profiling.py        # Data Profiling Dashboard (Optional)
    └── export.py           # Function 12 — Data Export
```

---

## 👨‍💻 About the Developer

**Ashmit Singh** — Tech and Machine Learning enthusiast from **IIT Delhi**.

Built DataSmith to help bridge the gap between raw datasets and ML-ready data, because every great ML model starts with clean, well-understood data.

---

## 📄 License
This project is built for educational purposes as part of a data science learning initiative.