import streamlit as st
import pandas as pd
from datetime import datetime


def log_transformation(action):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state['transformation_log'].append(f"[{timestamp}] {action}")


def show_cleaning(df):
    st.subheader("🧹 Data Cleaning")

    tab1, tab2 = st.tabs(["Missing Value Treatment", "Duplicate Rows"])

    # ── TAB 1 ── Missing Value Treatment
    with tab1:
        st.markdown("#### 🩹 Handle Missing Values")
        missing_cols_list = df.columns[df.isnull().any()].tolist()

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
                if method == "Remove Rows":
                    df = df.dropna(subset=[selected_col])
                    log_transformation(f"Removed rows with missing values in '{selected_col}'")
                    st.success(f"✅ Rows with missing **{selected_col}** removed. New shape: {df.shape}")
                elif method == "Mean":
                    if df[selected_col].dtype in ['float64', 'int64']:
                        fill_val = round(df[selected_col].mean(), 2)
                        df[selected_col] = df[selected_col].fillna(fill_val)
                        log_transformation(f"Filled '{selected_col}' missing values with Mean ({fill_val})")
                        st.success(f"✅ Filled **{selected_col}** with Mean: {fill_val}")
                    else:
                        st.error("❌ Mean can only be applied to numeric columns")
                elif method == "Median":
                    if df[selected_col].dtype in ['float64', 'int64']:
                        fill_val = round(df[selected_col].median(), 2)
                        df[selected_col] = df[selected_col].fillna(fill_val)
                        log_transformation(f"Filled '{selected_col}' missing values with Median ({fill_val})")
                        st.success(f"✅ Filled **{selected_col}** with Median: {fill_val}")
                    else:
                        st.error("❌ Median can only be applied to numeric columns")
                elif method == "Mode":
                    fill_val = df[selected_col].mode()[0]
                    df[selected_col] = df[selected_col].fillna(fill_val)
                    log_transformation(f"Filled '{selected_col}' missing values with Mode ({fill_val})")
                    st.success(f"✅ Filled **{selected_col}** with Mode: {fill_val}")
                elif method == "Forward Fill":
                    df[selected_col] = df[selected_col].ffill()
                    log_transformation(f"Applied Forward Fill on '{selected_col}'")
                    st.success(f"✅ Applied Forward Fill on **{selected_col}**")
                elif method == "Backward Fill":
                    df[selected_col] = df[selected_col].bfill()
                    log_transformation(f"Applied Backward Fill on '{selected_col}'")
                    st.success(f"✅ Applied Backward Fill on **{selected_col}**")
                elif method == "Custom Value":
                    if custom_value:
                        df[selected_col] = df[selected_col].fillna(custom_value)
                        log_transformation(f"Filled '{selected_col}' missing values with custom value '{custom_value}'")
                        st.success(f"✅ Filled **{selected_col}** with: **{custom_value}**")
                    else:
                        st.error("❌ Please enter a custom value")
                st.session_state['df'] = df
                st.dataframe(df.astype(str), use_container_width=True)

    # ── TAB 2 ── Duplicate Rows
    with tab2:
        st.markdown("#### 🔁 Duplicate Row Handler")
        dup_count = df.duplicated().sum()
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
                df = df.drop_duplicates()
                st.session_state['df'] = df
                log_transformation(f"Removed {dup_count} duplicate rows")
                st.success(f"✅ Duplicates removed. New shape: {df.shape}")
                st.rerun()

    return df