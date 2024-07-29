from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()
    
    def insert_data(self, data):
        with self.driver.session() as session:
            try:
                for item in data:
                    session.run(
                        "MERGE (n:Text {content: $content}) RETURN n",
                        content=item["text"]
                    )
            except Exception as e:
                print(f"Failed to insert data into Neo4j: {e}")

    def generate_graph(self):
        with self.driver.session() as session:
            try:
                result = session.run(
                    "MATCH (n:Text) RETURN n.content AS content"
                )
                graph_data = [record["content"] for record in result]
                return graph_data
            except Exception as e:
                print(f"Failed to generate graph from Neo4j: {e}")
                return []

