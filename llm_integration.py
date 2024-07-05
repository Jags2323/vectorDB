import argparse
import json
import fitz  # PyMuPDF
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
from sentence_transformers import SentenceTransformer
import os
from openai import OpenAI

# Function to connect to Milvus
def connect_milvus():
    connections.connect("default", host="127.0.0.1", port="19530")

# Function to create collection
def create_collection(collection_name, dim):
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dim),
        FieldSchema(name="text", dtype=DataType.JSON)
    ]
    schema = CollectionSchema(fields)
    collection = Collection(name=collection_name, schema=schema)
    return collection

# Function to drop existing collection
def drop_collection_if_exists(collection_name):
    if utility.has_collection(collection_name):
        collection = Collection(collection_name)
        collection.drop()

# Function to insert data into Milvus
def insert_data(collection, embeddings, texts):
    data = [
        embeddings,
        [json.dumps({"text": text}) for text in texts]
    ]
    collection.insert(data)

# Function to create an index on the collection
def create_index(collection):
    index_params = {
        "index_type": "IVF_FLAT",
        "params": {"nlist": 100},
        "metric_type": "L2"
    }
    collection.create_index(field_name="embedding", index_params=index_params)

# Function to query Milvus
def query_milvus(collection, model, question):
    question_embedding = model.encode([question])[0].tolist()
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    results = collection.search(
        data=[question_embedding], 
        anns_field="embedding", 
        param=search_params, 
        limit=5, 
        output_fields=["text"]
    )
    return results

# Function to process text file
def process_text_file(file_path):
    with open(file_path, 'r') as file:
        paragraphs = file.read().strip().split('\n\n')
    return paragraphs

# Function to process PDF file
def process_pdf_file(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    
    lines = text.split('\n')
    paragraphs = []
    paragraph = ""
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            if paragraph:
                paragraphs.append(paragraph.strip())
                paragraph = ""
        else:
            if paragraph and (stripped_line[0].isupper() or stripped_line[0].isdigit()):
                paragraphs.append(paragraph.strip())
                paragraph = stripped_line
            else:
                paragraph += " " + stripped_line
    if paragraph:
        paragraphs.append(paragraph.strip())
    return paragraphs

# Main function
def main(file_path, prompt):
    connect_milvus()

    collection_name = "paragraph_collection"
    dim = 384

    drop_collection_if_exists(collection_name)
    collection = create_collection(collection_name, dim)

    if file_path.endswith('.pdf'):
        paragraphs = process_pdf_file(file_path)
    else:
        paragraphs = process_text_file(file_path)

    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embeddings = [model.encode([paragraph])[0].tolist() for paragraph in paragraphs]

    insert_data(collection, embeddings, paragraphs)
    create_index(collection)
    collection.load()

    results = query_milvus(collection, model, prompt)
    relevant_paragraphs = [json.loads(hit.entity.get("text"))["text"] for hit in results[0]]

    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    context = " ".join(relevant_paragraphs)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Answer the following question based on the provided context:\n\n{context}\n\nQuestion: {prompt}"}
        ],
        max_tokens=200
    )

    # # Print the raw response for debugging
    # print("Raw Response:", response)

    if response.choices:
        print("Generated Answer:")
        print(response.choices[0].message.content.strip())
    else:
        print("No response generated")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a paragraph file and query.')
    parser.add_argument('file_path', type=str, help='The path to the paragraph or PDF file.')
    parser.add_argument('prompt', type=str, help='The query prompt.')
    args = parser.parse_args()
    
    if not args.file_path:
        print("Error: No file provided.")
    elif not args.prompt:
        print("Error: No prompt provided.")
    else:
        main(args.file_path, args.prompt)
