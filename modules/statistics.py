import streamlit as st
import pandas as pd


def show_statistics(df):
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