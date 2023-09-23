from flask import Flask
from influxdb import InfluxDBClient
import os

app = Flask(__name__)

# https://github.com/btashton/flask-influxdb
influxdb_user = os.getenv("INFLUXDB_USER", "root")
influxdb_password = os.getenv("INFLUXDB_PASSWORD", "root")
influxdb_host = os.getenv("INFLUXDB_HOST", "localhost")
influxdb_port = os.getenv("INFLUXDB_port", "8086")
client = InfluxDBClient(host=influxdb_host, port=influxdb_port, 
						username=influxdb_user, password=influxdb_password)

@app.route('/')
def hello():
	output = "Hello World!"
	client.create_database('cat_gps_db')
	db_list = client.get_list_database()
	return output + str(db_list)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)
