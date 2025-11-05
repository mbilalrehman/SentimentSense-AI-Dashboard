# SentimentSense-AI-Dashboard
A full-stack web application for performing real-time sentiment analysis and keyword extraction on user-uploaded CSV files.

This project transforms raw customer feedback (from reviews, surveys, etc.) into actionable business insights using a Flask backend, Pandas for data processing, VADER for sentiment analysis, and Chart.js for beautiful, interactive frontend data visualization.

(Tip: Yahan aap apne working dashboard ki screenshot (jaisay aapne mujhay bheji thi) upload kar k uss ka link daal saktay hain)

Features

Hero Landing Page: A modern, eye-catching landing page to introduce the product.

CSV Upload: Easily upload any CSV file.

Column Selection: Dynamically specify which column contains the text for analysis.

AI-Powered Analysis:

Sentiment Breakdown: Uses VADER to generate Positive, Neutral, and Negative scores.

Top Keywords: Extracts the Top 10 most common and meaningful keywords (excluding stopwords).

Interactive Dashboard:

Pie Chart: Visualizes the sentiment breakdown.

Bar Chart: Shows the most frequent keywords.

Summary Stats: Displays total rows processed, analyzed, and skipped.

Tech Stack

Backend: Python, Flask

Data Processing: Pandas

AI / NLP: VADER (SentimentIntensityAnalyzer), re (Regex), collections.Counter

Frontend: HTML, Tailwind CSS, JavaScript

Data Visualization: Chart.js

How to Run Locally

Clone the repository: git clone [your-repo-link]

Navigate to the project directory: cd SentimentDashboard

Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate


Install the required libraries:

pip install -r requirements.txt


Run the Flask application:

flask run --host=0.0.0.0 --port=5000


Open your browser and go to: http://localhost:5000
