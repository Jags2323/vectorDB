from flask import Flask, request, jsonify
from flask_cors import CORS
from openai_util import openai_api
from milvus_util import milvus_functions
import json

app = Flask(__name__)
CORS(app)

conversation_history = []
collection_name = "MINTS"
file_path = 'data/MINTS/'

# Initialize the Milvus DB once when the app starts
def initialize_milvus():
    try:
        milvus_functions.delete_collection(collection_name)
        milvus_functions.generate_and_save_data(file_path, collection_name)
        print("Milvus DB initialized successfully with collection:", collection_name)
    except Exception as e:
        print(f"Error initializing Milvus DB: {str(e)}")
        raise

initialize_milvus()  # Initialize Milvus when the app starts

def process_prompt(prompt, conversation_history):
    # Query Milvus for relevant context using the user's prompt
    milvus_results = milvus_functions.query_collection(collection_name, prompt)
    context = json.dumps(milvus_results)  # Convert results to a string format if necessary

    # Append user's prompt and the retrieved context to the conversation history
    conversation_history.append({"role": "user", "content": prompt})
    conversation_history.append({"role": "system", "content": context})

    # Call OpenAI API with the combined prompt
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

