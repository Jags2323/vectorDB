import os
import json
from openai import OpenAI
from util import milvus_functions
from util.neo4j_connection import Neo4jConnection

def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return OpenAI(api_key=api_key)

def get_neo4j_connection():
    neo4j_uri = os.environ.get("NEO4J_URI", "neo4j+s://248ce93c.databases.neo4j.io")
    neo4j_user = os.environ.get("NEO4J_USER", "neo4j")
    neo4j_password = os.environ.get("NEO4J_PASSWORD", "b2DtRq6T2oH_6Qovk-cQ-vi3blx1Bmr8CG_OxbL34to")
    return Neo4jConnection(neo4j_uri, neo4j_user, neo4j_password)

def process_file(prompt, conversation_history):
    collection_name = "mint_collection"
    results = milvus_functions.query_collection(collection_name, prompt)
    context_json = json.dumps(results)

    client = get_openai_client()

    conversation_history.append({"role": "user", "content": prompt})
    conversation_history.append({"role": "system", "content": f"Context:{context_json}"})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history,
            max_tokens=2000
        )
        generated_answer = response.choices[0].message.content.strip() if response.choices else "No response generated"
    except Exception as e:
        print(f"Failed to get response from OpenAI: {e}")
        generated_answer = "Failed to get response"

    conversation_history.append({"role": "assistant", "content": generated_answer})

    try:
        neo4j_conn = get_neo4j_connection()
        neo4j_conn.insert_data([{"text": item["text"]} for item in results])
        graph_data = neo4j_conn.generate_graph()
        neo4j_conn.close()
    except Exception as e:
        print(f"Failed to interact with Neo4j: {e}")
        graph_data = []

    return {"answer": generated_answer, "graph": graph_data}, conversation_history
