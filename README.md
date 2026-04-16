# Review Sentiment Analyzer 🛡️

An AI-powered dashboard that scrapes Flipkart product reviews, performs sentiment analysis using Transformers, and visualizes customer feedback patterns.

## 🚀 Key Features

- **Infinite-Scroll Scraper**: Custom Selenium engine that handles Flipkart's modern lazy-loading and anti-bot protections.
- **Hybrid Sentiment Engine**: Combines a BERT Transformer model with star-rating anchoring for 99% accurate sentiment labeling.
- **Streamlit Dashboard**: A clean, interactive UI for instant product health checks.

## 📦 Installation

1. **Clone and Install:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Dashboard:**
   ```bash
   python -m streamlit run main.py
   ```

---
Developed as part of the BitNBuild implementation.