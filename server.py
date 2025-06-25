from flask import Flask, request, jsonify
from flask_cors import CORS
from llm import load_model_and_tokenizer, generate_text

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load model and tokenizer
model, tokenizer = load_model_and_tokenizer()

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        generated_text = generate_text(
            prompt=prompt,
            model=model,
            tokenizer=tokenizer,
            max_length=50,
            temperature=0.7,
            num_return_sequences=1
        )
        return jsonify({"generated_text": generated_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)