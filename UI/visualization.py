import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from logic.data_visualization import DataVisualization


def data_visualization(df):
    st.subheader("📈 Visualization Dashboard")

    viz = DataVisualization()

    numeric_cols = viz.get_numeric_columns(df)
    cat_cols = viz.get_categorical_columns(df)

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "Histogram", "Box Plot", "Scatter Plot", "Line Chart",
        "Bar Chart", "Pie Chart", "Distribution Plot", "3D Visualization"
    ])

    # ── TAB 1 ── Histogram
    with tab1:
        st.markdown("#### 📊 Histogram")
        if numeric_cols:
            hist_col = st.selectbox("Select Column", options=numeric_cols, key="hist_col")
            hist_bins = st.slider("Number of Bins", min_value=5, max_value=100, value=30, key="hist_bins")
            fig = px.histogram(df, x=hist_col, nbins=hist_bins,
                               title=f"Histogram — {hist_col}",
                               color_discrete_sequence=["#636EFA"])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No numeric columns available")

    # ── TAB 2 ── Box Plot
    with tab2:
        st.markdown("#### 📦 Box Plot")
        if numeric_cols:
            box_col = st.selectbox("Select Numeric Column", options=numeric_cols, key="box_col")
            box_group = st.selectbox("Group By (optional)", options=["None"] + cat_cols, key="box_group")
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
        if len(numeric_cols) >= 2:
            col1, col2, col3 = st.columns(3)
            with col1:
                scatter_x = st.selectbox("X Axis", options=numeric_cols, key="scatter_x")
            with col2:
                scatter_y = st.selectbox("Y Axis", options=numeric_cols, index=1, key="scatter_y")
            with col3:
                scatter_color = st.selectbox("Color By (optional)", options=["None"] + cat_cols, key="scatter_color")
            if scatter_color == "None":
                fig = px.scatter(df, x=scatter_x, y=scatter_y,
                                 title=f"Scatter — {scatter_x} vs {scatter_y}")
            else:
                fig = px.scatter(df, x=scatter_x, y=scatter_y, color=scatter_color,
                                 title=f"Scatter — {scatter_x} vs {scatter_y} by {scatter_color}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need at least 2 numeric columns")

    # ── TAB 4 ── Line Chart
    with tab4:
        st.markdown("#### 📉 Line Chart")
        if numeric_cols:
            col1, col2 = st.columns(2)
            with col1:
                line_x = st.selectbox("X Axis", options=viz.get_all_columns(df), key="line_x")
            with col2:
                line_y = st.selectbox("Y Axis", options=numeric_cols, key="line_y")
            fig = px.line(df, x=line_x, y=line_y,
                          title=f"Line Chart — {line_y} over {line_x}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No numeric columns available")

    # ── TAB 5 ── Bar Chart
    with tab5:
        st.markdown("#### 📊 Bar Chart")
        if cat_cols and numeric_cols:
            col1, col2 = st.columns(2)
            with col1:
                bar_x = st.selectbox("X Axis (Categorical)", options=cat_cols, key="bar_x")
            with col2:
                bar_y = st.selectbox("Y Axis (Numeric)", options=numeric_cols, key="bar_y")
            bar_agg = st.selectbox("Aggregation", options=["mean", "sum", "count", "median"], key="bar_agg")
            bar_data = viz.get_bar_data(df, bar_x, bar_y, bar_agg)
            fig = px.bar(bar_data, x=bar_x, y=bar_y, color=bar_x,
                         title=f"Bar Chart — {bar_agg.title()} of {bar_y} by {bar_x}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need at least one categorical and one numeric column")

    # ── TAB 6 ── Pie Chart
    with tab6:
        st.markdown("#### 🥧 Pie Chart")
        if cat_cols:
            pie_col = st.selectbox("Select Categorical Column", options=cat_cols, key="pie_col")
            pie_data, truncated = viz.get_pie_data(df, pie_col)
            if truncated:
                st.warning("⚠️ Too many categories — showing top 15 only")
            fig = px.pie(pie_data, names=pie_col, values="Count",
                         title=f"Pie Chart — {pie_col} Distribution")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No categorical columns available")

    # ── TAB 7 ── Distribution Plot
    with tab7:
        st.markdown("#### 🔔 Distribution Plot")
        if numeric_cols:
            dist_col = st.selectbox("Select Column", options=numeric_cols, key="dist_col")
            stats = viz.get_distribution_stats(df, dist_col)
            fig = ff.create_distplot([stats["data"]], group_labels=[dist_col],
                                     show_hist=True, show_rug=False)
            fig.update_layout(title=f"Distribution Plot — {dist_col}")
            st.plotly_chart(fig, use_container_width=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Skewness", stats["skewness"])
            with col2:
                st.metric("Kurtosis", stats["kurtosis"])
            with col3:
                st.metric("Std Dev", stats["std"])
        else:
            st.info("No numeric columns available")

    # ── TAB 8 ── 3D Visualization
    with tab8:
        st.markdown("#### 🌐 3D Visualization")
        st.info("Explore multidimensional relationships using interactive 3D plots.")

        if len(numeric_cols) < 2:
            st.warning("⚠️ Need at least 2 numeric columns for 3D visualization")
        else:
            viz_type = st.selectbox("Select 3D Chart Type", options=[
                "3D Scatter Plot",
                "3D Line Plot",
                "3D Surface Plot"
            ], key="viz_3d_type")

            if viz_type == "3D Scatter Plot":
                st.markdown("##### 🔵 3D Scatter Plot")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    x_col = st.selectbox("X Axis", options=numeric_cols, key="3d_x")
                with col2:
                    y_col = st.selectbox("Y Axis", options=numeric_cols,
                                         index=min(1, len(numeric_cols)-1), key="3d_y")
                with col3:
                    z_col = st.selectbox("Z Axis", options=numeric_cols,
                                         index=min(2, len(numeric_cols)-1), key="3d_z")
                with col4:
                    color_col = st.selectbox("Color By (optional)",
                                             options=["None"] + cat_cols, key="3d_color")
                if color_col == "None":
                    fig = px.scatter_3d(df, x=x_col, y=y_col, z=z_col,
                                        title=f"3D Scatter — {x_col} vs {y_col} vs {z_col}",
                                        opacity=0.7)
                else:
                    fig = px.scatter_3d(df, x=x_col, y=y_col, z=z_col,
                                        color=color_col,
                                        title=f"3D Scatter — {x_col} vs {y_col} vs {z_col}",
                                        opacity=0.7)
                fig.update_traces(marker=dict(size=4))
                st.plotly_chart(fig, use_container_width=True)

            elif viz_type == "3D Line Plot":
                st.markdown("##### 📈 3D Line Plot")
                col1, col2, col3 = st.columns(3)
                with col1:
                    x_col = st.selectbox("X Axis", options=numeric_cols, key="3dl_x")
                with col2:
                    y_col = st.selectbox("Y Axis", options=numeric_cols,
                                         index=min(1, len(numeric_cols)-1), key="3dl_y")
                with col3:
                    z_col = st.selectbox("Z Axis", options=numeric_cols,
                                         index=min(2, len(numeric_cols)-1), key="3dl_z")
                fig = px.line_3d(df, x=x_col, y=y_col, z=z_col,
                                 title=f"3D Line — {x_col} vs {y_col} vs {z_col}")
                st.plotly_chart(fig, use_container_width=True)

            elif viz_type == "3D Surface Plot":
                st.markdown("##### 🏔️ 3D Surface Plot")
                st.caption("Surface plot uses correlation matrix of numeric columns as Z axis.")
                corr, cols = viz.get_surface_data(df)
                fig = go.Figure(data=[go.Surface(
                    z=corr,
                    x=cols,
                    y=cols,
                    colorscale="RdBu",
                    reversescale=True
                )])
                fig.update_layout(
                    title="3D Surface — Correlation Matrix",
                    scene=dict(
                        xaxis_title="Columns",
                        yaxis_title="Columns",
                        zaxis_title="Correlation"
                    ),
                    height=600
                )
                st.plotly_chart(fig, use_container_width=True)
                st.caption("Each cell shows correlation between two numeric columns as a 3D surface.")