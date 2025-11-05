import os
import pandas as pd
from flask import Flask, request, render_template, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import Counter
import re
import io

app = Flask(__name__)

# VADER ko ek baar load karein
analyzer = SentimentIntensityAnalyzer()

# Common English stopwords (boring words) ki list
# (SpaCy/NLTK install kiye bina, taakay project halka rahay)
STOPWORDS = set([
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 
    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 
    'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 
    'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 
    'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 
    'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 
    'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 
    'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 
    'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 
    'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 've', 'll', 'm', 're'
])

@app.route('/')
def index():
    """Hamara HTML page serve karta hai."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    CSV file aur column name ko le kar AI analysis karta hai.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    column_name = request.form.get('columnName')

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not column_name:
        return jsonify({'error': 'No column name specified'}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Please upload a CSV file'}), 400

    try:
        # File ko seekable stream mein convert karein (Pandas k liye zaroori)
        file_stream = io.StringIO(file.stream.read().decode("utf-8"))
        
        # Pandas se CSV read karein
        df = pd.read_csv(file_stream)

        if column_name not in df.columns:
            return jsonify({'error': f"Column '{column_name}' not found in the CSV."}), 400
        
        # Text column ko string mein convert karein (NaN/numbers k maslay k liye)
        texts = df[column_name].dropna().astype(str)

        # --- AI Analysis 1: Sentiment (VADER) ---
        sentiment_scores = texts.apply(lambda text: analyzer.polarity_scores(text)['compound'])
        
        sentiment_counts = {
            'positive': int((sentiment_scores > 0.05).sum()),
            'neutral': int(((sentiment_scores >= -0.05) & (sentiment_scores <= 0.05)).sum()),
            'negative': int((sentiment_scores < -0.05).sum())
        }
        
        # --- AI Analysis 2: Top Keywords (Counter) ---
        all_text = ' '.join(texts).lower()
        all_text = re.sub(r'[^\w\s]', '', all_text) # Punctuation hata dein
        words = all_text.split()
        
        # Stopwords (boring words) hata dein
        filtered_words = [word for word in words if word not in STOPWORDS and len(word) > 2]
        
        # Top 10 sab se common keywords
        word_counts = Counter(filtered_words).most_common(10)
        top_keywords = dict(word_counts)

        # Final JSON response
        return jsonify({
            'total_rows': len(df),
            'rows_analyzed': len(texts),
            'sentiment_counts': sentiment_counts,
            'top_keywords': top_keywords
        })

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)