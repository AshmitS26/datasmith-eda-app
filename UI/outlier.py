import streamlit as st
import plotly.express as px
from logic.outlier_detection import DataOutlier
from UI.sidebar import log_transformation

def data_outlier(df):
    st.subheader("🎯 Outlier Detection and Treatment")

    detector = DataOutlier()
    numeric_cols = detector.get_numeric_columns(df)

    if len(numeric_cols) == 0:
        st.warning("⚠️ No numeric columns found")
    else:
        col1, col2 = st.columns(2)
        with col1:
            outlier_col = st.selectbox("Select Column", options=numeric_cols, key="out_col")
        with col2:
            outlier_method = st.selectbox("Detection Method", options=["IQR Method", "Z-Score Method"], key="out_method")

        if outlier_method == "IQR Method":
            outliers, lower, upper, Q1, Q3, IQR = detector.detect_iqr(df, outlier_col)
            st.markdown(f"**Q1:** {round(Q1,2)} | **Q3:** {round(Q3,2)} | **IQR:** {round(IQR,2)}")
            st.markdown(f"**Lower bound:** {round(lower,2)} | **Upper bound:** {round(upper,2)}")
        else:
            threshold = st.slider("Z-Score Threshold", min_value=1.0, max_value=4.0, value=3.0, step=0.1)
            outliers, outlier_indices = detector.detect_zscore(df, outlier_col, threshold)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Outliers Detected", len(outliers))
        with col2:
            st.metric("Outlier %", f"{detector.get_outlier_percentage(outliers, df)}%")

        fig = px.box(df, y=outlier_col, title=f"Box Plot — {outlier_col}",
                     color_discrete_sequence=["#636EFA"])
        st.plotly_chart(fig, use_container_width=True)

        if len(outliers) > 0:
            st.markdown("**Outlier rows preview:**")
            st.dataframe(outliers.astype(str), use_container_width=True)

            out_action = st.selectbox(
                "Action",
                options=["Remove Outliers", "Cap Outliers (Winsorize)"],
                key="out_action"
            )

            if st.button("Apply Outlier Treatment", type="primary", key="out_btn"):
                if out_action == "Remove Outliers":
                    if outlier_method == "IQR Method":
                        df = detector.remove_iqr(df, outlier_col, lower, upper)
                    else:
                        df = detector.remove_zscore(df, outlier_indices)
                    log_transformation(f"Removed outliers from '{outlier_col}' using {outlier_method}")
                    st.success(f"✅ Outliers removed. New shape: {df.shape}")
                else:
                    if outlier_method == "IQR Method":
                        df = detector.cap_iqr(df, outlier_col, lower, upper)
                    else:
                        df = detector.cap_zscore(df, outlier_col, threshold)
                    log_transformation(f"Capped outliers in '{outlier_col}' using {outlier_method}")
                    st.success(f"✅ Outliers capped in **{outlier_col}**")

                st.session_state['df'] = df
                st.rerun()

    return df