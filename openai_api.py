import os
import json
from openai import OpenAI
from util import milvus_functions
    
#/Users/jags/Desktop/Mints_Data/mints-main
def process_file(prompt, conversation_history):
    collection_name = "mints"

    file_path = 'MINTS/'
    milvus_functions.delete_collection(collection_name)
    milvus_functions.generate_and_save_data(file_path, collection_name)

    results = milvus_functions.query_collection(collection_name, prompt)
    context_json = json.dumps(results)

    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    # Prepare messages for the conversation history
    conversation_history.append({"role": "user", "content": f"{prompt}"})
    conversation_history.append({"role": "system", "content": f"Context:{context_json}"})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history,
        max_tokens=2000
    )

    if response.choices:
        generated_answer = response.choices[0].message.content.strip()
    else:
        generated_answer = "No response generated"

    # Update the conversation history with the new messages
    conversation_history.append({"role": "assistant", "content": f"{generated_answer}"})

    return generated_answer, conversation_history