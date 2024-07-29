import os
import json
from openai import OpenAI
from util import milvus_functions
from util.neo4j_connection import Neo4jConnection 

def process_file(prompt, conversation_history):
    collection_name = "mint_collection"
    results = milvus_functions.query_collection(collection_name, prompt)
    context_json = json.dumps(results)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    client = OpenAI(api_key=api_key)

    # Prepare messages for the conversation history
    conversation_history.append({"role": "user", "content": prompt})
    conversation_history.append({"role": "system", "content": f"Context:{context_json}"})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history,
            max_tokens=2000
        )

        if response.choices:
            generated_answer = response.choices[0].message['content'].strip()
        else:
            generated_answer = "No response generated"
        
    except Exception as e:
        print(f"Failed to get response from OpenAI: {e}")
        generated_answer = "Failed to get response"

    # Update the conversation history with the new messages
    conversation_history.append({"role": "assistant", "content": generated_answer})

    # Connect to Neo4j and insert data
    neo4j_uri = os.environ.get("NEO4J_URI", "neo4j+s://248ce93c.databases.neo4j.io")
    neo4j_user = os.environ.get("NEO4J_USER", "jagadeesh230795@gmail.com")
    neo4j_password = os.environ.get("NEO4J_PASSWORD", "23racecar23")

    try:
        neo4j_conn = Neo4jConnection(neo4j_uri, neo4j_user, neo4j_password)
        neo4j_conn.insert_data([{"text": item["text"]} for item in results])  
        graph_data = neo4j_conn.generate_graph()
        neo4j_conn.close()
    except Exception as e:
        print(f"Failed to interact with Neo4j: {e}")
        graph_data = []

    return {"answer": generated_answer, "graph": graph_data}, conversation_history
