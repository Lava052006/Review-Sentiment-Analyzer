import streamlit as st
import pandas as pd
import re
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Product Sentiment Analyzer", page_icon="📊", layout="wide")

@st.cache_resource
def get_analyzer():
    from ML import SentimentAnalyzer
    return SentimentAnalyzer()

def get_scraper_func():
    from scraper import scrape_reviews
    return scrape_reviews

# Styling for stability
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .sentiment-card {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        border: 1px solid #ddd;
        min-height: 150px; /* Lock height to prevent shaking */
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Product Sentiment Analyzer")
st.markdown("Automated insights from e-commerce reviews using **AI Transformers**.")

# Sidebar
st.sidebar.header("Configuration")
target_count = st.sidebar.slider("Target Number of Reviews", 10, 500, 50, step=10)

# URL Input
url = st.text_input("Enter Flipkart Product URL", placeholder="https://www.flipkart.com/...")

# ✅ FIX 1: Single persistent message slot — only used once per render
status_area = st.empty()

# Initialize session state for data persistence
if 'scraped_df' not in st.session_state:
    st.session_state.scraped_df = None

if 'status_msg' not in st.session_state:
    st.session_state.status_msg = ("info", "Paste a Flipkart product URL above to get started.")

if st.button("Analyze Sentiment"):
    if not url:
        st.session_state.status_msg = ("warning", "Please enter a URL.")
    else:
        scrape_reviews_func = get_scraper_func()
        # Use a localized spinner that doesn't conflict with status_area
        with st.spinner("Scraping reviews..."):
            df = scrape_reviews_func(url, target_count=target_count)
        
        if df.empty:
            st.session_state.status_msg = ("error", "No reviews found. Check URL.")
        else:
            with st.spinner("AI Sentiment Analysis..."):
                analyzer = get_analyzer()
                df = analyzer.analyze(df)
                st.session_state.scraped_df = df
            st.session_state.status_msg = ("success", "Analysis complete!")

# ✅ FIX 1 continued: Render status from session state — stable, no conflict
msg_type, msg_text = st.session_state.status_msg
if msg_type == "info":
    status_area.info(msg_text)
elif msg_type == "warning":
    status_area.warning(msg_text)
elif msg_type == "error":
    status_area.error(msg_text)
elif msg_type == "success":
    status_area.success(msg_text)

# Display dashboard if data exists
if st.session_state.scraped_df is not None:
    df = st.session_state.scraped_df
    
    # ✅ FIX 2: Reuse cached analyzer
    analyzer = get_analyzer()
    summary = analyzer.get_summary(df)
    
    # --- DASHBOARD LAYOUT (Locked Container) ---
    dashboard_container = st.container()
    with dashboard_container:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="sentiment-card"><h3>Positive</h3><h2 style="color:green">{summary.get("Positive", 0)}%</h2></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="sentiment-card"><h3>Neutral</h3><h2 style="color:orange">{summary.get("Neutral", 0)}%</h2></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="sentiment-card"><h3>Negative</h3><h2 style="color:red">{summary.get("Negative", 0)}%</h2></div>', unsafe_allow_html=True)
            
        st.divider()
        
        # --- CENTERED CHART ---
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.subheader("Sentiment Distribution")
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.countplot(data=df, x='sentiment_label', palette={'Positive': 'green', 'Neutral': 'orange', 'Negative': 'red'}, ax=ax)
            ax.set_title("Count of Reviews by Sentiment")
            plt.tight_layout() # Prevent label clipping
            st.pyplot(fig, use_container_width=True)
            plt.close(fig) # ✅ FIX 3: Prevent figure accumulation
else:
    pass # Managed by session_state status_area above
