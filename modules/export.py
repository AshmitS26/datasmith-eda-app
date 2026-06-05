import streamlit as st
import pandas as pd
import io


def show_export(df, filename):
    st.subheader("💾 Export Dataset")

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
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download as CSV",
            data=csv_data,
            file_name=f"datalens_cleaned_{filename.split('.')[0]}.csv",
            mime="text/csv",
            use_container_width=True
        )
    with col2:
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Cleaned Data')
        excel_data = excel_buffer.getvalue()
        st.download_button(
            label="⬇️ Download as Excel",
            data=excel_data,
            file_name=f"datalens_cleaned_{filename.split('.')[0]}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    st.markdown("---")
    st.caption("💡 Use the **Reset** button in the sidebar to restore your original dataset anytime.")