from pymilvus import connections, utility

# Connect to Milvus
connections.connect("default", host="127.0.0.1", port="19530")

# List all collections
collections = utility.list_collections()
print("Collections:", collections)
