from flask import Flask, request
from db import InfluxDB
import os
import subprocess
import time


delay_time = float(os.getenv("DELAY_START", 0.0))
print("Delaying start:", delay_time)
time.sleep(delay_time)

app = Flask(__name__)
db = InfluxDB()
db.create_and_switch_db("catgps")

@app.route('/')
def hello():
	output = "Hello World!"
	return output

@app.route("/gps", methods=["GET", "POST"])
def gps():
	# Pass from the cat
	cat = request.args["cat"]
	if request.method == "POST":
		print("Received POST Request", request)
		time = request.args["time"]
		lat = request.args["lat"]
		lon = request.args["lon"]
		alt = request.args["alt"]
		success = db.insert_gps_loc(cat, time, lat, lon, alt=alt)
		return str(success)
	else: #GET METHOD
		print("Received GET Request", request)
		locs = db.get_gps_loc(cat)
		return str(locs)
		

if __name__ == '__main__':
	server_ip=os.getenv("SERVER_HOST", "0.0.0.0")
	server_port=os.getenv("SERVER_PORT", 8000)
	app.run(host=server_ip, port=server_port)
