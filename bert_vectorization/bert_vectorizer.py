from transformers import BertTokenizer, TFBertModel
from pinecone import Pinecone, ServerlessSpec

# Initialize Pinecone
pc = Pinecone(api_key="e93f49a0-7115-4c93-8ae8-0a0901046d94")

# Define the index name and dimension
index_name = "vector"
dimension = 768  # Dimension of BERT embeddings

# List existing indexes
existing_indexes = pc.list_indexes()

# Create the index if it does not exist
if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=dimension,
        metric="euclidean", 
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

# Connect to the Pinecone index
index = pc.Index(index_name)

# Load your data (text)
text = "This is a sample text for BERT vectorization."

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
    return cls_token.numpy().flatten()  # Flatten the tensor to a 1D array of floats

# Encode the sample text
text_vector = encode_text(text)

# Define metadata (optional)
metadata = {"text": text}

# Store the vector and metadata in Pinecone
index.upsert(vectors=[{"id": "vectorDB", "values": text_vector.tolist(), "metadata": metadata}])

print("Text vector stored in Pinecone!")
