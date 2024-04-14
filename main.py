import psycopg2
from flask import Flask
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask app
app = Flask(__name__) 

# Create a general DB to GeoJSON function
def database_to_geojson(table_name):
    try:
        # Create connection to the DB
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
            cur.execute(query)
            data = cur.fetchall()
        
        # Close the connection
        conn.close()
        
        # Return the data
        return data[0][0]
    
    except Exception as e:
        # Log any exceptions
        logging.exception("Error in database_to_geojson function: %s", e)
        return None

# Create the data route
@app.route('/get_elevation_idw_geojson', methods=['GET'])
def get_elevation_idw_geojson():
    try:
        # Call our general function
        ele_idw = database_to_geojson("Idw_mn_temp_1_point")
        if ele_idw:
            return ele_idw
        else:
            return "Error retrieving data from the database", 500  # Internal Server Error
    except Exception as e:
        # Log any exceptions
        logging.exception("Error in get_elevation_idw_geojson route: %s", e)
        return "An unexpected error occurred", 500  # Internal Server Error

# Create the index route
@app.route('/') 
def index(): 
    return "The API is working!"

if __name__ == "__main__":
    # Start the Flask app
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
