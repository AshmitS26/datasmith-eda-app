import streamlit as st


def inject_css():
    st.markdown("""
    <style>
    /* ═══════════════════════════════════════════
       GOOGLE FONTS
    ═══════════════════════════════════════════ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    /* ═══════════════════════════════════════════
       ROOT VARIABLES
    ═══════════════════════════════════════════ */
    :root {
        --primary:       #6C63FF;
        --primary-light: #8B85FF;
        --primary-dark:  #4B44CC;
        --accent:        #00D4AA;
        --accent2:       #FF6B6B;
        --card-bg:       rgba(255,255,255,0.04);
        --card-border:   rgba(108,99,255,0.25);
        --card-hover:    rgba(108,99,255,0.12);
        --radius:        14px;
        --radius-sm:     8px;
        --shadow:        0 4px 24px rgba(0,0,0,0.35);
        --font-main:     'Inter', sans-serif;
        --font-heading:  'Space Grotesk', sans-serif;
    }

    /* ═══════════════════════════════════════════
       GLOBAL TYPOGRAPHY
    ═══════════════════════════════════════════ */
    html, body, [class*="css"] {
        font-family: var(--font-main) !important;
    }

    /* ═══════════════════════════════════════════
       MAIN TITLE
    ═══════════════════════════════════════════ */
    .main-title {
        font-family: var(--font-heading);
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
    }

    .main-subtitle {
        font-size: 1.05rem;
        opacity: 0.65;
        margin-top: 0;
        margin-bottom: 1.2rem;
        font-weight: 400;
    }

    /* ═══════════════════════════════════════════
       SECTION HEADERS (replaces st.subheader)
    ═══════════════════════════════════════════ */
    h2, h3 {
        font-family: var(--font-heading) !important;
        letter-spacing: -0.3px;
    }

    /* Section anchor header pill */
    .section-header {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 18px;
        background: linear-gradient(135deg, rgba(108,99,255,0.15), rgba(0,212,170,0.08));
        border-left: 3px solid var(--primary);
        border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
        margin-bottom: 1rem;
        font-family: var(--font-heading);
        font-size: 1.15rem;
        font-weight: 600;
    }

    /* ═══════════════════════════════════════════
       METRIC CARDS
    ═══════════════════════════════════════════ */
    [data-testid="metric-container"] {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: var(--radius);
        padding: 16px 20px !important;
        transition: box-shadow 0.2s, border-color 0.2s;
    }
    [data-testid="metric-container"]:hover {
        border-color: var(--primary-light);
        box-shadow: 0 0 0 1px rgba(108,99,255,0.3), var(--shadow);
    }
    [data-testid="metric-container"] [data-testid="stMetricLabel"] {
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        opacity: 0.6;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-family: var(--font-heading) !important;
        font-size: 1.9rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, var(--primary-light), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* ═══════════════════════════════════════════
       CARDS (st.container with border)
    ═══════════════════════════════════════════ */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        border-radius: var(--radius) !important;
        border-color: var(--card-border) !important;
        background: var(--card-bg) !important;
        transition: box-shadow 0.2s;
    }
    [data-testid="stVerticalBlockBorderWrapper"] > div:hover {
        box-shadow: 0 0 0 1px rgba(108,99,255,0.2);
    }

    /* ═══════════════════════════════════════════
       BUTTONS
    ═══════════════════════════════════════════ */
    /* Primary action buttons */
    [data-testid="stDownloadButton"] button,
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
        color: #fff !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em;
        transition: opacity 0.2s, transform 0.15s, box-shadow 0.2s !important;
        box-shadow: 0 2px 12px rgba(108,99,255,0.35) !important;
    }
    [data-testid="stDownloadButton"] button:hover,
    .stButton > button[kind="primary"]:hover {
        opacity: 0.9 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(108,99,255,0.45) !important;
    }

    /* Secondary / default buttons */
    .stButton > button {
        border-radius: var(--radius-sm) !important;
        font-weight: 500 !important;
        border: 1px solid var(--card-border) !important;
        transition: border-color 0.2s, background 0.2s !important;
    }
    .stButton > button:hover {
        border-color: var(--primary-light) !important;
        background: var(--card-hover) !important;
    }

    /* ═══════════════════════════════════════════
       SELECTBOX, MULTISELECT, TEXT INPUT
    ═══════════════════════════════════════════ */
    [data-testid="stSelectbox"] > div > div,
    [data-testid="stMultiSelect"] > div > div,
    [data-testid="stTextInput"] > div > div {
        border-radius: var(--radius-sm) !important;
        border-color: var(--card-border) !important;
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    [data-testid="stSelectbox"] > div > div:focus-within,
    [data-testid="stMultiSelect"] > div > div:focus-within,
    [data-testid="stTextInput"] > div > div:focus-within {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(108,99,255,0.2) !important;
    }

    /* Multiselect tag pills */
    [data-testid="stMultiSelect"] span[data-baseweb="tag"] {
        background: rgba(108,99,255,0.2) !important;
        border-radius: 6px !important;
        border: 1px solid rgba(108,99,255,0.4) !important;
    }

    /* ═══════════════════════════════════════════
       FILE UPLOADER
    ═══════════════════════════════════════════ */
    [data-testid="stFileUploader"] > div {
        border: 2px dashed var(--primary) !important;
        border-radius: var(--radius) !important;
        background: rgba(108,99,255,0.04) !important;
        transition: background 0.2s, border-color 0.2s;
    }
    [data-testid="stFileUploader"] > div:hover {
        background: rgba(108,99,255,0.08) !important;
        border-color: var(--accent) !important;
    }

    /* ═══════════════════════════════════════════
       TABS
    ═══════════════════════════════════════════ */
    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(255,255,255,0.03) !important;
        padding: 4px;
        border-radius: var(--radius-sm);
    }
    [data-testid="stTabs"] [data-baseweb="tab"] {
        border-radius: var(--radius-sm) !important;
        font-weight: 500 !important;
        transition: background 0.2s !important;
    }
    [data-testid="stTabs"] [aria-selected="true"] {
        background: var(--primary) !important;
        color: #fff !important;
        font-weight: 600 !important;
    }

    /* ═══════════════════════════════════════════
       EXPANDER
    ═══════════════════════════════════════════ */
    [data-testid="stExpander"] {
        border: 1px solid var(--card-border) !important;
        border-radius: var(--radius) !important;
        background: var(--card-bg) !important;
    }
    [data-testid="stExpander"] summary {
        font-weight: 600 !important;
        font-family: var(--font-heading) !important;
    }

    /* ═══════════════════════════════════════════
       DATAFRAME / TABLE
    ═══════════════════════════════════════════ */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--card-border) !important;
        border-radius: var(--radius) !important;
        overflow: hidden;
    }

    /* ═══════════════════════════════════════════
       ALERTS / INFO / SUCCESS / WARNING
    ═══════════════════════════════════════════ */
    [data-testid="stAlert"] {
        border-radius: var(--radius-sm) !important;
        border-width: 1px !important;
    }

    /* ═══════════════════════════════════════════
       SIDEBAR
    ═══════════════════════════════════════════ */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0e1a 0%, #131228 50%, #0e1117 100%) !important;
        border-right: 1px solid rgba(108,99,255,0.2) !important;
    }
    [data-testid="stSidebar"] .stTitle,
    [data-testid="stSidebar"] h1 {
        font-family: var(--font-heading) !important;
        background: linear-gradient(135deg, var(--primary-light), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.4rem !important;
    }

    /* Sidebar nav links hover glow */
    [data-testid="stSidebar"] a > div {
        transition: background 0.2s, box-shadow 0.2s !important;
    }
    [data-testid="stSidebar"] a > div:hover {
        background: rgba(108,99,255,0.25) !important;
        box-shadow: inset 2px 0 0 var(--primary) !important;
    }

    /* Sidebar buttons */
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(108,99,255,0.12) !important;
        border: 1px solid rgba(108,99,255,0.3) !important;
        color: #fff !important;
        font-weight: 500 !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(108,99,255,0.25) !important;
        border-color: var(--primary-light) !important;
    }

    /* ═══════════════════════════════════════════
       DIVIDER
    ═══════════════════════════════════════════ */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(108,99,255,0.4), transparent) !important;
        margin: 1.5rem 0 !important;
    }

    /* ═══════════════════════════════════════════
       SLIDER
    ═══════════════════════════════════════════ */
    [data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stSliderThumb"] {
        background: var(--primary) !important;
        border-color: var(--primary-light) !important;
    }

    /* ═══════════════════════════════════════════
       CHECKBOX & RADIO
    ═══════════════════════════════════════════ */
    [data-testid="stCheckbox"] input:checked + div,
    [data-testid="stRadio"] input:checked + div {
        background: var(--primary) !important;
        border-color: var(--primary) !important;
    }

    /* ═══════════════════════════════════════════
       PROGRESS BAR
    ═══════════════════════════════════════════ */
    [data-testid="stProgress"] > div > div {
        background: linear-gradient(90deg, var(--primary), var(--accent)) !important;
        border-radius: 99px !important;
    }

    /* ═══════════════════════════════════════════
       FOOTER BADGE
    ═══════════════════════════════════════════ */
    .ds-badge {
        display: inline-block;
        padding: 3px 10px;
        background: rgba(108,99,255,0.15);
        border: 1px solid rgba(108,99,255,0.35);
        border-radius: 99px;
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--primary-light);
        letter-spacing: 0.04em;
    }

    /* ═══════════════════════════════════════════
       ABOUT CARD
    ═══════════════════════════════════════════ */
    .about-card {
        padding: 24px;
        border-radius: var(--radius);
        border: 1px solid var(--card-border);
        background: linear-gradient(135deg, rgba(108,99,255,0.08), rgba(0,212,170,0.05));
        text-align: center;
        transition: box-shadow 0.25s;
    }
    .about-card:hover {
        box-shadow: 0 0 0 1px var(--primary), var(--shadow);
    }

    /* ═══════════════════════════════════════════
       HIDE STREAMLIT DEFAULT CHROME
    ═══════════════════════════════════════════ */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)