import streamlit as st
import pandas as pd
from logic.data_loader import DataLoader
from UI.sidebar import log_transformation


def data_upload():
    st.session_state['current_section'] = 'upload'
    st.subheader("📂 Upload Your Dataset")
    st.markdown("Supported formats: **CSV** and **Excel (.xlsx)**")

    uploaded_file = st.file_uploader(
        label="Drag and drop or click to browse",
        type=["csv", "xlsx"],
        help="Upload a CSV or Excel file to begin analysis",
        key="main_file_uploader"
    )

    if uploaded_file is not None:
        loader = DataLoader()
        df = loader.load_file(uploaded_file)
        info = loader.get_file_info()

        st.session_state['df'] = df
        st.session_state['original_df'] = df.copy()
        st.session_state['filename'] = info['filename']

        if info['filename'] not in st.session_state['file_history']:
            st.session_state['file_history'].append(info['filename'])

        log_transformation(f"Uploaded file: {info['filename']} — Shape: {df.shape}")
        st.success(f"✅ **{info['filename']}** uploaded successfully!")

    # ← OUTSIDE the if block — shows on every rerun
    if st.session_state['df'] is not None:
        df = st.session_state['df']
        info = {
            'rows': df.shape[0],
            'columns': df.shape[1],
            'format': st.session_state['filename'].split('.')[-1].upper(),
            'filename': st.session_state['filename']
        }

        




def data_export(df, filename):
    st.session_state['current_section'] = 'export'
    st.subheader("💾 Export Dataset")

    loader = DataLoader()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Rows", df.shape[0])
    with col2:
        st.metric("Current Columns", df.shape[1])
    with col3:
        original_rows = st.session_state['original_df'].shape[0]
        st.metric("Rows Removed", original_rows - df.shape[0])

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="⬇️ Download as CSV",
            data=loader.export_csv(df),
            file_name=f"datasmith_cleaned_{filename.split('.')[0]}.csv",
            mime="text/csv",
            use_container_width=True
        )
    with col2:
        st.download_button(
            label="⬇️ Download as Excel",
            data=loader.export_excel(df),
            file_name=f"datasmith_cleaned_{filename.split('.')[0]}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    st.markdown("---")
    st.caption("💡 Use the **Reset** button in the sidebar to restore your original dataset anytime.")