from neo4j import GraphDatabase
import json
import os
import re

# Replace with your local Neo4j database URI
URI = "bolt://localhost:7687"
AUTH = None  # If you have credentials, replace None with (username, password)

# Initialize the Neo4j driver
driver = GraphDatabase.driver(URI, auth=AUTH)

# Function to verify connection
def verify_connection(driver):
    try:
        with driver.session() as session:
            result = session.execute_write(lambda tx: tx.run("RETURN 1").single())
            if result:
                print("Connection established.")
            else:
                print("Connection test failed.")
    except Exception as e:
        print(f"Error occurred: {e}")

# Function to process JSON file
def process_json_file(file_path):
    json_segments = []
    print(f"Started processing JSON file: {file_path}")

    try:
        with open(file_path, 'r') as file:
            json_data = file.read()
        
        if not json_data.strip():
            return json_segments
        
        data = json.loads(json_data)
        
        if isinstance(data, list):
            for obj in data:
                if isinstance(obj, dict):
                    json_segments.append(obj)
        elif isinstance(data, dict):
            json_segments.append(data)
        else:
            print("Unsupported JSON format")
            
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return json_segments

# Function to insert data into Neo4j
def insert_data(driver, data):
    with driver.session() as session:
        try:
            for integration in data:
                # Flatten complex properties if needed
                def flatten_properties(properties):
                    flattened = {}
                    for key, value in properties.items():
                        if isinstance(value, (dict, list)):
                            flattened[key] = json.dumps(value)  # Serialize complex objects
                        else:
                            flattened[key] = value
                    return flattened

                # Create the Integration node
                query = """
                CREATE (i:Integration {
                    id: $id,
                    name: $name,
                    description: $description,
                    target: $target,
                    environment: $environment,
                    country: $country,
                    instance: $instance,
                    minVolume: $minVolume,
                    avgVolume: $avgVolume,
                    maxVolume: $maxVolume,
                    template: $template,
                    entryDt: datetime($entryDt),
                    keys: $keys
                })
                """
                session.run(query,
                            id=integration['id'],
                            name=integration['name'],
                            description=integration['description'],
                            target=integration.get('target', ''),
                            environment=integration['environment'],
                            country=integration['country'],
                            instance=integration['instance'],
                            minVolume=integration['minVolume'],
                            avgVolume=integration['avgVolume'],
                            maxVolume=integration['maxVolume'],
                            template=integration['template'],
                            entryDt=integration['entryDt'],
                            keys=json.dumps(integration.get('keys', {})))  # Serialize complex objects

                # Create relationships to source applications
                for source_app in integration.get('source', []):
                    query = """
                    MATCH (i:Integration {id: $integration_id})
                    MERGE (a:Application {name: $app_name})
                    CREATE (i)-[:HAS_SOURCE]->(a)
                    """
                    session.run(query,
                                integration_id=integration['id'],
                                app_name=source_app)

                # Create relationships to destination applications
                for dest_app in integration.get('destinations', []):
                    query = """
                    MATCH (i:Integration {id: $integration_id})
                    MERGE (a:Application {name: $app_name})
                    CREATE (i)-[:HAS_DESTINATION]->(a)
                    """
                    session.run(query,
                                integration_id=integration['id'],
                                app_name=dest_app)

                # Create Route nodes and relationships (simplified)
                for route in integration.get('routes', []):
                    query = """
                    MATCH (i:Integration {id: $integration_id})
                    CREATE (r:Route {
                        id: $route_id, 
                        palette: $palette, 
                        properties: $properties
                    })
                    CREATE (i)-[:HAS_ROUTE]->(r)
                    """
                    session.run(query,
                                integration_id=integration['id'],
                                route_id=route['_id'],
                                palette=route['palette'],
                                properties=json.dumps(route.get('properties', {})))  # Serialize complex objects

            print("Data inserted successfully.")
        except Exception as e:
            print(f"Error occurred during data insertion: {e}")

# # Function to process JSON files from a folder and add data to Neo4j
# def process_folder_and_insert_data(folder_path, driver):
#     for filename in os.listdir(folder_path):
#         if filename.endswith(".json"):
#             file_path = os.path.join(folder_path, filename)
#             json_data = process_json_file(file_path)
#             insert_data(driver, json_data)

def process_folder_and_insert_data(file_path, driver):
    """Processes a single JSON file and inserts the data into Neo4j."""
    json_data = process_json_file(file_path)
    insert_data(driver, json_data)


# Verify the connection
verify_connection(driver)

# Path to your JSON file
file_path = '/Users/jags/Documents/GitHub/vectorDB/JSON/integrations.json'

# Process the JSON file and insert data into Neo4j
process_folder_and_insert_data(file_path, driver)

# Close the driver connection when done
driver.close()
