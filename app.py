import streamlit as st

from UI.style import inject_css
from UI.sidebar import init_session_state, sidebar
from UI.loader import data_upload, data_export
from UI.cleaner import data_cleaning
from UI.preview import preview
from UI.eda_UI import data_statistics, data_quality, data_correlation, data_insight
from UI.filtering import data_filtering
from UI.scaling import data_scaling
from UI.outlier import data_outlier
from UI.transfromation import data_transformation
from UI.visualization import data_visualization
from UI.profiling import data_profiling

# ── PAGE CONFIG ──
st.set_page_config(
    page_title="DataSmith - EDA Tool",
    page_icon="⚒️",
    layout="wide",
    initial_sidebar_state="expanded"
)
#CSS
inject_css()


# ── SESSION + SIDEBAR ──
init_session_state()
sidebar()

# ── TITLE ──
st.title("⚒️ DataSmith")
st.markdown("##### Your Smart Data Cleaning & EDA Toolkit")

with st.expander("ℹ️ How to use DataSmith — Quick Guide", expanded=False):
    st.markdown("""
    ### 👋 Welcome to DataSmith!

    **DataSmith** is an interactive EDA and data preprocessing tool. Follow these steps:

    **🗂️ Use the Sidebar to navigate between sections:**
    - Click any section link in the sidebar to jump directly to it
    - Use the **Reset button** to restore your original data anytime
    - Download your **Transformation Log** to track all changes made
    - Toggle between **Dark and Light mode** using the button at the top of the sidebar

    **📋 Workflow — follow this order for best results:**

    | Step | Section | What it does |
    |------|---------|-------------|
    | 1 | 📂 Upload | Upload your CSV or Excel file |
    | 2 | 👁️ Preview | View data shape, types, and sample rows |
    | 3 | 🔬 Statistics | Missing values, unique values, descriptive stats |
    | 4 | 🛡️ Quality | Quality score, duplicates, constant columns |
    | 5 | 🧠 Insights | Deep dive into any single column |
    | 6 | 🧹 Cleaning | Fill missing values, remove duplicates |
    | 7 | ⚙️ Transformation | Encode, rename, drop, convert columns |
    | 8 | 📏 Scaling | Standardize or normalize numeric columns |
    | 9 | 🎯 Outliers | Detect and remove/cap outliers |
    | 10 | 🔍 Filter | Filter rows by value, category, or date |
    | 11 | 🔗 Correlation | Correlation matrix and heatmap |
    | 12 | 📈 Visualizations | Charts including 3D plots |
    | 13 | 📋 Profiling | Full automated EDA report |
    | 14 | 💾 Export | Download cleaned dataset as CSV or Excel |

    **💡 Tips:**
    - Use the **Transformation Log** in the sidebar to track every change
    - **Reset** anytime to go back to your original uploaded data
    """)

st.divider()

# ── UPLOAD ──
data_upload()

if st.session_state['df'] is not None:
    df = st.session_state['df']
    filename = st.session_state['filename']

    st.divider()
    preview()

    st.divider()
    data_statistics(df)

    st.divider()
    data_quality(df)

    st.divider()
    data_insight(df)

    st.divider()
    df = data_cleaning(df)

    st.divider()
    df = data_transformation(df)

    st.divider()
    df = data_scaling(df)

    st.divider()
    df = data_outlier(df)

    st.divider()
    data_filtering(df)

    st.divider()
    data_correlation(df)

    st.divider()
    data_visualization(df)

    st.divider()
    data_profiling(df)

    st.divider()
    data_export(df, filename)

# ── ABOUT THE DEVELOPER ──
st.divider()
st.subheader("👨‍💻 About the Developer")
col1, col2 = st.columns([1, 2])
with col1:
    st.markdown("""
    <div style="padding: 20px; border-radius: 12px; border: 1px solid #636EFA; text-align: center;">
        <h2 style="margin:0">🎓</h2>
        <h3 style="margin: 8px 0 4px 0;">Ashmit Singh</h3>
        <p style="margin:0; opacity:0.7;">IIT Delhi</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    **Hey there!** 👋

    I'm **Ashmit Singh**, a tech and Machine Learning enthusiast from **IIT Delhi**.

    I built **DataSmith** to bridge the gap between raw datasets and ML-ready data —
    because every great ML model starts with clean, well-understood data.
    """)
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🏛️ **Institution**\nIIT Delhi")
    with col2:
        st.info("💡 **Interests**\nMachine Learning & Tech")
    with col3:
        st.info("🛠️ **Built With**\nPython & Streamlit")