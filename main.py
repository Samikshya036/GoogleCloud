import psycopg2
from flask import Flask, jsonify
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask app
app = Flask(__name__) 

# Function to retrieve data from the database and convert it to GeoJSON
def database_to_geojson(table_name):
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host="34.132.34.153",
            database="gis5572",
            user="postgres",
            password="sami@2010",
            port="5432",
        )
        
        # Retrieve the data
        with conn.cursor() as cur:
            query = f"""
                SELECT JSON_BUILD_OBJECT(
                    'type', 'FeatureCollection',
                    'features', JSON_AGG(
                        ST_AsGeoJson({table_name}.*)::json
                    )
                )
                FROM {table_name};
            """
            logging.debug("Executing SQL query: %s", query)  # Log SQL query
            cur.execute(query)
            data = cur.fetchone()[0]  # Fetch single row
            
            # Close the cursor and connection
            cur.close()
            conn.close()
            
            return data
        
    except Exception as e:
        # Log any exceptions
        logging.exception("Error retrieving data from database: %s", e)
        return None

# Route to retrieve data as GeoJSON
@app.route('/get_elevation_idw_geojson', methods=['GET'])
def get_elevation_idw_geojson():
    try:
        # Call the database_to_geojson function
        geojson_data = database_to_geojson("Idw_mn_temp_1_point")
        
        if geojson_data:
            return jsonify(geojson_data)
        else:
            return "Error retrieving data from the database", 500  # Internal Server Error
    
    except Exception as e:
        # Log any exceptions
        logging.exception("Error in get_elevation_idw_geojson route: %s", e)
        return "An unexpected error occurred", 500  # Internal Server Error

# Route for the index page
@app.route('/') 
def index(): 
    return "The API is working!"

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

