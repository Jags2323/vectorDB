import os
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
from sentence_transformers import SentenceTransformer
from . import file_processing

# Function to connect to Milvus
def _connect_milvus(host="127.0.0.1", port="19530"):
    connections.connect("default", host=host, port=port)

# Function to create collection
def _create_collection(collection_name, dim):
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dim),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=10000)
    ]
    schema = CollectionSchema(fields)
    collection = Collection(name=collection_name, schema=schema)
    return collection

# Function to drop existing collection
def _drop_collection(collection_name):
    if utility.has_collection(collection_name):
        collection = Collection(collection_name)
        collection.drop()

# Function to insert data into Milvus
def _insert_data(collection, embeddings, texts):
    data = [
        embeddings,
        texts  # Insert plain strings
    ]
    collection.insert(data)

# Function to create an index on the collection
def _create_index(collection):
    index_params = {
        "index_type": "IVF_FLAT",  # Change to FAISS index type
        "params": {"nlist": 100},
        "metric_type": "L2"  # L2 can still be used as metric_type in FAISS
    }
    collection.create_index(field_name="embedding", index_params=index_params)

# Function to query Milvus
def _query_milvus(collection_name, model, question):
    collection = Collection(collection_name)
    question_embedding = model.encode([question])[0].tolist()
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}  # Adjust as necessary for FAISS
    results = collection.search(
        data=[question_embedding], 
        anns_field="embedding", 
        param=search_params, 
        limit=10, 
        output_fields=["text"]
    )
    return results

# Function to process different file types
def _process_file(file_path):
    if file_path.endswith('.xml'):
        return file_processing.process_xml_file_by_tag(file_path)
    elif file_path.endswith('.pdf'):
        return file_processing.process_pdf_file(file_path)
    elif file_path.endswith('.json'):
        return file_processing.process_json_file(file_path)
    else:
        return file_processing.process_text_file(file_path)

def generate_and_save_data(path, collection_name, host="127.0.0.1", port="19530", dim=384):
    _connect_milvus(host, port)
    
    # Check if collection exists
    if not utility.has_collection(collection_name):
        # Create a new collection if it doesn't exist
        collection = _create_collection(collection_name, dim)
    else:
        # Use the existing collection
        collection = Collection(collection_name)
    
    text_segments = []

    # Check if the provided path is a directory or a single file
    if os.path.isdir(path):
        # Iterate through each file in the folder
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                text_segments.extend(_process_file(file_path))
    elif os.path.isfile(path):
        # Process the single file
        text_segments.extend(_process_file(path))
    else:
        raise ValueError("The provided path is neither a directory nor a file")

    # Vectorize the text_segments
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embeddings = [model.encode([text_segment])[0].tolist() for text_segment in text_segments]

    # Insert data into Milvus
    _insert_data(collection, embeddings, text_segments)

    # Create an index on the collection if it's a new collection
    if not collection.has_index():
        _create_index(collection)

# Public function to query the Milvus collection and return results as JSON
def query_collection(collection_name, prompt, host="127.0.0.1", port="19530"):
    _connect_milvus(host, port)
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    
    # Load the collection to make it searchable
    collection = Collection(collection_name)
    collection.load()

    # Query the database
    results = _query_milvus(collection_name, model, prompt)

    # Extract and return the text and distance from the query results
    result_list = []
    if results:
        for hit in results[0]:
            result_text = hit.entity.get("text")  # Directly get the text
            result_list.append({
                "text": result_text,
                "distance": hit.distance
            })
    return result_list

# Public function to delete a collection
def delete_collection(collection_name, host="127.0.0.1", port="19530"):
    _connect_milvus(host, port)
    _drop_collection(collection_name)
