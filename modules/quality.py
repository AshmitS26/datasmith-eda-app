import streamlit as st


def show_quality(df):
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