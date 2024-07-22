from flask import Flask, request, jsonify
from flask_cors import CORS
import openai_api

app = Flask(__name__)
CORS(app)

# Flask endpoint to process files
@app.route('/process_prompt', methods=['POST'])
def process_prompt_endpoint():
    data = request.json
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({"error": "Prompt is required."}), 400

    try:
        result = openai_api.process_file(prompt)
        return jsonify({"response": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)