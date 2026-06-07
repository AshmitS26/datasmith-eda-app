import streamlit as st
import pandas as pd
from logic.data_cleaner import DataCleaner
from UI.sidebar import log_transformation


def data_cleaning(df):
    st.session_state['current_section'] = 'cleaning'
    st.subheader("🧹 Data Cleaning")

    cleaner = DataCleaner()
    tab1, tab2 = st.tabs(["Missing Value Treatment", "Duplicate Rows"])

    with tab1:
        st.markdown("#### 🩹 Handle Missing Values")
        missing_cols_list = cleaner.get_missing_cols(df)

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
                if method == "Mean":
                    if df[selected_col].dtype in ['float64', 'int64']:
                        df = cleaner.fill_mean(df, selected_col)
                    else:
                        st.error("❌ Mean can only be applied to numeric columns")
                elif method == "Median":
                    if df[selected_col].dtype in ['float64', 'int64']:
                        df = cleaner.fill_median(df, selected_col)
                    else:
                        st.error("❌ Median can only be applied to numeric columns")
                elif method == "Mode":
                    df = cleaner.fill_mode(df, selected_col)
                elif method == "Forward Fill":
                    df = cleaner.fill_forward(df, selected_col)
                elif method == "Backward Fill":
                    df = cleaner.fill_backward(df, selected_col)
                elif method == "Custom Value":
                    if custom_value:
                        df = cleaner.fill_custom(df, selected_col, custom_value)
                    else:
                        st.error("❌ Please enter a custom value")
                elif method == "Remove Rows":
                    df = cleaner.remove_missing_rows(df, selected_col)

                if cleaner.last_action:
                    log_transformation(cleaner.last_action)
                    st.success(f"✅ {cleaner.last_action}")
                    st.session_state['df'] = df
                    st.dataframe(df.astype(str), use_container_width=True)

    with tab2:
        st.markdown("#### 🔁 Duplicate Row Handler")
        dup_count = cleaner.get_duplicate_count(df)

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
                df = cleaner.remove_duplicates(df)
                log_transformation(cleaner.last_action)
                st.session_state['df'] = df
                st.success(f"✅ {cleaner.last_action}")
                st.rerun()

    return df