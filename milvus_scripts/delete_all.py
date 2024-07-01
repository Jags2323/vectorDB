from pymilvus import connections, Collection, utility

# Connect to Milvus
connections.connect("default", host="127.0.0.1", port="19530")

# List all collections
collections = utility.list_collections()
print("Collections:", collections)

# Drop all collections (use with caution)
for collection_name in collections:
    collection = Collection(collection_name)
    collection.drop()
    print(f"Dropped collection: {collection_name}")

# Verify cleanup
collections = utility.list_collections()
print("Collections after cleanup:", collections)
