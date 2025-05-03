from flask import Flask, request, jsonify, render_template
from scraper import scrape_website
from faq_generator import generate_faqs
import os
from difflib import get_close_matches

# Debug paths
print("=" * 50)
print("Current working directory:", os.getcwd())
print("Templates exists?:", os.path.exists('templates'))
print("Index.html exists?:", os.path.exists('templates/index.html'))
print("Files in directory:", os.listdir())
print("=" * 50)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False  # Maintain JSON key order
faqs = []


# Improved initialization endpoint
@app.route('/init', methods=['POST'])
def init_bot():
    global faqs
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 415

        data = request.get_json()
        url = data.get("url")

        if not url:
            return jsonify({"error": "URL parameter is required"}), 400

        scraped_data = scrape_website(url)

        if not scraped_data.get("text"):
            error_msg = scraped_data.get("error", "No text content found")
            return jsonify({
                "error": "Scraping failed",
                "details": error_msg,
                "received_data": scraped_data
            }), 500

        faqs = generate_faqs(scraped_data["text"])
        return jsonify({
            "status": "Ready!",
            "faqs": faqs,
            "stats": {
                "pages_scraped": 1,
                "faqs_generated": len(faqs)
            }
        })

    except Exception as e:
        return jsonify({
            "error": "Initialization failed",
            "details": str(e)
        }), 500


# Enhanced Q&A endpoint
@app.route('/ask', methods=['POST'])
def ask():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 415

        data = request.get_json()
        question = data.get("question", "").strip().lower()

        if not question:
            return jsonify({"error": "Question cannot be empty"}), 400

        # Exact match first
        exact_match = next(
            (faq for faq in faqs if question in faq["question"].lower()),
            None
        )

        # Fuzzy matching if no exact match
        if not exact_match:
            questions = [faq["question"].lower() for faq in faqs]
            matches = get_close_matches(question, questions, n=1, cutoff=0.6)
            if matches:
                exact_match = next(
                    faq for faq in faqs
                    if faq["question"].lower() == matches[0]
                )

        if exact_match:
            return jsonify({
                "answer": exact_match["answer"],
                "matched_question": exact_match["question"],
                "confidence": "exact" if question == exact_match["question"].lower() else "fuzzy"
            })

        return jsonify({
            "answer": "I couldn't find an answer. Try rephrasing your question.",
            "suggestions": [faq["question"] for faq in faqs[:3]]
        })

    except Exception as e:
        return jsonify({
            "error": "Answer generation failed",
            "details": str(e)
        }), 500


# Frontend route
@app.route('/')
def home():
    return render_template('index.html')


# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": ["/init (POST)", "/ask (POST)", "/"]
    }), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({
        "error": "Internal server error",
        "tip": "Check server logs for details"
    }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
