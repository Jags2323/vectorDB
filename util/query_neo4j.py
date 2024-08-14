from neo4j import GraphDatabase
import json

# Replace with your local Neo4j database URI
URI = "bolt://localhost:7687"
AUTH = None  # If you have credentials, replace None with (username, password)

# Initialize the Neo4j driver
driver = GraphDatabase.driver(URI, auth=AUTH)

def query_neo4j(driver, query, parameters=None):
    """
    Function to query Neo4j and return results.
    
    :param driver: The Neo4j driver instance.
    :param query: The Cypher query to execute.
    :param parameters: Optional dictionary of parameters for the query.
    :return: List of records from the query result.
    """
    with driver.session() as session:
        try:
            result = session.execute_read(lambda tx: tx.run(query, parameters).data())
            return result
        except Exception as e:
            print(f"Error occurred: {e}")
            return []

def write_results_to_file(results, file_path):
    """
    Writes query results to a JSON file.

    :param results: The query results to write.
    :param file_path: The path to the file where results should be saved.
    """
    with open(file_path, 'w') as file:
        json.dump(results, file, default=str, indent=4)

def get_all_integrations(file_path):
    """
    Retrieves all Integration nodes and their properties and saves to file.
    """
    query = "MATCH (i:Integration) RETURN i"
    results = query_neo4j(driver, query)
    write_results_to_file(results, file_path)

def get_integrations_by_source(source_app_name, file_path):
    """
    Retrieves integrations that have a specific source application and saves to file.

    :param source_app_name: The name of the source application.
    :param file_path: The path to the file where results should be saved.
    """
    query = """
    MATCH (i:Integration)-[:HAS_SOURCE]->(a:Application)
    WHERE a.name = $source_app_name
    RETURN i
    """
    results = query_neo4j(driver, query, parameters={"source_app_name": source_app_name})
    write_results_to_file(results, file_path)

def get_routes_for_integration(integration_id, file_path):
    """
    Retrieves routes associated with a specific integration and saves to file.

    :param integration_id: The ID of the integration.
    :param file_path: The path to the file where results should be saved.
    """
    query = """
    MATCH (i:Integration {id: $integration_id})-[:HAS_ROUTE]->(r:Route)
    RETURN r
    """
    results = query_neo4j(driver, query, parameters={"integration_id": integration_id})
    write_results_to_file(results, file_path)

if __name__ == "__main__":
    # File path to save results
    file_path = '/Users/jags/Documents/GitHub/vectorDB/sample.json'

    # Uncomment the desired functions to run

    # Get all integrations and save to file
    # get_all_integrations(file_path)

    # Get integrations with source "Customer Interact" and save to file
    # get_integrations_by_source("Customer Interact", file_path)

    # Get routes for a specific integration (replace with an actual ID) and save to file
    get_routes_for_integration("I0001", file_path)

    # Close the driver connection when done
    driver.close()
