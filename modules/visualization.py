import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff


def show_visualization(df):
    st.subheader("📈 Visualization Dashboard")

    numeric_cols_viz = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    cat_cols_viz = df.select_dtypes(include=['object', 'category']).columns.tolist()

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "Histogram", "Box Plot", "Scatter Plot", "Line Chart",
        "Bar Chart", "Pie Chart", "Distribution Plot", "Correlation Heatmap"
    ])

    # ── TAB 1 ── Histogram
    with tab1:
        st.markdown("#### 📊 Histogram")
        if numeric_cols_viz:
            hist_col = st.selectbox("Select Column", options=numeric_cols_viz, key="hist_col")
            hist_bins = st.slider("Number of Bins", min_value=5, max_value=100, value=30, key="hist_bins")
            fig = px.histogram(df, x=hist_col, nbins=hist_bins, title=f"Histogram — {hist_col}",
                               color_discrete_sequence=["#636EFA"])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No numeric columns available")

    # ── TAB 2 ── Box Plot
    with tab2:
        st.markdown("#### 📦 Box Plot")
        if numeric_cols_viz:
            box_col = st.selectbox("Select Numeric Column", options=numeric_cols_viz, key="box_col")
            box_group = st.selectbox("Group By (optional)", options=["None"] + cat_cols_viz, key="box_group")
            if box_group == "None":
                fig = px.box(df, y=box_col, title=f"Box Plot — {box_col}")
            else:
                fig = px.box(df, x=box_group, y=box_col, color=box_group,
                             title=f"Box Plot — {box_col} by {box_group}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No numeric columns available")

    # ── TAB 3 ── Scatter Plot
    with tab3:
        st.markdown("#### 🔵 Scatter Plot")
        if len(numeric_cols_viz) >= 2:
            col1, col2, col3 = st.columns(3)
            with col1:
                scatter_x = st.selectbox("X Axis", options=numeric_cols_viz, key="scatter_x")
            with col2:
                scatter_y = st.selectbox("Y Axis", options=numeric_cols_viz, index=1, key="scatter_y")
            with col3:
                scatter_color = st.selectbox("Color By (optional)", options=["None"] + cat_cols_viz, key="scatter_color")
            if scatter_color == "None":
                fig = px.scatter(df, x=scatter_x, y=scatter_y, title=f"Scatter — {scatter_x} vs {scatter_y}")
            else:
                fig = px.scatter(df, x=scatter_x, y=scatter_y, color=scatter_color,
                                 title=f"Scatter — {scatter_x} vs {scatter_y} by {scatter_color}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need at least 2 numeric columns")

    # ── TAB 4 ── Line Chart
    with tab4:
        st.markdown("#### 📉 Line Chart")
        if numeric_cols_viz:
            col1, col2 = st.columns(2)
            with col1:
                line_x = st.selectbox("X Axis", options=df.columns.tolist(), key="line_x")
            with col2:
                line_y = st.selectbox("Y Axis", options=numeric_cols_viz, key="line_y")
            fig = px.line(df, x=line_x, y=line_y, title=f"Line Chart — {line_y} over {line_x}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No numeric columns available")

    # ── TAB 5 ── Bar Chart
    with tab5:
        st.markdown("#### 📊 Bar Chart")
        if cat_cols_viz and numeric_cols_viz:
            col1, col2 = st.columns(2)
            with col1:
                bar_x = st.selectbox("X Axis (Categorical)", options=cat_cols_viz, key="bar_x")
            with col2:
                bar_y = st.selectbox("Y Axis (Numeric)", options=numeric_cols_viz, key="bar_y")
            bar_agg = st.selectbox("Aggregation", options=["mean", "sum", "count", "median"], key="bar_agg")
            bar_data = df.groupby(bar_x)[bar_y].agg(bar_agg).reset_index()
            fig = px.bar(bar_data, x=bar_x, y=bar_y, color=bar_x,
                         title=f"Bar Chart — {bar_agg.title()} of {bar_y} by {bar_x}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need at least one categorical and one numeric column")

    # ── TAB 6 ── Pie Chart
    with tab6:
        st.markdown("#### 🥧 Pie Chart")
        if cat_cols_viz:
            pie_col = st.selectbox("Select Categorical Column", options=cat_cols_viz, key="pie_col")
            pie_data = df[pie_col].value_counts().reset_index()
            pie_data.columns = [pie_col, "Count"]
            if len(pie_data) > 15:
                st.warning("⚠️ Too many categories — showing top 15 only")
                pie_data = pie_data.head(15)
            fig = px.pie(pie_data, names=pie_col, values="Count",
                         title=f"Pie Chart — {pie_col} Distribution")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No categorical columns available")

    # ── TAB 7 ── Distribution Plot
    with tab7:
        st.markdown("#### 🔔 Distribution Plot")
        if numeric_cols_viz:
            dist_col = st.selectbox("Select Column", options=numeric_cols_viz, key="dist_col")
            dist_data = df[dist_col].dropna()
            fig = ff.create_distplot([dist_data.tolist()], group_labels=[dist_col],
                                     show_hist=True, show_rug=False)
            fig.update_layout(title=f"Distribution Plot — {dist_col}")
            st.plotly_chart(fig, use_container_width=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Skewness", round(dist_data.skew(), 4))
            with col2:
                st.metric("Kurtosis", round(dist_data.kurtosis(), 4))
            with col3:
                st.metric("Std Dev", round(dist_data.std(), 4))
        else:
            st.info("No numeric columns available")

    # ── TAB 8 ── Correlation Heatmap
    with tab8:
        st.markdown("#### 🌡️ Correlation Heatmap")
        if len(numeric_cols_viz) >= 2:
            corr_matrix = df[numeric_cols_viz].corr().round(2)
            fig = px.imshow(corr_matrix, text_auto=True, color_continuous_scale="RdBu_r",
                            title="Correlation Heatmap", aspect="auto")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need at least 2 numeric columns")