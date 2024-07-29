from flask import Flask, request, jsonify
from flask_cors import CORS
import openai_api

app = Flask(__name__)
CORS(app)

# In-memory store for conversation history
conversation_history = [{"role": "system", "content": "You are a helpful assistant. Answer questions of the user based on context provided."}]

# Flask endpoint to process prompts
@app.route('/process_prompt', methods=['POST'])
def process_prompt_endpoint():
    global conversation_history  
    data = request.json
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({"error": "Prompt is required."}), 400

    try:
        result, conversation_history = openai_api.process_file(prompt, conversation_history)
        return jsonify({"response": result["answer"], "context": f"{conversation_history}", "graph": result["graph"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
