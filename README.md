# ⚒️ DataSmith — Smart Data Cleaning & EDA Toolkit

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Status-Live-22c55e?style=flat)
![License](https://img.shields.io/badge/License-Educational-8b5cf6?style=flat)

**From raw datasets to ML-ready data — clean, transform, visualize, all in one place.**

🔗 **Live App:** https://datasmith-eda-app-ashmit26.streamlit.app/

---

## What is DataSmith?

DataSmith is a fully interactive, no-code web application built with Python and Streamlit. Upload any CSV or Excel dataset and run through 14 preprocessing steps — from basic EDA all the way to outlier treatment, feature scaling, and export — without writing a single line of code.

Designed specifically to prepare raw datasets for Machine Learning workflows.

---

## Features

| Category | Features |
|---|---|
| 📂 Data Loading | CSV & Excel upload, file history, metadata display |
| 🔬 Exploration | Shape, dtypes, sample preview, missing value analysis, descriptive stats |
| 🛡️ Quality | Quality score, duplicate detection, constant column detection |
| 🧠 Insights | Column-wise deep dive — distribution, skewness, outlier count, top values |
| 🧹 Cleaning | Fill missing (Mean / Median / Mode / FFill / BFill / Custom), remove duplicates |
| ⚙️ Transformation | Label / One-Hot / Ordinal encoding, rename columns, drop columns, dtype conversion |
| 📏 Scaling | StandardScaler, MinMaxScaler, RobustScaler |
| 🎯 Outliers | IQR & Z-Score detection — remove or cap treatment |
| 🔍 Filtering | Numeric range, categorical, date, and global text search filters |
| 🔗 Correlation | Pearson / Spearman / Kendall matrix + interactive heatmap |
| 📈 Visualization | 8 chart types + 3D Scatter, 3D Line, 3D Surface via Plotly |
| 📋 Profiling | Full automated EDA report via ydata-profiling |
| 💾 Export | Download cleaned dataset as CSV or Excel |

**Bonus UX:**
- Dark / Light mode toggle
- Transformation log with timestamps and download
- Reset to original data anytime
- Recent file history in sidebar
- Full CSS makeover — animated background, gradient cards, hover effects

---

## Getting Started

### Prerequisites

- Python 3.11
- pip

### Installation

```bash
git clone https://github.com/AshmitS26/datasmith-eda-app.git
cd datasmith-eda-app
pip install -r requirements.txt
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## Project Structure

```
datasmith-eda-app/
│
├── app.py                        # Main entry point — orchestrates UI flow
├── requirements.txt              # All dependencies
├── titanic.csv                   # Sample dataset (CSV)
├── titanic.xlsx                  # Sample dataset (Excel)
│
├── .streamlit/
│   └── config.toml               # Default dark theme config
│
├── logic/                        # Pure Python — zero Streamlit code
│   ├── __init__.py
│   ├── data_loader.py            # DataLoader class
│   ├── data_cleaner.py           # DataCleaner class
│   ├── data_transformation.py    # DataTransformer class
│   ├── data_scaling.py           # DataScaler class
│   ├── outlier_detection.py      # DataOutlier class
│   ├── data_filtering.py         # DataFilter class
│   ├── data_visualization.py     # DataVisualization class
│   ├── eda.py                    # DataEDA class
│   └── data_profiling.py         # DataProfiler class
│
└── UI/                           # Streamlit UI — calls logic classes only
    ├── __init__.py
    ├── style.py                  # Full CSS makeover
    ├── sidebar.py                # Sidebar, navigation, transformation log
    ├── loader.py                 # Upload and export UI
    ├── preview.py                # Dataset preview UI
    ├── eda_UI.py                 # Statistics, quality, correlation, insights
    ├── cleaner.py                # Cleaning UI
    ├── transfromation.py         # Transformation UI
    ├── scaling.py                # Scaling UI
    ├── outlier.py                # Outlier UI
    ├── filtering.py              # Filtering UI
    ├── visualization.py          # Charts and 3D visualization UI
    └── profiling.py              # Profiling report UI
```

---

## Architecture

DataSmith follows a strict separation of concerns — UI and logic are completely decoupled.

```
UI Layer (Streamlit only)           Logic Layer (Pure Python only)
─────────────────────────           ──────────────────────────────
UI/cleaner.py            ────────►  logic/data_cleaner.py
UI/transfromation.py     ────────►  logic/data_transformation.py
UI/scaling.py            ────────►  logic/data_scaling.py
UI/outlier.py            ────────►  logic/outlier_detection.py
UI/filtering.py          ────────►  logic/data_filtering.py
UI/visualization.py      ────────►  logic/data_visualization.py
UI/eda_UI.py             ────────►  logic/eda.py
UI/profiling.py          ────────►  logic/data_profiling.py
```

- **logic/** — Python classes with all data processing. No Streamlit imports anywhere.
- **UI/** — Streamlit rendering only. Calls logic classes, never processes data directly.
- **app.py** — Pure routing. Imports UI functions and calls them in order.

---

## Application Workflow

| Step | Section | Description |
|------|---------|-------------|
| 1 | 📂 Upload | Upload CSV or Excel, view file metadata |
| 2 | 👁️ Preview | Shape, dtypes, sample rows |
| 3 | 🔬 Statistics | Missing values, unique counts, descriptive stats |
| 4 | 🛡️ Quality | Quality score, duplicates, constant columns |
| 5 | 🧠 Column Insights | Per-column distribution, skewness, top values |
| 6 | 🧹 Cleaning | Fill missing values, remove duplicates |
| 7 | ⚙️ Transformation | Encode, rename, drop, convert columns |
| 8 | 📏 Scaling | Standard / MinMax / Robust scaling |
| 9 | 🎯 Outliers | IQR / Z-Score detection — remove or cap |
| 10 | 🔍 Filter | Numeric range, categorical, date, global search |
| 11 | 🔗 Correlation | Pearson / Spearman / Kendall heatmap |
| 12 | 📈 Visualizations | 8 chart types + 3D Scatter / Line / Surface |
| 13 | 📋 Profiling | Full automated EDA report |
| 14 | 💾 Export | Download cleaned data as CSV or Excel |

---

## Dependencies

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
ydata-profiling==4.18.4
numba==0.62.1
statsmodels
visions==0.8.1
phik
wordcloud
imagehash==4.3.2
```

---

## Known Limitations

| Issue | Detail |
|---|---|
| Profiling on Cloud | ydata-profiling may time out on Streamlit Community Cloud for large datasets. Works fully on local Python 3.11. |
| Theme Toggle | Uses st._config.set_option — works locally, may not persist on all cloud platforms. |
| Large Files | Streamlit Cloud has a 200MB memory limit. Very large datasets may be slow. |

---

## Sample Datasets

| File | Rows | Columns | Description |
|------|------|---------|-------------|
| titanic.csv | 891 | 15 | Mix of numeric, categorical, and missing values — ideal for testing all features |
| titanic.xlsx | 891 | 15 | Same dataset in Excel format |

---

## About the Developer

**Ashmit Singh**
B.Tech — Energy Science & Engineering, IIT Delhi

Built DataSmith to bridge the gap between raw datasets and ML-ready data, because every great ML model starts with clean, well-understood data.

---

## License

Built for educational purposes as part of a data science learning initiative at IIT Delhi.
