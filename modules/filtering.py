import streamlit as st
import pandas as pd


def show_filtering(df):
    st.subheader("🔍 Data Filtering and Exploration")

    search_term = st.text_input("🔎 Search across all columns", placeholder="Type to search any value...")

    tab1, tab2, tab3 = st.tabs(["Numeric Filter", "Categorical Filter", "Date Filter"])

    # ── TAB 1 ── Numeric Filter
    with tab1:
        st.markdown("#### 🔢 Filter Numeric Columns")
        num_cols_filter = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        if len(num_cols_filter) == 0:
            st.info("No numeric columns available")
        else:
            num_filter_col = st.selectbox("Select Numeric Column", options=num_cols_filter, key="num_fcol")
            col_min = float(df[num_filter_col].min())
            col_max = float(df[num_filter_col].max())
            num_range = st.slider(
                f"Select Range for {num_filter_col}",
                min_value=col_min, max_value=col_max,
                value=(col_min, col_max), key="num_range"
            )
            filtered_df = df[
                (df[num_filter_col] >= num_range[0]) &
                (df[num_filter_col] <= num_range[1])
            ]
            st.markdown(f"**Rows matching filter:** {len(filtered_df)}")
            st.dataframe(filtered_df.astype(str), use_container_width=True)

    # ── TAB 2 ── Categorical Filter
    with tab2:
        st.markdown("#### 🏷️ Filter Categorical Columns")
        cat_cols_filter = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
        if len(cat_cols_filter) == 0:
            st.info("No categorical columns available")
        else:
            cat_filter_col = st.selectbox("Select Categorical Column", options=cat_cols_filter, key="cat_fcol")
            unique_cat_vals = df[cat_filter_col].dropna().unique().tolist()
            selected_vals = st.multiselect(
                f"Select values for {cat_filter_col}",
                options=unique_cat_vals,
                default=unique_cat_vals,
                key="cat_vals"
            )
            cat_filtered = df[df[cat_filter_col].isin(selected_vals)]
            st.markdown(f"**Rows matching filter:** {len(cat_filtered)}")
            st.dataframe(cat_filtered.astype(str), use_container_width=True)

    # ── TAB 3 ── Date Filter
    with tab3:
        st.markdown("#### 📅 Filter Date Columns")
        date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        possible_date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
        all_date_cols = list(set(date_cols + possible_date_cols))
        if len(all_date_cols) == 0:
            st.info("No date columns detected. Convert column dtype first using Data Transformation.")
        else:
            date_col_sel = st.selectbox("Select Date Column", options=all_date_cols, key="date_fcol")
            try:
                df[date_col_sel] = pd.to_datetime(df[date_col_sel])
                min_date = df[date_col_sel].min().date()
                max_date = df[date_col_sel].max().date()
                date_range = st.date_input("Select Date Range", value=(min_date, max_date), key="date_range")
                if len(date_range) == 2:
                    date_filtered = df[
                        (df[date_col_sel].dt.date >= date_range[0]) &
                        (df[date_col_sel].dt.date <= date_range[1])
                    ]
                    st.markdown(f"**Rows in range:** {len(date_filtered)}")
                    st.dataframe(date_filtered.astype(str), use_container_width=True)
            except Exception as e:
                st.error(f"❌ Could not parse dates: {e}")

    # ── Global Search ──
    if search_term:
        st.markdown(f"#### 🔎 Search Results for: `{search_term}`")
        mask = df.astype(str).apply(lambda col: col.str.contains(search_term, case=False, na=False)).any(axis=1)
        search_results = df[mask]
        st.markdown(f"**{len(search_results)} rows** found")
        st.dataframe(search_results.astype(str), use_container_width=True)