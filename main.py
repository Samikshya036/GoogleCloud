from flask import Flask, jsonify
import os
import psycopg2
from psycopg2 import pool
import sys

# create the Flask app
app = Flask(__name__)

# Database connection pool setup
try:
    postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20,
                                                         user=os.getenv("DB_USER", "postgres"),
                                                         password=os.getenv("DB_PASSWORD", "your_password"),
                                                         host=os.getenv("DB_HOST", "34.71.94.96"),
                                                         port=os.getenv("DB_PORT", "5432"),
                                                         database=os.getenv("DB_NAME", "gis5572"))
except (Exception, psycopg2.DatabaseError) as error:
    print("Error while connecting to PostgreSQL", error)
    sys.exit(1)

# Route to check if the API is working
@app.route('/')
def index():
    return "The API is working!"

# Function to convert DB data to GeoJSON
def database_to_geojson(table_name):
    conn = None
    try:
        # get connection from the pool
        conn = postgreSQL_pool.getconn()
        if conn:
            cur = conn.cursor()
            query = f"""
            SELECT JSON_BUILD_OBJECT(
                'type', 'FeatureCollection',
                'features', JSON_AGG(
                    ST_AsGeoJson(t.*)::json
                )
            )
            FROM {table_name} as t;
            """
            cur.execute(query)
            data = cur.fetchall()
            cur.close()
            return data[0][0]
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while fetching data from PostgreSQL", error)
        return {}
    finally:
        if conn:
            postgreSQL_pool.putconn(conn)

# Route to get elevation data in GeoJSON format
@app.route('/get_elevation_idw_geojson', methods=['GET'])
def get_elevation_idw_geojson():
    try:
        ele_idw = database_to_geojson("idwelevationpoints_in_sde")
        return jsonify(ele_idw)
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
