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
    neo4j_uri = os.environ.get("NEO4J_URI", "neo4j+s://fba6723a.databases.neo4j.io")
    neo4j_user = os.environ.get("NEO4J_USER", "neo4j")
    neo4j_password = os.environ.get("NEO4J_PASSWORD", "b2DtRq6T2oH_6Qovk-cQ-vi3blx1Bmr8CG_OxbL34to")
    try:
        conn = Neo4jConnection(neo4j_uri, neo4j_user, neo4j_password)
        conn.close()  # Try to connect and close immediately for basic connectivity check
        return conn
    except Exception as e:
        print(f"Failed to connect to Neo4j: {e}")
        return None  # Return None on connection failure

def process_file(prompt, conversation_history):
    collection_name = "mint_collection"
    results = milvus_functions.query_collection(collection_name, prompt)
    context_json = json.dumps(results)

    client = get_openai_client()

    conversation_history.append({"role": "user", "content": prompt})
    conversation_history.append({"role": "system", "content": f"Context:{context_json}"})

    neo4j_conn = get_neo4j_connection()
    if not neo4j_conn:
        print("Neo4j connection failed. Skipping Neo4j processing.")
        return {"answer": "Failed to connect to Neo4j", "graph": []}, conversation_history

    try:
        # Send Vector DB results to Neo4j for analysis (if connection successful)
        neo4j_conn.process_vector_db_results(results)  # Update Neo4j_connection.py

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history,
            max_tokens=4000
        )
        generated_answer = response.choices[0].message.content.strip() if response.choices else "No response generated"
    except Exception as e:
        print(f"Failed to interact with Neo4j or OpenAI: {e}")
        generated_answer = "Failed to process request"

    conversation_history.append({"role": "assistant", "content": generated_answer})

    # Generate graph data from Neo4j for every prompt (if connection successful)
    try:
        graph_data = neo4j_conn.generate_graph(prompt)  # Update Neo4j_connection.py (consider prompt filtering)
    except Exception as e:
        print(f"Failed to generate graph from Neo4j: {e}")
        graph_data = []

    neo4j_conn.close()
    return {"answer": generated_answer, "graph": graph_data}, conversation_history

# Update Neo4j_connection.py to include these functions:

def process_vector_db_results(self, results):
    # Convert Vector DB results into Neo4j nodes and relationships (implement logic)
    pass

def generate_graph(self, prompt):
    # Adapt Cypher query based on prompt and potentially filter results (implement logic)
    # Return processed graph data structure
    pass
