import json
import util.milvus_functions as milvus_functions

def main():
    # File path and collection name
    file_path = "data/paragraphs.txt"
    collection_name = "paragraph_collection"

    # Delete the collection if it exists and generate new data
    milvus_functions.delete_collection(collection_name)
    milvus_functions.generate_and_save_data(file_path, collection_name)
    
    # Querying the collection
    prompt = "What can computer vision do?"
    results = milvus_functions.query_collection(collection_name, prompt)
    
    # Print the JSON results
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
