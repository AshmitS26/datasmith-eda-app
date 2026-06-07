import streamlit as st
from logic.data_filtering import DataFilter


def data_filtering(df):
    st.subheader("🔍 Data Filtering and Exploration")

    filter_obj = DataFilter()

    search_term = st.text_input("🔎 Search across all columns", placeholder="Type to search any value...")

    tab1, tab2, tab3 = st.tabs(["Numeric Filter", "Categorical Filter", "Date Filter"])

    with tab1:
        st.markdown("#### 🔢 Filter Numeric Columns")
        num_cols = filter_obj.get_numeric_columns(df)
        if len(num_cols) == 0:
            st.info("No numeric columns available")
        else:
            num_filter_col = st.selectbox("Select Numeric Column", options=num_cols, key="num_fcol")
            col_min = float(df[num_filter_col].min())
            col_max = float(df[num_filter_col].max())
            num_range = st.slider(
                f"Select Range for {num_filter_col}",
                min_value=col_min, max_value=col_max,
                value=(col_min, col_max), key="num_range"
            )
            filtered_df = filter_obj.filter_numeric(df, num_filter_col, num_range[0], num_range[1])
            st.markdown(f"**Rows matching filter:** {len(filtered_df)}")
            st.dataframe(filtered_df.astype(str), use_container_width=True)

    with tab2:
        st.markdown("#### 🏷️ Filter Categorical Columns")
        cat_cols = filter_obj.get_categorical_columns(df)
        if len(cat_cols) == 0:
            st.info("No categorical columns available")
        else:
            cat_filter_col = st.selectbox("Select Categorical Column", options=cat_cols, key="cat_fcol")
            unique_vals = df[cat_filter_col].dropna().unique().tolist()
            selected_vals = st.multiselect(
                f"Select values for {cat_filter_col}",
                options=unique_vals, default=unique_vals, key="cat_vals"
            )
            cat_filtered = filter_obj.filter_categorical(df, cat_filter_col, selected_vals)
            st.markdown(f"**Rows matching filter:** {len(cat_filtered)}")
            st.dataframe(cat_filtered.astype(str), use_container_width=True)

    with tab3:
        st.markdown("#### 📅 Filter Date Columns")
        date_cols = filter_obj.get_date_columns(df)
        if len(date_cols) == 0:
            st.info("No date columns detected. Convert column dtype first using Data Transformation.")
        else:
            date_col_sel = st.selectbox("Select Date Column", options=date_cols, key="date_fcol")
            try:
                import pandas as pd
                df[date_col_sel] = pd.to_datetime(df[date_col_sel])
                min_date = df[date_col_sel].min().date()
                max_date = df[date_col_sel].max().date()
                date_range = st.date_input("Select Date Range", value=(min_date, max_date), key="date_range")
                if len(date_range) == 2:
                    date_filtered = filter_obj.filter_date(df, date_col_sel, date_range[0], date_range[1])
                    st.markdown(f"**Rows in range:** {len(date_filtered)}")
                    st.dataframe(date_filtered.astype(str), use_container_width=True)
            except Exception as e:
                st.error(f"❌ Could not parse dates: {e}")

    if search_term:
        st.markdown(f"#### 🔎 Search Results for: `{search_term}`")
        search_results = filter_obj.search_all_columns(df, search_term)
        st.markdown(f"**{len(search_results)} rows** found")
        st.dataframe(search_results.astype(str), use_container_width=True)