from flask import Flask, request, jsonify
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import re, string

app = Flask(__name__)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load models on startup
print("Loading models...")
tokenizer = AutoTokenizer.from_pretrained("./sentiment_model")
model = AutoModelForSequenceClassification.from_pretrained("./sentiment_model")
model.to(device)
model.eval()
pretrained_neg = pipeline("sentiment-analysis")
le_classes = ['Neutral', 'Null', 'Positive']
print("Models loaded!")

def clean_text(text):
    text = str(text)
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"@\w+|#\w+", "", text)
    text = re.sub(r"[•●▪️♦▶►→\-–—*▪•]", " ", text)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    text = text.translate(str.maketrans("", "", string.punctuation.replace(".", "").replace(",", "").replace("!", "").replace("?", "")))
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()

def get_sentiment(text):
    cleaned = clean_text(text)

    # Step 1: Pretrained Negative check
    result = pretrained_neg(cleaned)[0]
    if (result["label"].upper() == "NEGATIVE"
        and result["score"] > 0.70
        and len(cleaned.split()) > 2):
        return "Negative"

    # Step 2: Fine-tuned model for Positive, Neutral, Null
    inputs = tokenizer(cleaned, return_tensors="pt", truncation=True, padding=True, max_length=128).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
        pred_id = torch.argmax(outputs.logits, dim=1).item()

    # Map to API response format
    sentiment = le_classes[pred_id]
    if sentiment == "Positive":
        return "Positive"
    elif sentiment == "Neutral":
        return "Neutral"
    else:  # Null
        return "Null"

@app.route('/getsentiment', methods=['POST'])
def api_sentiment():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No JSON data received'}), 400

    # Batch mode 
    results = {}
    for key, comment in data.items():
        results[key] = get_sentiment(comment)

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
