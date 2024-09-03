from flask import Flask, request, jsonify
from flask_cors import CORS
from openai_tools import openai_api

app = Flask(__name__)
CORS(app)

conversation_history = []

def process_prompt(prompt, conversation_history):
    conversation_history.append({"role": "user", "content": prompt})

    response, updated_messages = openai_api.prompt(conversation_history)

    return response, updated_messages

@app.route('/process_prompt', methods=['POST'])
def process_prompt_endpoint():
    global conversation_history
    data = request.json
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({"error": "Prompt is required."}), 400

    try:
        response, conversation_history = process_prompt(prompt, conversation_history)
        return jsonify({"response": response, "conversation_history": conversation_history}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
