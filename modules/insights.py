import streamlit as st
import plotly.express as px


def show_insights(df):
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