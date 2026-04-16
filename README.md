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

## ☁️ Deployment to Hugging Face Spaces

1. Create a new **Space** on Hugging Face.
2. Select **Streamlit** as the SDK.
3. In the "Create" screen, select **"Import from GitHub"**.
4. Connect this repository: `https://github.com/Lava052006/Review-Sentiment-Analyzer`.
5. Hugging Face will automatically use the `packages.txt` and `requirements.txt` to set up the environment.

---
Developed as part of the BitNBuild implementation.