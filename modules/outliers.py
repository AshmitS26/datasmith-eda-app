import streamlit as st
import numpy as np
import plotly.express as px
from scipy import stats
from datetime import datetime


def log_transformation(action):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state['transformation_log'].append(f"[{timestamp}] {action}")


def show_outliers(df):
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

    return df