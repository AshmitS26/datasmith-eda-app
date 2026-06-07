import streamlit as st
from datetime import datetime


def log_transformation(action):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state['transformation_log'].append(f"[{timestamp}] {action}")

def init_session_state():
    defaults = {
        'df': None,
        'original_df': None,
        'filename': None,
        'transformation_log': [],
        'file_history': [],
        'current_section': 'upload',
        'theme': 'dark'
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value



def sidebar():
    with st.sidebar:
        st.title("⚒️ DataSmith")
        st.markdown("---")

        # ── Theme Toggle ──
        if st.session_state['theme'] == 'dark':
            if st.button("☀️ Switch to Light Mode", use_container_width=True):
                st.session_state['theme'] = 'light'
                st._config.set_option('theme.base', 'light')
                st._config.set_option('theme.backgroundColor', '#f5f7fa')
                st._config.set_option('theme.secondaryBackgroundColor', '#ffffff')
                st._config.set_option('theme.textColor', '#1a1a2e')
                st.rerun()
        else:
            if st.button("🌙 Switch to Dark Mode", use_container_width=True):
                st.session_state['theme'] = 'dark'
                st._config.set_option('theme.base', 'dark')
                st._config.set_option('theme.backgroundColor', '#0e1117')
                st._config.set_option('theme.secondaryBackgroundColor', '#1e2130')
                st._config.set_option('theme.textColor', '#fafafa')
                st.rerun()

        st.markdown("---")
        st.markdown("## 🗂️ Quick Navigation")
        st.caption("Click any section to jump directly to it")

        nav_bg = "#1e2130" if st.session_state['theme'] == 'dark' else "#e8eaf0"
        nav_color = "white" if st.session_state['theme'] == 'dark' else "#000000"

        st.markdown(f"""
        <a href="#upload-your-dataset" style="text-decoration:none">
            <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">📂 1. Upload Dataset</div>
        </a>
        <a href="#dataset-preview" style="text-decoration:none">
            <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">👁️ 2. Preview</div>
        </a>
        <a href="#dataset-statistics-and-analysis" style="text-decoration:none">
            <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">🔬 3. Statistics</div>
        </a>
        <a href="#data-quality-summary" style="text-decoration:none">
            <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">🛡️ 4. Quality Summary</div>
        </a>
        <a href="#column-wise-insights" style="text-decoration:none">
            <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">🧠 5. Column Insights</div>
        </a>
        <a href="#data-cleaning" style="text-decoration:none">
            <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">🧹 6. Data Cleaning</div>
        </a>
        <a href="#data-transformation" style="text-decoration:none">
            <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">⚙️ 7. Transformation</div>
        </a>
        <a href="#feature-scaling" style="text-decoration:none">
            <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">📏 8. Feature Scaling</div>
        </a>
        <a href="#outlier-detection-and-treatment" style="text-decoration:none">
            <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">🎯 9. Outlier Treatment</div>
        </a>
        <a href="#data-filtering-and-exploration" style="text-decoration:none">
            <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">🔍 10. Filter & Explore</div>
        </a>
        <a href="#correlation-analysis" style="text-decoration:none">
            <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">🔗 11. Correlation</div>
        </a>
        <a href="#visualization-dashboard" style="text-decoration:none">
            <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">📈 12. Visualizations</div>
        </a>
        <a href="#data-profiling-dashboard" style="text-decoration:none">
        <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">📋 13. Data Profiling</div>
        </a> 
        <a href="#export-dataset" style="text-decoration:none">
        <div style="padding:6px 10px;margin:3px 0;border-radius:6px;background:{nav_bg};color:{nav_color};">💾 14. Export Data</div>
        </a>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # ── Transformation Log ──
        st.markdown("## 📝 Transformation Log")
        st.caption("Last 5 operations applied")

        if len(st.session_state['transformation_log']) > 0:
            for entry in st.session_state['transformation_log'][-5:][::-1]:
                st.caption(f"• {entry}")
            if len(st.session_state['transformation_log']) > 5:
                st.caption(f"... and {len(st.session_state['transformation_log']) - 5} more")
            log_text = "\n".join(st.session_state['transformation_log'])
            st.download_button(
                label="⬇️ Download Full Log",
                data=log_text,
                file_name="datasmith_transformation_log.txt",
                mime="text/plain",
                use_container_width=True,
                key="sidebar_log_download"
            )
        else:
            st.caption("No transformations yet")

        st.markdown("---")

        if st.button("🔄 Reset to Original Data", use_container_width=True):
            if st.session_state['original_df'] is not None:
                st.session_state['df'] = st.session_state['original_df'].copy()
                log_transformation("Reset to original data")
                st.success("✅ Reset done")
                st.rerun()

        if len(st.session_state['file_history']) > 0:
            st.markdown("---")
            st.markdown("## 🕘 Recent Files")
            for f in st.session_state['file_history'][-5:][::-1]:
                st.caption(f"📄 {f}")