from transformers import BertTokenizer, TFBertModel
from pinecone import Pinecone, ServerlessSpec
import numpy as np

# Initialize Pinecone
pc = Pinecone(api_key="e93f49a0-7115-4c93-8ae8-0a0901046d94")

# Define the index name and dimension
index_name = "vectorquery"
dimension = 768  # Dimension of BERT embeddings

# List existing indexes
existing_indexes = pc.list_indexes()

# Create the index if it does not exist
if index_name not in existing_indexes:
    try:
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="euclidean", 
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        print(f"Index '{index_name}' created.")
    except PineconeApiException as e:
        print(f"Failed to create index '{index_name}': {e}")

# Connect to the Pinecone index
index = pc.Index(index_name)

# Load the pre-trained BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = TFBertModel.from_pretrained('bert-base-uncased')

# Define a function to encode text using BERT
def encode_text(text):
    encoded_input = tokenizer(text, return_tensors='tf')
    input_ids = encoded_input['input_ids']
    attention_mask = encoded_input['attention_mask']
    outputs = model(input_ids, attention_mask=attention_mask)
    cls_token = outputs.last_hidden_state[:, 0, :]
    cls_token_numpy = cls_token.numpy().flatten()  # Convert to a 1D numpy array
    cls_token_list = cls_token_numpy.tolist()  # Convert to a list of floats
    return cls_token_list

# Encode and store sample text
def store_text(text, text_id):
    text_vector = encode_text(text)
    metadata = {"text": text}
    index.upsert(vectors=[{"id": text_id, "values": text_vector, "metadata": metadata}])
    print(f"Text '{text}' stored with ID '{text_id}' in Pinecone!")

# Store sample text
store_text("This is a sample text for BERT vectorization.", "vectorDB")

# Define a function to query the Pinecone index
def query_pinecone(query_text, top_k=3):
    query_vector = encode_text(query_text)
    
    # Debug: Print the query vector
    print("Query vector:", query_vector)

    # Validate vector dimension and type
    if len(query_vector) != dimension:
        raise ValueError(f"Query vector dimension mismatch: expected {dimension}, got {len(query_vector)}")
    if not all(isinstance(v, (int, float)) for v in query_vector):
        raise ValueError("Query vector contains non-numeric values")

    # Perform the query
    query_response = index.query(queries=[query_vector], top_k=top_k)
    print("Query results:")
    for match in query_response['matches']:
        print(f"ID: {match['id']}, Score: {match['score']}, Metadata: {match['metadata']}")

# Perform a sample query
query_pinecone("Sample query text.", top_k=3)
