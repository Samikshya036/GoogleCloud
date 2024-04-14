from flask import Flask, jsonify
import psycopg2
from shapely.wkb import loads

# PostGIS database connection details
dbname = 'gis5572'
user = 'postgres'
password = 'Hyderabad43%'
host = '35.238.64.215'  # Cloud DB Public IP address
port = '5432'

app = Flask(__name__)

def connect_to_postgres():
    try:
        connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

@app.route('/temp_points', methods=['GET'])
def get_temp_points():
    connection = connect_to_postgres()
    if connection:
        try:
            cursor = connection.cursor()

            # Define table name
            table_name = 'mn_clean_weather'

            sql_query = f"SELECT shape FROM {table_name};"
            cursor.execute(sql_query)
            rows = cursor.fetchall()

            features = []
            for row in rows:
                try:
                    geojson = wkb_to_geojson(row[0])
                    features.append({"type": "Feature", "geometry": geojson})
                except Exception as e:
                    print(f"Error converting geometry: {e}")

            cursor.close()
            connection.close()

            return jsonify({"type": "FeatureCollection", "features": features})
        except psycopg2.Error as e:
            print(f"Error executing SQL query: {e}")
            return jsonify({"error": "Internal Server Error"}), 500
    else:
        return jsonify({"error": "Database Connection Error"}), 500

@app.route('/temp_accuracy', methods=['GET'])
def get_temp_accuracy():
    connection = connect_to_postgres()
    if connection:
        try:
            cursor = connection.cursor()

            # Define table name
            table_name = 'diff_krigord_temp_points'

            sql_query = f"SELECT shape FROM {table_name};"
            cursor.execute(sql_query)
            rows = cursor.fetchall()

            features = []
            for row in rows:
                try:
                    geojson = wkb_to_geojson(row[0])
                    features.append({"type": "Feature", "geometry": geojson})
                except Exception as e:
                    print(f"Error converting geometry: {e}")

            cursor.close()
            connection.close()

            return jsonify({"type": "FeatureCollection", "features": features})
        except psycopg2.Error as e:
            print(f"Error executing SQL query: {e}")
            return jsonify({"error": "Internal Server Error"}), 500
    else:
        return jsonify({"error": "Database Connection Error"}), 500

@app.route('/elev_points', methods=['GET'])
def get_elev_points():
    connection = connect_to_postgres()
    if connection:
        try:
            cursor = connection.cursor()

            # Define table name
            table_name = 'mndem_points_points'

            sql_query = f"SELECT shape FROM {table_name};"
            cursor.execute(sql_query)
            rows = cursor.fetchall()

            features = []
            for row in rows:
                try:
                    geojson = wkb_to_geojson(row[0])
                    features.append({"type": "Feature", "geometry": geojson})
                except Exception as e:
                    print(f"Error converting geometry: {e}")

            cursor.close()
            connection.close()

            return jsonify({"type": "FeatureCollection", "features": features})
        except psycopg2.Error as e:
            print(f"Error executing SQL query: {e}")
            return jsonify({"error": "Internal Server Error"}), 500
    else:
        return jsonify({"error": "Database Connection Error"}), 500

@app.route('/elev_accuracy', methods=['GET'])
def get_elev_accuracy():
    connection = connect_to_postgres()
    if connection:
        try:
            cursor = connection.cursor()

            # Define table name
            table_name = 'elev_ord_accuracy'

            sql_query = f"SELECT shape FROM {table_name};"
            cursor.execute(sql_query)
            rows = cursor.fetchall()

            features = []
            for row in rows:
                try:
                    geojson = wkb_to_geojson(row[0])
                    features.append({"type": "Feature", "geometry": geojson})
                except Exception as e:
                    print(f"Error converting geometry: {e}")

            cursor.close()
            connection.close()

            return jsonify({"type": "FeatureCollection", "features": features})
        except psycopg2.Error as e:
            print(f"Error executing SQL query: {e}")
            return jsonify({"error": "Internal Server Error"}), 500
    else:
        return jsonify({"error": "Database Connection Error"}), 500

def wkb_to_geojson(wkb):
    geometry = loads(wkb, hex=True)
    return geometry.__geo_interface__

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
