# Import necessary libraries
from pymilvus import connections, Collection, utility

# Function to connect to Milvus
def connect_milvus():
    connections.connect("default", host="127.0.0.1", port="19530")

# Function to list all collections
def list_collections():
    return utility.list_collections()

# Function to retrieve vectors from a collection
def retrieve_vectors(collection_name):
    if not utility.has_collection(collection_name):
        print(f"Collection {collection_name} does not exist.")
        return

    collection = Collection(collection_name)
    
    # Load the collection to make it queryable
    collection.load()
    
    # Retrieve all vectors and their corresponding text
    # Use an expression that matches all records
    vectors = collection.query(expr="id >= 0", output_fields=["embedding", "text"])
    
    # Print the vectors and their corresponding text
    for vector in vectors:
        print("--------------------")
        print(f"Text: {vector['text']}")
        print(f"Vector: {vector['embedding'][:5]}... (truncated for brevity)")

def main():
    connect_milvus()

    collections = list_collections()
    if not collections:
        print("No collections found.")
        return

    print("Available collections:")
    for idx, collection_name in enumerate(collections):
        print(f"{idx}: {collection_name}")

    try:
        selected_index = int(input("Enter the number of the collection you want to read: "))
        if selected_index < 0 or selected_index >= len(collections):
            print("Invalid index selected.")
            return

        selected_collection = collections[selected_index]
        print(f"Retrieving vectors from collection: {selected_collection}")
        retrieve_vectors(selected_collection)
    except ValueError:
        print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
