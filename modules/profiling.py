import streamlit as st


def show_profiling(df):
    st.subheader("📋 Data Profiling Dashboard")
    st.markdown("Generates a comprehensive automated EDA report for your dataset.")
    st.warning("⚠️ This may take 15–30 seconds depending on dataset size.")

    if st.button("🚀 Generate Profiling Report", type="primary", key="profile_btn"):
        try:
            from ydata_profiling import ProfileReport
            with st.spinner("Generating report... please wait"):
                profile = ProfileReport(df, title="DataLens Profiling Report", explorative=True)
                profile_html = profile.to_html()
            st.success("✅ Report generated successfully!")
            st.download_button(
                label="⬇️ Download Full HTML Report",
                data=profile_html,
                file_name="datalens_profile_report.html",
                mime="text/html",
                use_container_width=True
            )
            st.components.v1.html(profile_html, height=800, scrolling=True)
        except Exception as e:
            st.error(f"❌ Profiling failed: {e}")