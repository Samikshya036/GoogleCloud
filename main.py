import psycopg2
from flask import Flask
import os


# create the Flask app
app = Flask(__name__) 

# Connect to the PostgreSQL database

# create the index route
@app.route('/') 
def index(): 
    return "The API is working!"

# create a general DB to GeoJSON function
def database_to_geojson(table_name):
        # create connection to the DB
    conn = psycopg2.connect(
        host = "34.71.94.96",
        database = "gis5572",
        user = "postgres",
        password = "sami@2010",
        port = "5432",
    )
    # retrieve the data
    with conn.cursor() as cur:
        query =f"""
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
    # close the connection
    conn.close()
    
    # Returning the data
    return data [0][0]

# create the data route

@app.route('/get_elevation_idw_geojson', methods=['GET'])
def get_elevation_idw_geojson():
    # call our general function
    ele_idw = database_to_geojson("idwelevationpoints_in_sde")
    return ele_idw
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
