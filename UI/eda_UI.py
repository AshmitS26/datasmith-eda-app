import streamlit as st
import plotly.express as px
from logic.eda import DataEDA


def data_statistics(df):
    st.subheader("🔬 Dataset Statistics and Analysis")

    eda = DataEDA()

    tab1, tab2, tab3 = st.tabs(["Missing Values", "Unique Values", "Descriptive Statistics"])

    with tab1:
        st.markdown("#### 🚨 Missing Values Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Missing Values", eda.get_total_missing(df))
        with col2:
            st.metric("Columns with Missing Values", eda.get_missing_col_count(df))
        st.dataframe(eda.get_missing_stats(df), use_container_width=True, hide_index=True)

    with tab2:
        st.markdown("#### 🔢 Unique Values Per Column")
        st.dataframe(eda.get_unique_stats(df), use_container_width=True, hide_index=True)

    with tab3:
        st.markdown("#### 📊 Descriptive Statistics")
        st.markdown("Numeric columns only")
        st.dataframe(eda.get_descriptive_stats(df), use_container_width=True)


def data_quality(df):
    st.subheader("🛡️ Data Quality Summary")

    eda = DataEDA()

    constant_cols = eda.get_constant_columns(df)
    quality_score = eda.get_quality_score(df)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Missing Cells", eda.get_total_missing(df))
    with col2:
        st.metric("Duplicate Rows", eda.get_duplicate_count(df))
    with col3:
        st.metric("Constant Columns", len(constant_cols))
    with col4:
        st.metric("Quality Score", f"{quality_score}%")

    if len(constant_cols) > 0:
        st.warning(f"⚠️ Constant columns detected: {', '.join(constant_cols)}")
    else:
        st.success("✅ No constant columns found")


def data_correlation(df):
    st.subheader("🔗 Correlation Analysis")

    eda = DataEDA()
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    if len(numeric_cols) < 2:
        st.warning("⚠️ Need at least 2 numeric columns for correlation analysis")
    else:
        corr_method = st.selectbox(
            "Correlation Method",
            options=["pearson", "spearman", "kendall"],
            key="corr_method",
            help="Pearson: linear | Spearman: rank-based | Kendall: ordinal"
        )
        corr_matrix = eda.get_correlation(df, corr_method)

        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("#### 📋 Correlation Matrix")
            st.dataframe(corr_matrix, use_container_width=True)
        with col2:
            st.markdown("#### 🌡️ Heatmap")
            fig = px.imshow(
                corr_matrix, text_auto=True,
                color_continuous_scale="RdBu_r",
                title=f"{corr_method.title()} Correlation Heatmap",
                aspect="auto"
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### 🏆 Top Correlated Pairs")
        top_pairs = eda.get_top_correlated_pairs(corr_matrix)
        st.dataframe(
            top_pairs[["Column 1", "Column 2", "Correlation"]].reset_index(drop=True),
            use_container_width=True, hide_index=True
        )


def data_insight(df):
    st.subheader("🧠 Column-wise Insights")

    eda = DataEDA()
    insight_col = st.selectbox(
        "Select a Column to Inspect",
        options=df.columns.tolist(),
        key="insight_col"
    )
    info = eda.get_column_insights(df, insight_col)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Data Type", info["dtype"])
    with col2:
        st.metric("Missing Values", info["missing"])
    with col3:
        st.metric("Unique Values", info["unique"])
    with col4:
        st.metric("Missing %", f"{info['missing_pct']}%")

    if df[insight_col].dtype in ['float64', 'int64']:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Mean", info["mean"])
        with col2:
            st.metric("Median", info["median"])
        with col3:
            st.metric("Std Dev", info["std"])
        with col4:
            st.metric("Skewness", info["skewness"])
        fig = px.histogram(
            df, x=insight_col,
            title=f"Distribution of {insight_col}",
            color_discrete_sequence=["#636EFA"]
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown("**Top 10 Value Counts:**")
        val_counts = info["value_counts"]
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(val_counts, use_container_width=True, hide_index=True)
        with col2:
            fig = px.bar(
                val_counts, x=insight_col, y="Count",
                title=f"Top Values in {insight_col}",
                color=insight_col
            )
            st.plotly_chart(fig, use_container_width=True)