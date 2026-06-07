import streamlit as st
from logic.data_scaling import DataScaler
from UI.sidebar import log_transformation





def data_scaling(df):
    st.subheader("📏 Feature Scaling")

    scaler = DataScaler()
    numeric_cols = scaler.get_numeric_columns(df)

    if len(numeric_cols) == 0:
        st.warning("⚠️ No numeric columns found for scaling")
    else:
        col1, col2 = st.columns(2)
        with col1:
            scale_cols = st.multiselect(
                "Select Columns to Scale",
                options=numeric_cols,
                key="scale_cols"
            )
        with col2:
            scale_method = st.selectbox(
                "Select Scaling Method",
                options=[
                    "Standard Scaler (Z-score)",
                    "MinMax Scaler (0 to 1)",
                    "Robust Scaler (outlier resistant)"
                ],
                key="scale_method"
            )

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
                df = scaler.scale(df, scale_cols, scale_method)
                st.session_state['df'] = df
                log_transformation(f"Applied {scale_method} on columns: {', '.join(scale_cols)}")
                st.success(f"✅ **{scale_method}** applied on {len(scale_cols)} column(s)")
                st.dataframe(scaler.get_scaled_summary(df, scale_cols), use_container_width=True)

    return df