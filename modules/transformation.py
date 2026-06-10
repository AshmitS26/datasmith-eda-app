import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from datetime import datetime


def log_transformation(action):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state['transformation_log'].append(f"[{timestamp}] {action}")


def show_transformation(df):
    st.subheader("⚙️ Data Transformation")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Label Encoding", "One-Hot Encoding", "Ordinal Encoding",
        "Datatype Conversion", "Rename / Drop Columns"
    ])

    # ── TAB 1 ── Label Encoding
    with tab1:
        st.markdown("#### 🏷️ Label Encoding")
        st.info("Assigns a unique number to each category. Best for **target/output columns** only.")
        cat_cols_le = df.select_dtypes(include=['object', 'category']).columns.tolist()
        if len(cat_cols_le) == 0:
            st.success("✅ No categorical columns found")
        else:
            selected_le_col = st.selectbox("Select Column", options=cat_cols_le, key="le_col")
            st.markdown(f"**Unique values:** {', '.join(map(str, df[selected_le_col].dropna().unique()))}")
            if st.button("Apply Label Encoding", type="primary", key="le_btn"):
                le = LabelEncoder()
                df[selected_le_col] = le.fit_transform(df[selected_le_col].astype(str))
                st.session_state['df'] = df
                log_transformation(f"Applied Label Encoding on '{selected_le_col}'")
                st.success(f"✅ Label Encoding applied on **{selected_le_col}**")
                st.dataframe(df[[selected_le_col]], use_container_width=True)

    # ── TAB 2 ── One-Hot Encoding
    with tab2:
        st.markdown("#### 🔥 One-Hot Encoding")
        st.info("Creates a new column for each category. Best for **input features** with no order.")
        cat_cols_ohe = df.select_dtypes(include=['object', 'category']).columns.tolist()
        if len(cat_cols_ohe) == 0:
            st.success("✅ No categorical columns found")
        else:
            selected_ohe_col = st.selectbox("Select Column", options=cat_cols_ohe, key="ohe_col")
            unique_count = df[selected_ohe_col].nunique()
            st.markdown(f"**Unique values:** {unique_count} → will create **{unique_count} new columns**")
            if unique_count > 15:
                st.warning(f"⚠️ {unique_count} unique values will create many columns.")
            drop_first = st.checkbox("Drop first column (avoid dummy variable trap)", value=True, key="ohe_drop")
            if st.button("Apply One-Hot Encoding", type="primary", key="ohe_btn"):
                df = pd.get_dummies(df, columns=[selected_ohe_col], drop_first=drop_first)
                st.session_state['df'] = df
                log_transformation(f"Applied One-Hot Encoding on '{selected_ohe_col}'")
                st.success(f"✅ One-Hot Encoding applied. New shape: {df.shape}")
                st.dataframe(df.astype(str), use_container_width=True)

    # ── TAB 3 ── Ordinal Encoding
    with tab3:
        st.markdown("#### 📊 Ordinal Encoding")
        st.info("Assigns numbers based on a meaningful order you define.")
        cat_cols_oe = df.select_dtypes(include=['object', 'category']).columns.tolist()
        if len(cat_cols_oe) == 0:
            st.success("✅ No categorical columns found")
        else:
            selected_oe_col = st.selectbox("Select Column", options=cat_cols_oe, key="oe_col")
            unique_vals_oe = df[selected_oe_col].dropna().unique().tolist()
            st.markdown(f"**Unique values found:** {', '.join(map(str, unique_vals_oe))}")
            order_input = st.text_input(
                "Enter values in order (lowest → highest), comma separated",
                value=', '.join(map(str, unique_vals_oe)), key="oe_order"
            )
            if st.button("Apply Ordinal Encoding", type="primary", key="oe_btn"):
                order_list = [x.strip() for x in order_input.split(',')]
                order_map = {val: idx for idx, val in enumerate(order_list)}
                df[selected_oe_col] = df[selected_oe_col].map(order_map)
                st.session_state['df'] = df
                log_transformation(f"Applied Ordinal Encoding on '{selected_oe_col}'")
                st.success(f"✅ Ordinal Encoding applied on **{selected_oe_col}**")
                st.dataframe(
                    pd.DataFrame({"Category": list(order_map.keys()), "Encoded Value": list(order_map.values())}),
                    use_container_width=True, hide_index=True
                )

    # ── TAB 4 ── Datatype Conversion
    with tab4:
        st.markdown("#### 🔄 Datatype Conversion")
        col1, col2 = st.columns(2)
        with col1:
            selected_dtype_col = st.selectbox("Select Column", options=df.columns.tolist(), key="dtype_col")
            st.markdown(f"**Current dtype:** `{df[selected_dtype_col].dtype}`")
        with col2:
            target_dtype = st.selectbox("Convert To", options=["int64", "float64", "str", "bool"], key="dtype_target")
        if st.button("Convert Datatype", type="primary", key="dtype_btn"):
            try:
                df[selected_dtype_col] = df[selected_dtype_col].astype(target_dtype)
                st.session_state['df'] = df
                log_transformation(f"Converted '{selected_dtype_col}' to {target_dtype}")
                st.success(f"✅ **{selected_dtype_col}** converted to `{target_dtype}`")
            except Exception as e:
                st.error(f"❌ Conversion failed: {e}")

    # ── TAB 5 ── Rename / Drop Columns
    with tab5:
        st.markdown("#### ✏️ Rename or Drop Columns")
        inner_tab1, inner_tab2 = st.tabs(["Rename Column", "Drop Columns"])
        with inner_tab1:
            col1, col2 = st.columns(2)
            with col1:
                col_to_rename = st.selectbox("Select Column to Rename", options=df.columns.tolist(), key="rename_col")
            with col2:
                new_col_name = st.text_input("Enter New Name", placeholder="e.g. passenger_age", key="rename_new")
            if st.button("Rename Column", type="primary", key="rename_btn"):
                if new_col_name:
                    df = df.rename(columns={col_to_rename: new_col_name})
                    st.session_state['df'] = df
                    log_transformation(f"Renamed column '{col_to_rename}' to '{new_col_name}'")
                    st.success(f"✅ **{col_to_rename}** renamed to **{new_col_name}**")
                    st.rerun()
                else:
                    st.error("❌ Please enter a new column name")
        with inner_tab2:
            cols_to_drop = st.multiselect("Select Columns to Drop", options=df.columns.tolist(), key="drop_cols")
            if cols_to_drop:
                st.warning(f"⚠️ About to drop: {', '.join(cols_to_drop)}")
            if st.button("Drop Selected Columns", type="primary", key="drop_btn"):
                if cols_to_drop:
                    df = df.drop(columns=cols_to_drop)
                    st.session_state['df'] = df
                    log_transformation(f"Dropped columns: {', '.join(cols_to_drop)}")
                    st.success(f"✅ Dropped {len(cols_to_drop)} column(s). New shape: {df.shape}")
                    st.rerun()
                else:
                    st.error("❌ Please select at least one column")

    return df