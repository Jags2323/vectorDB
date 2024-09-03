import os
from neo4j import GraphDatabase
import pandas as pd
from sqlalchemy import create_engine

def execute_mysql_query(query, database):
    """
    Executes an SQL query on a specified MySQL database.

    Args:
    query (str): The SQL query to be executed.
    database (str): The name of the database to execute the query against.

    Returns:
    list: A list of dictionaries containing the query results.
    str: An error message if an exception occurs.
    """
    # Hardcoded connection details
    user = 'root'
    password = 'qwerty'
    host = 'localhost'
    port = 3306

    # Create the connection string
    connection_string = f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}'

    try:
        # Create the SQLAlchemy engine
        engine = create_engine(connection_string)
        
        # Execute the query
        df = pd.read_sql_query(query, engine)
        
        # Convert the result to JSON
        result_json = df.to_json(orient='records')
        
        return result_json
    
    except Exception as e:
        return str(e)
    
def execute_cypher_query(query):
    """
    Executes a Cypher query on the Neo4j database.

    Args:
    query (str): The Cypher query to be executed.

    Returns:
    list: A list of dictionaries containing the query results.
    str: An error message if an exception occurs.
    """
    NEO4J_URI = "neo4j+ssc://ae9fac9e.databases.neo4j.io"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD")

    try:
        # Connect to the Neo4j database
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    except Exception as e:
        return str(e)
    
    try:
        # Open a session
        with driver.session() as session:
            # Execute the Cypher query
            result = session.run(query)
            
            # Collect the results
            results = [record.data() for record in result]
            return results
    
    except Exception as e:
        print("An error occurred while executing the query or collecting results:", e)
        return str(e)
    
    finally:
        driver.close()

def get_temperature(city_name):
    # Hardcoded temperatures for three specific cities
    temperatures = {
        "New York": 22,     # Temperature in degrees Celsius
        "Los Angeles": 28,  # Temperature in degrees Celsius
        "Chicago": 18       # Temperature in degrees Celsius
    }

    # Convert city name to the proper format
    city_name = city_name.title()

    # Check if the city is in the dictionary and return the temperature in the appropriate format
    if city_name in temperatures:
        return {
            "city": city_name,
            "temperature": temperatures[city_name]
        }
    else:
        return {
            "error": "City not found in the database."
        }