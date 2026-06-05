import streamlit as st
import plotly.express as px


def show_correlation(df):
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