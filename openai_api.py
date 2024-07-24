import os
import json
from openai import OpenAI
from util import milvus_functions

# Function to handle file processing and AI response
#/Users/jags/Desktop/Mints_Data/mints-main
def process_file(prompt):
    file_path = '/Users/jags/Desktop/Mints_Data/mints-main' 
    collection_name = "paragraph_collection"

    milvus_functions.delete_collection(collection_name)
    milvus_functions.generate_and_save_data(file_path, collection_name)

    results = milvus_functions.query_collection(collection_name, prompt)
    context_json = json.dumps(results)

    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Answer the following question based on the provided context:{context_json}\n\nQuestion: {prompt}"}
        ],
        max_tokens=200
    )

    if response.choices:
        generated_answer = response.choices[0].message.content.strip()
    else:
        generated_answer = "No response generated"

    return generated_answer