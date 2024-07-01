import argparse
import json
import fitz  # PyMuPDF
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
from sentence_transformers import SentenceTransformer

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
    
    # Split text into lines
    lines = text.split('\n')

    # Group lines into paragraphs based on typical paragraph formatting
    paragraphs = []
    paragraph = ""
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            # Empty line indicates a new paragraph
            if paragraph:
                paragraphs.append(paragraph.strip())
                paragraph = ""
        else:
            if paragraph and (stripped_line[0].isupper() or stripped_line[0].isdigit()):
                # New paragraph if the line starts with an uppercase letter or a number and the paragraph is not empty
                paragraphs.append(paragraph.strip())
                paragraph = stripped_line
            else:
                # Continue the current paragraph
                paragraph += " " + stripped_line

    # Add the last paragraph if not empty
    if paragraph:
        paragraphs.append(paragraph.strip())
    
    # print("Extracted paragraphs:")
    # for p in paragraphs:
    #     print(f"{p}\n{'-'*50}")
    
    return paragraphs

# Main function
def main(file_path, prompt):
    connect_milvus()

    collection_name = "paragraph_collection"
    dim = 384  # Correct dimension for the embeddings from the model

    # Drop existing collection if it exists
    drop_collection_if_exists(collection_name)

    # Create a new collection
    collection = create_collection(collection_name, dim)

    # Determine file type and process accordingly
    if file_path.endswith('.pdf'):
        paragraphs = process_pdf_file(file_path)
    else:
        paragraphs = process_text_file(file_path)

    # Vectorize the paragraphs
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embeddings = [model.encode([paragraph])[0].tolist() for paragraph in paragraphs]

    # Insert data into Milvus
    insert_data(collection, embeddings, paragraphs)

    # Create an index on the collection
    create_index(collection)

    # Load the collection to make it searchable
    collection.load()

    # Query the database
    results = query_milvus(collection, model, prompt)

    # Extract and print the text and distance from the query results
    if results:
        for hit in results[0]:
            result_text = json.loads(hit.entity.get("text"))["text"]
            print("----------------------")
            print("Matched text:", result_text)
            print("Distance:", hit.distance)

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
