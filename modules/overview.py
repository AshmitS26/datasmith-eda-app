import streamlit as st
import pandas as pd


def show_overview(df, filename):
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