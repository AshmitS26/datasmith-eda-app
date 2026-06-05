import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import LabelEncoder
import io
import json
from datetime import datetime

# ── PAGE CONFIG ──
st.set_page_config(
    page_title="DataSmith - EDA Tool",
    page_icon="⚒️",
    layout="wide"
)

# ── THEME TOGGLE ──
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'dark'

if st.session_state['theme'] == 'dark':
    st.markdown("""
        <style>
            .stApp { background-color: #0e1117; color: #fafafa; }
            .metric-card { background-color: #1e2130; border-radius: 10px; padding: 15px; }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            .stApp { background-color: #ffffff; color: #000000; }
            .metric-card { background-color: #f0f2f6; border-radius: 10px; padding: 15px; }
        </style>
    """, unsafe_allow_html=True)

# ── SESSION STATE INIT ──
if 'transformation_log' not in st.session_state:
    st.session_state['transformation_log'] = []
if 'file_history' not in st.session_state:
    st.session_state['file_history'] = []

def log_transformation(action):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state['transformation_log'].append(f"[{timestamp}] {action}")

# ── SIDEBAR ──
with st.sidebar:
    st.title("⚒️ DataSmith")
    st.markdown("---")

    # Theme Toggle
    theme_label = "☀️ Switch to Light Mode" if st.session_state['theme'] == 'dark' else "🌙 Switch to Dark Mode"
    if st.button(theme_label, use_container_width=True):
        st.session_state['theme'] = 'light' if st.session_state['theme'] == 'dark' else 'dark'
        st.rerun()

    st.markdown("---")
    st.markdown("## 🗂️ Quick Navigation")
    st.caption("Click any section to jump directly to it")

    nav_bg = "#1e2130" if st.session_state['theme'] == 'dark' else "#e8eaf0"
    nav_color = "white" if st.session_state['theme'] == 'dark' else "#000000"

    st.markdown(f"""
    <a href="#upload-your-dataset" style="text-decoration:none">
        <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">📂 1. Upload Dataset</div>
    </a>
    <a href="#dataset-overview" style="text-decoration:none">
        <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">📊 2. Dataset Overview</div>
    </a>
    <a href="#dataset-statistics-and-analysis" style="text-decoration:none">
        <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">🔬 3. Statistics</div>
    </a>
    <a href="#data-quality-summary" style="text-decoration:none">
        <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">🛡️ 4. Quality Summary</div>
    </a>
    <a href="#data-cleaning" style="text-decoration:none">
        <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">🧹 5. Data Cleaning</div>
    </a>
    <a href="#data-transformation" style="text-decoration:none">
        <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">⚙️ 6. Transformation</div>
    </a>
    <a href="#feature-scaling" style="text-decoration:none">
        <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">📏 7. Feature Scaling</div>
    </a>
    <a href="#outlier-detection-and-treatment" style="text-decoration:none">
        <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">🎯 8. Outlier Treatment</div>
    </a>
    <a href="#data-filtering-and-exploration" style="text-decoration:none">
        <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">🔍 9. Filter & Explore</div>
    </a>
    <a href="#visualization-dashboard" style="text-decoration:none">
        <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">📈 10. Visualizations</div>
    </a>
    <a href="#correlation-analysis" style="text-decoration:none">
        <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">🔗 11. Correlation</div>
    </a>
    <a href="#column-wise-insights" style="text-decoration:none">
        <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">🧠 12. Column Insights</div>
    </a>
    <a href="#data-profiling-dashboard" style="text-decoration:none">
        <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">📋 13. Data Profiling</div>
    </a>
    <a href="#export-dataset" style="text-decoration:none">
        <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">💾 14. Export Data</div>
    </a>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Transformation Log in Sidebar
    st.markdown("## 📝 Transformation Log")
    st.caption("Last 5 operations applied")
    if 'transformation_log' in st.session_state and len(st.session_state['transformation_log']) > 0:
        for entry in st.session_state['transformation_log'][-5:]:
            st.caption(f"• {entry}")
        if len(st.session_state['transformation_log']) > 5:
            st.caption(f"... and {len(st.session_state['transformation_log']) - 5} more (download in Export section)")
        st.markdown("")
        log_text = "\n".join(st.session_state['transformation_log'])
        st.download_button(
            label="⬇️ Download Full Log",
            data=log_text,
            file_name="datasmith_transformation_log.txt",
            mime="text/plain",
            use_container_width=True,
            key="sidebar_log_download"
        )
    else:
        st.caption("No transformations yet")

    st.markdown("---")

    if st.button("🔄 Reset to Original Data", use_container_width=True):
        if 'original_df' in st.session_state:
            st.session_state['df'] = st.session_state['original_df'].copy()
            log_transformation("Reset to original data")
            st.success("✅ Reset done")
            st.rerun()

    # Recent File History
    if len(st.session_state['file_history']) > 0:
        st.markdown("---")
        st.markdown("## 🕘 Recent Files")
        for f in st.session_state['file_history'][-5:][::-1]:
            st.caption(f"📄 {f}")

# ── TITLE ──
st.title("⚒️ DataSmith")
st.markdown("##### Your Smart Data Cleaning & EDA Toolkit")
st.divider()

# ── UPLOAD ──
st.subheader("📂 Upload Your Dataset")
st.markdown("Supported formats: **CSV** and **Excel (.xlsx)**")

uploaded_file = st.file_uploader(
    label="Drag and drop or click to browse",
    type=["csv", "xlsx"],
    help="Upload a CSV or Excel file to begin analysis"
)

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    st.session_state['df'] = df
    st.session_state['original_df'] = df.copy()
    st.session_state['filename'] = uploaded_file.name

    if uploaded_file.name not in st.session_state['file_history']:
        st.session_state['file_history'].append(uploaded_file.name)

    log_transformation(f"Uploaded file: {uploaded_file.name} — Shape: {df.shape}")
    st.success(f"✅ **{uploaded_file.name}** uploaded successfully!")

if 'df' in st.session_state:
    df = st.session_state['df']
    filename = st.session_state.get('filename', 'dataset')

    st.divider()

    # ══════════════════════════════════════════
    # FUNCTION 1 — Dataset Overview
    # ══════════════════════════════════════════
    st.subheader("📊 Dataset Overview")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rows", df.shape[0])
    with col2:
        st.metric("Total Columns", df.shape[1])
    with col3:
        st.metric("File Format", filename.split('.')[-1].upper())

    st.divider()

    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("🏷️ Column Data Types")
        dtype_df = pd.DataFrame({
            "Column": df.dtypes.index,
            "Data Type": df.dtypes.values.astype(str)
        })
        st.dataframe(dtype_df, use_container_width=True, hide_index=True)

    with col_right:
        st.subheader("📈 Type Summary")
        type_summary = df.dtypes.astype(str).value_counts().reset_index()
        type_summary.columns = ["Data Type", "Count"]
        st.dataframe(type_summary, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("👁️ Dataset Preview")
    st.markdown("Showing first **5 rows** of your dataset")
    st.dataframe(df.head().astype(str), use_container_width=True)

    st.divider()

    # ══════════════════════════════════════════
    # FUNCTION 2 — Statistics & Analysis
    # ══════════════════════════════════════════
    st.subheader("🔬 Dataset Statistics and Analysis")

    tab1, tab2, tab3 = st.tabs(["Missing Values", "Unique Values", "Descriptive Statistics"])

    with tab1:
        st.markdown("#### 🚨 Missing Values Analysis")
        missing = pd.DataFrame({
            "Column": df.columns,
            "Missing Count": df.isnull().sum().values,
            "Missing %": (df.isnull().sum().values / len(df) * 100).round(2)
        }).sort_values("Missing Count", ascending=False)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Missing Values", df.isnull().sum().sum())
        with col2:
            st.metric("Columns with Missing Values", (df.isnull().sum() > 0).sum())
        st.dataframe(missing, use_container_width=True, hide_index=True)

    with tab2:
        st.markdown("#### 🔢 Unique Values Per Column")
        unique = pd.DataFrame({
            "Column": df.columns,
            "Unique Count": df.nunique().values,
            "Unique %": (df.nunique().values / len(df) * 100).round(2)
        }).sort_values("Unique Count", ascending=False)
        st.dataframe(unique, use_container_width=True, hide_index=True)

    with tab3:
        st.markdown("#### 📊 Descriptive Statistics")
        st.markdown("Numeric columns only")
        st.dataframe(df.describe().round(2), use_container_width=True)

    st.divider()

    # ══════════════════════════════════════════
    # FUNCTION 3 — Data Quality Summary
    # ══════════════════════════════════════════
    st.subheader("🛡️ Data Quality Summary")

    constant_cols = [col for col in df.columns if df[col].nunique() <= 1]
    quality_score = 100 - round((df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100, 2)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Missing Cells", df.isnull().sum().sum())
    with col2:
        st.metric("Duplicate Rows", df.duplicated().sum())
    with col3:
        st.metric("Constant Columns", len(constant_cols))
    with col4:
        st.metric("Quality Score", f"{quality_score}%")

    if len(constant_cols) > 0:
        st.warning(f"⚠️ Constant columns detected: {', '.join(constant_cols)}")
    else:
        st.success("✅ No constant columns found")

    st.divider()

    # ══════════════════════════════════════════
    # FUNCTION 4 & 5 — Data Cleaning
    # ══════════════════════════════════════════
    st.subheader("🧹 Data Cleaning")

    tab1, tab2 = st.tabs(["Missing Value Treatment", "Duplicate Rows"])

    with tab1:
        st.markdown("#### 🩹 Handle Missing Values")
        missing_cols_list = df.columns[df.isnull().any()].tolist()

        if len(missing_cols_list) == 0:
            st.success("✅ No missing values found in your dataset")
        else:
            st.markdown(f"**{len(missing_cols_list)} columns** have missing values:")
            st.dataframe(
                pd.DataFrame({
                    "Column": missing_cols_list,
                    "Missing Count": [df[col].isnull().sum() for col in missing_cols_list],
                    "Missing %": [(df[col].isnull().sum() / len(df) * 100).round(2) for col in missing_cols_list]
                }),
                use_container_width=True, hide_index=True
            )
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                selected_col = st.selectbox("Select Column to Treat", options=missing_cols_list)
            with col2:
                method = st.selectbox("Select Fill Method", options=[
                    "Mean", "Median", "Mode", "Forward Fill",
                    "Backward Fill", "Custom Value", "Remove Rows"
                ])

            custom_value = None
            if method == "Custom Value":
                custom_value = st.text_input("Enter Custom Value", placeholder="e.g. Unknown, 0, NA")

            if st.button("Apply Treatment", type="primary", key="mv_btn"):
                if method == "Remove Rows":
                    df = df.dropna(subset=[selected_col])
                    log_transformation(f"Removed rows with missing values in '{selected_col}'")
                    st.success(f"✅ Rows with missing **{selected_col}** removed. New shape: {df.shape}")
                elif method == "Mean":
                    if df[selected_col].dtype in ['float64', 'int64']:
                        fill_val = round(df[selected_col].mean(), 2)
                        df[selected_col] = df[selected_col].fillna(fill_val)
                        log_transformation(f"Filled '{selected_col}' missing values with Mean ({fill_val})")
                        st.success(f"✅ Filled **{selected_col}** with Mean: {fill_val}")
                    else:
                        st.error("❌ Mean can only be applied to numeric columns")
                elif method == "Median":
                    if df[selected_col].dtype in ['float64', 'int64']:
                        fill_val = round(df[selected_col].median(), 2)
                        df[selected_col] = df[selected_col].fillna(fill_val)
                        log_transformation(f"Filled '{selected_col}' missing values with Median ({fill_val})")
                        st.success(f"✅ Filled **{selected_col}** with Median: {fill_val}")
                    else:
                        st.error("❌ Median can only be applied to numeric columns")
                elif method == "Mode":
                    fill_val = df[selected_col].mode()[0]
                    df[selected_col] = df[selected_col].fillna(fill_val)
                    log_transformation(f"Filled '{selected_col}' missing values with Mode ({fill_val})")
                    st.success(f"✅ Filled **{selected_col}** with Mode: {fill_val}")
                elif method == "Forward Fill":
                    df[selected_col] = df[selected_col].ffill()
                    log_transformation(f"Applied Forward Fill on '{selected_col}'")
                    st.success(f"✅ Applied Forward Fill on **{selected_col}**")
                elif method == "Backward Fill":
                    df[selected_col] = df[selected_col].bfill()
                    log_transformation(f"Applied Backward Fill on '{selected_col}'")
                    st.success(f"✅ Applied Backward Fill on **{selected_col}**")
                elif method == "Custom Value":
                    if custom_value:
                        df[selected_col] = df[selected_col].fillna(custom_value)
                        log_transformation(f"Filled '{selected_col}' missing values with custom value '{custom_value}'")
                        st.success(f"✅ Filled **{selected_col}** with: **{custom_value}**")
                    else:
                        st.error("❌ Please enter a custom value")
                st.session_state['df'] = df
                st.dataframe(df.astype(str), use_container_width=True)

    with tab2:
        st.markdown("#### 🔁 Duplicate Row Handler")
        dup_count = df.duplicated().sum()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Duplicate Rows Found", dup_count)
        with col2:
            st.metric("Rows After Removal", df.shape[0] - dup_count)

        if dup_count == 0:
            st.success("✅ No duplicate rows found")
        else:
            st.warning(f"⚠️ **{dup_count}** duplicate rows detected")
            st.dataframe(df[df.duplicated()].astype(str), use_container_width=True)
            if st.button("Remove Duplicates", type="primary", key="dup_btn"):
                df = df.drop_duplicates()
                st.session_state['df'] = df
                log_transformation(f"Removed {dup_count} duplicate rows")
                st.success(f"✅ Duplicates removed. New shape: {df.shape}")
                st.rerun()

    st.divider()

    # ══════════════════════════════════════════
    # FUNCTION 6 — Data Transformation
    # ══════════════════════════════════════════
    st.subheader("⚙️ Data Transformation")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Label Encoding", "One-Hot Encoding", "Ordinal Encoding",
        "Datatype Conversion", "Rename / Drop Columns"
    ])

    with tab1:
        st.markdown("#### 🏷️ Label Encoding")
        st.info("Assigns a unique number to each category. Best for **target/output columns** only.")
        cat_cols_le = df.select_dtypes(include=['object', 'category']).columns.tolist()
        if len(cat_cols_le) == 0:
            st.success("✅ No categorical columns found")
        else:
            selected_le_col = st.selectbox("Select Column", options=cat_cols_le, key="le_col")
            st.markdown(f"**Unique values:** {', '.join(map(str, df[selected_le_col].dropna().unique()))}")
            if st.button("Apply Label Encoding", type="primary", key="le_btn"):
                le = LabelEncoder()
                df[selected_le_col] = le.fit_transform(df[selected_le_col].astype(str))
                st.session_state['df'] = df
                log_transformation(f"Applied Label Encoding on '{selected_le_col}'")
                st.success(f"✅ Label Encoding applied on **{selected_le_col}**")
                st.dataframe(df[[selected_le_col]], use_container_width=True)

    with tab2:
        st.markdown("#### 🔥 One-Hot Encoding")
        st.info("Creates a new column for each category. Best for **input features** with no order.")
        cat_cols_ohe = df.select_dtypes(include=['object', 'category']).columns.tolist()
        if len(cat_cols_ohe) == 0:
            st.success("✅ No categorical columns found")
        else:
            selected_ohe_col = st.selectbox("Select Column", options=cat_cols_ohe, key="ohe_col")
            unique_count = df[selected_ohe_col].nunique()
            st.markdown(f"**Unique values:** {unique_count} → will create **{unique_count} new columns**")
            if unique_count > 15:
                st.warning(f"⚠️ {unique_count} unique values will create many columns.")
            drop_first = st.checkbox("Drop first column (avoid dummy variable trap)", value=True, key="ohe_drop")
            if st.button("Apply One-Hot Encoding", type="primary", key="ohe_btn"):
                df = pd.get_dummies(df, columns=[selected_ohe_col], drop_first=drop_first)
                st.session_state['df'] = df
                log_transformation(f"Applied One-Hot Encoding on '{selected_ohe_col}'")
                st.success(f"✅ One-Hot Encoding applied. New shape: {df.shape}")
                st.dataframe(df.astype(str), use_container_width=True)

    with tab3:
        st.markdown("#### 📊 Ordinal Encoding")
        st.info("Assigns numbers based on a meaningful order you define.")
        cat_cols_oe = df.select_dtypes(include=['object', 'category']).columns.tolist()
        if len(cat_cols_oe) == 0:
            st.success("✅ No categorical columns found")
        else:
            selected_oe_col = st.selectbox("Select Column", options=cat_cols_oe, key="oe_col")
            unique_vals_oe = df[selected_oe_col].dropna().unique().tolist()
            st.markdown(f"**Unique values found:** {', '.join(map(str, unique_vals_oe))}")
            order_input = st.text_input(
                "Enter values in order (lowest → highest), comma separated",
                value=', '.join(map(str, unique_vals_oe)), key="oe_order"
            )
            if st.button("Apply Ordinal Encoding", type="primary", key="oe_btn"):
                order_list = [x.strip() for x in order_input.split(',')]
                order_map = {val: idx for idx, val in enumerate(order_list)}
                df[selected_oe_col] = df[selected_oe_col].map(order_map)
                st.session_state['df'] = df
                log_transformation(f"Applied Ordinal Encoding on '{selected_oe_col}'")
                st.success(f"✅ Ordinal Encoding applied on **{selected_oe_col}**")
                st.dataframe(
                    pd.DataFrame({"Category": list(order_map.keys()), "Encoded Value": list(order_map.values())}),
                    use_container_width=True, hide_index=True
                )

    with tab4:
        st.markdown("#### 🔄 Datatype Conversion")
        col1, col2 = st.columns(2)
        with col1:
            selected_dtype_col = st.selectbox("Select Column", options=df.columns.tolist(), key="dtype_col")
            st.markdown(f"**Current dtype:** `{df[selected_dtype_col].dtype}`")
        with col2:
            target_dtype = st.selectbox("Convert To", options=["int64", "float64", "str", "bool"], key="dtype_target")
        if st.button("Convert Datatype", type="primary", key="dtype_btn"):
            try:
                df[selected_dtype_col] = df[selected_dtype_col].astype(target_dtype)
                st.session_state['df'] = df
                log_transformation(f"Converted '{selected_dtype_col}' to {target_dtype}")
                st.success(f"✅ **{selected_dtype_col}** converted to `{target_dtype}`")
            except Exception as e:
                st.error(f"❌ Conversion failed: {e}")

    with tab5:
        st.markdown("#### ✏️ Rename or Drop Columns")
        inner_tab1, inner_tab2 = st.tabs(["Rename Column", "Drop Columns"])
        with inner_tab1:
            col1, col2 = st.columns(2)
            with col1:
                col_to_rename = st.selectbox("Select Column to Rename", options=df.columns.tolist(), key="rename_col")
            with col2:
                new_col_name = st.text_input("Enter New Name", placeholder="e.g. passenger_age", key="rename_new")
            if st.button("Rename Column", type="primary", key="rename_btn"):
                if new_col_name:
                    df = df.rename(columns={col_to_rename: new_col_name})
                    st.session_state['df'] = df
                    log_transformation(f"Renamed column '{col_to_rename}' to '{new_col_name}'")
                    st.success(f"✅ **{col_to_rename}** renamed to **{new_col_name}**")
                    st.rerun()
                else:
                    st.error("❌ Please enter a new column name")
        with inner_tab2:
            cols_to_drop = st.multiselect("Select Columns to Drop", options=df.columns.tolist(), key="drop_cols")
            if cols_to_drop:
                st.warning(f"⚠️ About to drop: {', '.join(cols_to_drop)}")
            if st.button("Drop Selected Columns", type="primary", key="drop_btn"):
                if cols_to_drop:
                    df = df.drop(columns=cols_to_drop)
                    st.session_state['df'] = df
                    log_transformation(f"Dropped columns: {', '.join(cols_to_drop)}")
                    st.success(f"✅ Dropped {len(cols_to_drop)} column(s). New shape: {df.shape}")
                    st.rerun()
                else:
                    st.error("❌ Please select at least one column")

    st.divider()

    # ══════════════════════════════════════════
    # FUNCTION 7 — Feature Scaling
    # ══════════════════════════════════════════
    st.subheader("📏 Feature Scaling")

    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    if len(numeric_cols) == 0:
        st.warning("⚠️ No numeric columns found for scaling")
    else:
        col1, col2 = st.columns(2)
        with col1:
            scale_cols = st.multiselect("Select Columns to Scale", options=numeric_cols, key="scale_cols")
        with col2:
            scale_method = st.selectbox("Select Scaling Method", options=[
                "Standard Scaler (Z-score)",
                "MinMax Scaler (0 to 1)",
                "Robust Scaler (outlier resistant)"
            ], key="scale_method")

        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("**Standard Scaler**\nMean=0, Std=1\nUse when no outliers")
        with col2:
            st.info("**MinMax Scaler**\nRange: 0 to 1\nUse when bounded range needed")
        with col3:
            st.info("**Robust Scaler**\nUses median & IQR\nUse when outliers present")

        if st.button("Apply Scaling", type="primary", key="scale_btn"):
            if not scale_cols:
                st.error("❌ Please select at least one column")
            else:
                from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
                if "Standard" in scale_method:
                    scaler = StandardScaler()
                elif "MinMax" in scale_method:
                    scaler = MinMaxScaler()
                else:
                    scaler = RobustScaler()
                df[scale_cols] = scaler.fit_transform(df[scale_cols])
                st.session_state['df'] = df
                log_transformation(f"Applied {scale_method} on columns: {', '.join(scale_cols)}")
                st.success(f"✅ **{scale_method}** applied on {len(scale_cols)} column(s)")
                st.dataframe(df[scale_cols].describe().round(4), use_container_width=True)

    st.divider()

    # ══════════════════════════════════════════
    # FUNCTION 8 — Outlier Detection and Treatment
    # ══════════════════════════════════════════
    st.subheader("🎯 Outlier Detection and Treatment")

    numeric_cols_out = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    if len(numeric_cols_out) == 0:
        st.warning("⚠️ No numeric columns found")
    else:
        col1, col2 = st.columns(2)
        with col1:
            outlier_col = st.selectbox("Select Column", options=numeric_cols_out, key="out_col")
        with col2:
            outlier_method = st.selectbox("Detection Method", options=["IQR Method", "Z-Score Method"], key="out_method")

        if outlier_method == "IQR Method":
            Q1 = df[outlier_col].quantile(0.25)
            Q3 = df[outlier_col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            outliers = df[(df[outlier_col] < lower) | (df[outlier_col] > upper)]
            st.markdown(f"**Q1:** {round(Q1,2)} | **Q3:** {round(Q3,2)} | **IQR:** {round(IQR,2)}")
            st.markdown(f"**Lower bound:** {round(lower,2)} | **Upper bound:** {round(upper,2)}")
        else:
            z_scores = np.abs(stats.zscore(df[outlier_col].dropna()))
            threshold = st.slider("Z-Score Threshold", min_value=1.0, max_value=4.0, value=3.0, step=0.1)
            outlier_indices = df[outlier_col].dropna().index[z_scores > threshold]
            outliers = df.loc[outlier_indices]

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Outliers Detected", len(outliers))
        with col2:
            st.metric("Outlier %", f"{round(len(outliers)/len(df)*100, 2)}%")

        fig = px.box(df, y=outlier_col, title=f"Box Plot — {outlier_col}",
                     color_discrete_sequence=["#636EFA"])
        st.plotly_chart(fig, use_container_width=True)

        if len(outliers) > 0:
            st.markdown("**Outlier rows preview:**")
            st.dataframe(outliers.astype(str), use_container_width=True)
            out_action = st.selectbox("Action", options=["Remove Outliers", "Cap Outliers (Winsorize)"], key="out_action")
            if st.button("Apply Outlier Treatment", type="primary", key="out_btn"):
                if out_action == "Remove Outliers":
                    if outlier_method == "IQR Method":
                        df = df[(df[outlier_col] >= lower) & (df[outlier_col] <= upper)]
                    else:
                        df = df.drop(index=outlier_indices)
                    log_transformation(f"Removed outliers from '{outlier_col}' using {outlier_method}")
                    st.success(f"✅ Outliers removed. New shape: {df.shape}")
                else:
                    if outlier_method == "IQR Method":
                        df[outlier_col] = df[outlier_col].clip(lower=lower, upper=upper)
                    else:
                        mean = df[outlier_col].mean()
                        std = df[outlier_col].std()
                        df[outlier_col] = df[outlier_col].clip(
                            lower=mean - threshold * std,
                            upper=mean + threshold * std
                        )
                    log_transformation(f"Capped outliers in '{outlier_col}' using {outlier_method}")
                    st.success(f"✅ Outliers capped in **{outlier_col}**")
                st.session_state['df'] = df
                st.rerun()

    st.divider()

    # ══════════════════════════════════════════
    # FUNCTION 9 — Data Filtering and Exploration
    # ══════════════════════════════════════════
    st.subheader("🔍 Data Filtering and Exploration")

    search_term = st.text_input("🔎 Search across all columns", placeholder="Type to search any value...")

    tab1, tab2, tab3 = st.tabs(["Numeric Filter", "Categorical Filter", "Date Filter"])

    with tab1:
        st.markdown("#### 🔢 Filter Numeric Columns")
        num_cols_filter = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        if len(num_cols_filter) == 0:
            st.info("No numeric columns available")
        else:
            num_filter_col = st.selectbox("Select Numeric Column", options=num_cols_filter, key="num_fcol")
            col_min = float(df[num_filter_col].min())
            col_max = float(df[num_filter_col].max())
            num_range = st.slider(
                f"Select Range for {num_filter_col}",
                min_value=col_min, max_value=col_max,
                value=(col_min, col_max), key="num_range"
            )
            filtered_df = df[
                (df[num_filter_col] >= num_range[0]) &
                (df[num_filter_col] <= num_range[1])
            ]
            st.markdown(f"**Rows matching filter:** {len(filtered_df)}")
            st.dataframe(filtered_df.astype(str), use_container_width=True)

    with tab2:
        st.markdown("#### 🏷️ Filter Categorical Columns")
        cat_cols_filter = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
        if len(cat_cols_filter) == 0:
            st.info("No categorical columns available")
        else:
            cat_filter_col = st.selectbox("Select Categorical Column", options=cat_cols_filter, key="cat_fcol")
            unique_cat_vals = df[cat_filter_col].dropna().unique().tolist()
            selected_vals = st.multiselect(
                f"Select values for {cat_filter_col}",
                options=unique_cat_vals,
                default=unique_cat_vals,
                key="cat_vals"
            )
            cat_filtered = df[df[cat_filter_col].isin(selected_vals)]
            st.markdown(f"**Rows matching filter:** {len(cat_filtered)}")
            st.dataframe(cat_filtered.astype(str), use_container_width=True)

    with tab3:
        st.markdown("#### 📅 Filter Date Columns")
        date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        possible_date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
        all_date_cols = list(set(date_cols + possible_date_cols))
        if len(all_date_cols) == 0:
            st.info("No date columns detected. Convert column dtype first using Data Transformation.")
        else:
            date_col_sel = st.selectbox("Select Date Column", options=all_date_cols, key="date_fcol")
            try:
                df[date_col_sel] = pd.to_datetime(df[date_col_sel])
                min_date = df[date_col_sel].min().date()
                max_date = df[date_col_sel].max().date()
                date_range = st.date_input("Select Date Range", value=(min_date, max_date), key="date_range")
                if len(date_range) == 2:
                    date_filtered = df[
                        (df[date_col_sel].dt.date >= date_range[0]) &
                        (df[date_col_sel].dt.date <= date_range[1])
                    ]
                    st.markdown(f"**Rows in range:** {len(date_filtered)}")
                    st.dataframe(date_filtered.astype(str), use_container_width=True)
            except Exception as e:
                st.error(f"❌ Could not parse dates: {e}")

    if search_term:
        st.markdown(f"#### 🔎 Search Results for: `{search_term}`")
        mask = df.astype(str).apply(lambda col: col.str.contains(search_term, case=False, na=False)).any(axis=1)
        search_results = df[mask]
        st.markdown(f"**{len(search_results)} rows** found")
        st.dataframe(search_results.astype(str), use_container_width=True)

    st.divider()

    # ══════════════════════════════════════════
    # FUNCTION 10 — Visualization Dashboard
    # ══════════════════════════════════════════
    st.subheader("📈 Visualization Dashboard")

    numeric_cols_viz = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    cat_cols_viz = df.select_dtypes(include=['object', 'category']).columns.tolist()

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "Histogram", "Box Plot", "Scatter Plot", "Line Chart",
        "Bar Chart", "Pie Chart", "Distribution Plot", "Correlation Heatmap"
    ])

    with tab1:
        st.markdown("#### 📊 Histogram")
        if numeric_cols_viz:
            hist_col = st.selectbox("Select Column", options=numeric_cols_viz, key="hist_col")
            hist_bins = st.slider("Number of Bins", min_value=5, max_value=100, value=30, key="hist_bins")
            fig = px.histogram(df, x=hist_col, nbins=hist_bins, title=f"Histogram — {hist_col}",
                               color_discrete_sequence=["#636EFA"])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No numeric columns available")

    with tab2:
        st.markdown("#### 📦 Box Plot")
        if numeric_cols_viz:
            box_col = st.selectbox("Select Numeric Column", options=numeric_cols_viz, key="box_col")
            box_group = st.selectbox("Group By (optional)", options=["None"] + cat_cols_viz, key="box_group")
            if box_group == "None":
                fig = px.box(df, y=box_col, title=f"Box Plot — {box_col}")
            else:
                fig = px.box(df, x=box_group, y=box_col, color=box_group,
                             title=f"Box Plot — {box_col} by {box_group}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No numeric columns available")

    with tab3:
        st.markdown("#### 🔵 Scatter Plot")
        if len(numeric_cols_viz) >= 2:
            col1, col2, col3 = st.columns(3)
            with col1:
                scatter_x = st.selectbox("X Axis", options=numeric_cols_viz, key="scatter_x")
            with col2:
                scatter_y = st.selectbox("Y Axis", options=numeric_cols_viz, index=1, key="scatter_y")
            with col3:
                scatter_color = st.selectbox("Color By (optional)", options=["None"] + cat_cols_viz, key="scatter_color")
            if scatter_color == "None":
                fig = px.scatter(df, x=scatter_x, y=scatter_y, title=f"Scatter — {scatter_x} vs {scatter_y}")
            else:
                fig = px.scatter(df, x=scatter_x, y=scatter_y, color=scatter_color,
                                 title=f"Scatter — {scatter_x} vs {scatter_y} by {scatter_color}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need at least 2 numeric columns")

    with tab4:
        st.markdown("#### 📉 Line Chart")
        if numeric_cols_viz:
            col1, col2 = st.columns(2)
            with col1:
                line_x = st.selectbox("X Axis", options=df.columns.tolist(), key="line_x")
            with col2:
                line_y = st.selectbox("Y Axis", options=numeric_cols_viz, key="line_y")
            fig = px.line(df, x=line_x, y=line_y, title=f"Line Chart — {line_y} over {line_x}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No numeric columns available")

    with tab5:
        st.markdown("#### 📊 Bar Chart")
        if cat_cols_viz and numeric_cols_viz:
            col1, col2 = st.columns(2)
            with col1:
                bar_x = st.selectbox("X Axis (Categorical)", options=cat_cols_viz, key="bar_x")
            with col2:
                bar_y = st.selectbox("Y Axis (Numeric)", options=numeric_cols_viz, key="bar_y")
            bar_agg = st.selectbox("Aggregation", options=["mean", "sum", "count", "median"], key="bar_agg")
            bar_data = df.groupby(bar_x)[bar_y].agg(bar_agg).reset_index()
            fig = px.bar(bar_data, x=bar_x, y=bar_y, color=bar_x,
                         title=f"Bar Chart — {bar_agg.title()} of {bar_y} by {bar_x}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need at least one categorical and one numeric column")

    with tab6:
        st.markdown("#### 🥧 Pie Chart")
        if cat_cols_viz:
            pie_col = st.selectbox("Select Categorical Column", options=cat_cols_viz, key="pie_col")
            pie_data = df[pie_col].value_counts().reset_index()
            pie_data.columns = [pie_col, "Count"]
            if len(pie_data) > 15:
                st.warning("⚠️ Too many categories — showing top 15 only")
                pie_data = pie_data.head(15)
            fig = px.pie(pie_data, names=pie_col, values="Count",
                         title=f"Pie Chart — {pie_col} Distribution")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No categorical columns available")

    with tab7:
        st.markdown("#### 🔔 Distribution Plot")
        if numeric_cols_viz:
            dist_col = st.selectbox("Select Column", options=numeric_cols_viz, key="dist_col")
            dist_data = df[dist_col].dropna()
            fig = ff.create_distplot([dist_data.tolist()], group_labels=[dist_col],
                                     show_hist=True, show_rug=False)
            fig.update_layout(title=f"Distribution Plot — {dist_col}")
            st.plotly_chart(fig, use_container_width=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Skewness", round(dist_data.skew(), 4))
            with col2:
                st.metric("Kurtosis", round(dist_data.kurtosis(), 4))
            with col3:
                st.metric("Std Dev", round(dist_data.std(), 4))
        else:
            st.info("No numeric columns available")

    with tab8:
        st.markdown("#### 🌡️ Correlation Heatmap")
        if len(numeric_cols_viz) >= 2:
            corr_matrix = df[numeric_cols_viz].corr().round(2)
            fig = px.imshow(corr_matrix, text_auto=True, color_continuous_scale="RdBu_r",
                            title="Correlation Heatmap", aspect="auto")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need at least 2 numeric columns")

    st.divider()

    # ══════════════════════════════════════════
    # FUNCTION 11 — Correlation Analysis
    # ══════════════════════════════════════════
    st.subheader("🔗 Correlation Analysis")

    numeric_cols_corr = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    if len(numeric_cols_corr) < 2:
        st.warning("⚠️ Need at least 2 numeric columns for correlation analysis")
    else:
        corr_method = st.selectbox(
            "Correlation Method",
            options=["pearson", "spearman", "kendall"],
            key="corr_method",
            help="Pearson: linear | Spearman: rank-based | Kendall: ordinal"
        )
        corr_matrix = df[numeric_cols_corr].corr(method=corr_method).round(3)

        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("#### 📋 Correlation Matrix")
            st.dataframe(corr_matrix, use_container_width=True)
        with col2:
            st.markdown("#### 🌡️ Heatmap")
            fig = px.imshow(corr_matrix, text_auto=True, color_continuous_scale="RdBu_r",
                            title=f"{corr_method.title()} Correlation Heatmap", aspect="auto")
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### 🏆 Top Correlated Pairs")
        corr_pairs = corr_matrix.unstack().reset_index()
        corr_pairs.columns = ["Column 1", "Column 2", "Correlation"]
        corr_pairs = corr_pairs[corr_pairs["Column 1"] != corr_pairs["Column 2"]]
        corr_pairs["Abs Correlation"] = corr_pairs["Correlation"].abs()
        corr_pairs = corr_pairs.drop_duplicates(subset=["Abs Correlation"])
        corr_pairs = corr_pairs.sort_values("Abs Correlation", ascending=False).head(10)
        st.dataframe(corr_pairs[["Column 1", "Column 2", "Correlation"]].reset_index(drop=True),
                     use_container_width=True, hide_index=True)

    st.divider()

    # ══════════════════════════════════════════
    # OPTIONAL — Column-wise Insights
    # ══════════════════════════════════════════
    st.subheader("🧠 Column-wise Insights")

    insight_col = st.selectbox("Select a Column to Inspect", options=df.columns.tolist(), key="insight_col")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Data Type", str(df[insight_col].dtype))
    with col2:
        st.metric("Missing Values", df[insight_col].isnull().sum())
    with col3:
        st.metric("Unique Values", df[insight_col].nunique())
    with col4:
        st.metric("Missing %", f"{round(df[insight_col].isnull().sum()/len(df)*100, 2)}%")

    if df[insight_col].dtype in ['float64', 'int64']:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Mean", round(df[insight_col].mean(), 3))
        with col2:
            st.metric("Median", round(df[insight_col].median(), 3))
        with col3:
            st.metric("Std Dev", round(df[insight_col].std(), 3))
        with col4:
            st.metric("Skewness", round(df[insight_col].skew(), 3))
        fig = px.histogram(df, x=insight_col, title=f"Distribution of {insight_col}",
                           color_discrete_sequence=["#636EFA"])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown("**Top 10 Value Counts:**")
        val_counts = df[insight_col].value_counts().head(10).reset_index()
        val_counts.columns = [insight_col, "Count"]
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(val_counts, use_container_width=True, hide_index=True)
        with col2:
            fig = px.bar(val_counts, x=insight_col, y="Count",
                         title=f"Top Values in {insight_col}", color=insight_col)
            st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ══════════════════════════════════════════
    # OPTIONAL — Data Profiling Dashboard
    # ══════════════════════════════════════════
    st.subheader("📋 Data Profiling Dashboard")
    st.markdown("Generates a comprehensive automated EDA report for your dataset.")
    st.warning("⚠️ This may take 15–30 seconds depending on dataset size.")

    if st.button("🚀 Generate Profiling Report", type="primary", key="profile_btn"):
        try:
            from ydata_profiling import ProfileReport
            with st.spinner("Generating report... please wait"):
                profile = ProfileReport(df, title="DataSmith Profiling Report", explorative=True)
                profile_html = profile.to_html()
            st.success("✅ Report generated successfully!")
            st.download_button(
                label="⬇️ Download Full HTML Report",
                data=profile_html,
                file_name="datasmith_profile_report.html",
                mime="text/html",
                use_container_width=True
            )
            st.components.v1.html(profile_html, height=800, scrolling=True)
        except Exception as e:
            st.error(f"❌ Profiling failed: {e}")

    st.divider()

    # ══════════════════════════════════════════
    # FUNCTION 12 — Export Dataset
    # ══════════════════════════════════════════
    st.subheader("💾 Export Dataset")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Rows", df.shape[0])
    with col2:
        st.metric("Current Columns", df.shape[1])
    with col3:
        original_rows = st.session_state['original_df'].shape[0]
        st.metric("Rows Removed", original_rows - df.shape[0])

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download as CSV",
            data=csv_data,
            file_name=f"datasmith_cleaned_{filename.split('.')[0]}.csv",
            mime="text/csv",
            use_container_width=True
        )
    with col2:
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Cleaned Data')
        excel_data = excel_buffer.getvalue()
        st.download_button(
            label="⬇️ Download as Excel",
            data=excel_data,
            file_name=f"datasmith_cleaned_{filename.split('.')[0]}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    st.markdown("---")
    st.caption("💡 Use the **Reset** button in the sidebar to restore your original dataset anytime.")

else:
    st.info("👆 Please upload a CSV or Excel file to get started.")

    st.divider()

    # ══════════════════════════════════════════
    # ABOUT THE DEVELOPER
    # ══════════════════════════════════════════
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

        This app lets you explore, clean, transform, and visualize your dataset interactively,
        so you can confidently feed it into any ML algorithm without worrying about
        missing values, outliers, or unscaled features.

        
        """)

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🏛️ **Institution**\nIIT Delhi")
    with col2:
        st.info("💡 **Interests**\nMachine Learning & Tech")
    with col3:
        st.info("🛠️ **Built With**\nPython & Streamlit")