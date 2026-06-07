import streamlit as st
from logic.data_profiling import DataProfiler


def data_profiling(df):
    st.subheader("📋 Data Profiling Dashboard")
    st.markdown("Generates a comprehensive automated EDA report for your dataset.")
    st.warning("⚠️ This may take 15–30 seconds depending on dataset size.")

    if st.button("🚀 Generate Profiling Report", type="primary", key="profile_btn"):
        try:
            profiler = DataProfiler()
            with st.spinner("Generating report... please wait"):
                profile_html = profiler.generate_report(df)
            st.success("✅ Report generated successfully!")
            st.download_button(
                label="⬇️ Download Full HTML Report",
                data=profile_html,
                file_name="datasmith_profile_report.html",
                mime="text/html",
                use_container_width=True
            )
            st.components.v1.html(profile_html, height=800, scrolling=True)
        except ImportError:
            st.warning("⚠️ Profiling available on local installation only.")
            st.info("To use locally: pip install ydata-profiling")
        except Exception as e:
            st.error(f"❌ Profiling failed: {e}")