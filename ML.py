from transformers import pipeline
import pandas as pd
import re

class SentimentAnalyzer:
    def __init__(self, model_name="nlptown/bert-base-multilingual-uncased-sentiment"):
        """
        Initializes the sentiment analysis pipeline using a pre-trained Hugging Face model.
        """
        print(f"Loading model: {model_name}...")
        # Force PyTorch (framework='pt') to avoid Keras 3 compatibility issues
        self.analyzer = pipeline("sentiment-analysis", model=model_name, framework="pt")
        print("Model loaded successfully.")

    def analyze(self, reviews_df):
        """
        Takes a DataFrame with a 'review' column and adds sentiment scores and labels.
        """
        if reviews_df.empty or 'review' not in reviews_df.columns:
            return reviews_df

        texts = reviews_df['review'].tolist()
        # Truncate texts to 512 tokens to avoid model errors
        truncated_texts = [str(text)[:512] for text in texts]
        
        results = self.analyzer(truncated_texts)
        
        scores = []
        labels = []
        
        for res in results:
            star_count = int(res['label'].split(' ')[0])
            scores.append(star_count)
            
            if star_count <= 2:
                labels.append("Negative")
            elif star_count == 3:
                labels.append("Neutral")
            else:
                labels.append("Positive")
                
        # --- STAR RATING ANCHORING ---
        # Strictly override the AI label based on actual user star rating
        final_labels = []
        for i, row in reviews_df.iterrows():
            pred_label = labels[i]
            # Extract actual rating digit from scraped text
            rating_str = str(row.get('rating', '3'))
            match = re.search(r'\d', rating_str)
            actual_stars = int(match.group()) if match else 3
            
            if actual_stars <= 2:
                final_labels.append("Negative")
            elif actual_stars >= 4:
                final_labels.append("Positive")
            else:
                final_labels.append(pred_label)
        
        reviews_df['sentiment_score'] = scores
        reviews_df['sentiment_label'] = final_labels
        
        return reviews_df

    def get_summary(self, reviews_df):
        """
        Returns a summary dictionary of the sentiment distribution.
        """
        if reviews_df.empty:
            return {}
            
        summary = reviews_df['sentiment_label'].value_counts(normalize=True).to_dict()
        summary = {k: round(v * 100, 2) for k, v in summary.items()}
        return summary
