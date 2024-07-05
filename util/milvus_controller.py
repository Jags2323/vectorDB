import argparse
from pymilvus import connections, utility, Collection

# Connect to the Milvus server
def connect_to_milvus():
    connections.connect("default", host="127.0.0.1", port="19530")

# List all collections in the Milvus database
def list_collections():
    connect_to_milvus()
    collections = utility.list_collections()
    print("Collections in Milvus:")
    for collection in collections:
        print(collection)

# Show details of a specific collection
def show_collection(collection_name):
    connect_to_milvus()
    if not utility.has_collection(collection_name):
        print(f"Collection '{collection_name}' does not exist.")
        return

    collection = Collection(collection_name)
    print(f"Details of collection '{collection_name}':")
    print(f"Schema: {collection.schema}")

    fields = [field.name for field in collection.schema.fields]
    print("Entities:")
    try:
        results = collection.query(expr="", output_fields=fields, limit=10)
        for result in results:
            if 'embedding' in result:
                result['embedding'] = result['embedding'][:5]  # Limit the vector to the first 5 elements
            print(result)
    except Exception as e:
        print(f"Error querying collection: {e}")

# Delete a specific collection
def delete_collection(collection_name):
    connect_to_milvus()
    if not utility.has_collection(collection_name):
        print(f"Collection '{collection_name}' does not exist.")
        return

    utility.drop_collection(collection_name)
    print(f"Collection '{collection_name}' deleted.")

# Main function to parse command-line arguments and execute appropriate function
def main():
    parser = argparse.ArgumentParser(description="Milvus Controller")
    subparsers = parser.add_subparsers(dest="command")

    # Sub-command to list collections
    subparsers.add_parser("list", help="List all collections in Milvus")

    # Sub-command to show a collection
    show_parser = subparsers.add_parser("show", help="Show details of a collection")
    show_parser.add_argument("collection_name", type=str, help="Name of the collection to show")

    # Sub-command to delete a collection
    delete_parser = subparsers.add_parser("delete", help="Delete a collection")
    delete_parser.add_argument("collection_name", type=str, help="Name of the collection to delete")

    args = parser.parse_args()

    if args.command == "list":
        list_collections()
    elif args.command == "show":
        show_collection(args.collection_name)
    elif args.command == "delete":
        delete_collection(args.collection_name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
