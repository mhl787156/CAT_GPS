from influxdb import InfluxDBClient
import os
import json

class InfluxDB:

    def __init__(self) -> None:

        # https://github.com/btashton/flask-influxdb
        influxdb_user = os.getenv("INFLUXDB_USER", "root")

        if os.getenv("INFLUXDB_PASSWORD_FILE"):
            with open(os.getenv("INFLUXDB_PASSWORD_FILE"), 'r') as f:
                influxdb_password = f.readline()
        else:
            influxdb_password = os.getenv("INFLUXDB_PASSWORD", "root")
        influxdb_host = os.getenv("INFLUXDB_HOST", "localhost")
        influxdb_port = os.getenv("INFLUXDB_port", "8086")

        print("user, password:", influxdb_user, influxdb_password)
        print("Host port:", influxdb_host, influxdb_port)
        self.client = InfluxDBClient(
            host=influxdb_host, 
            port=influxdb_port, 
            username=influxdb_user, 
            password=influxdb_password)
    
    def create_and_switch_db(self, db_name="cat_db") -> None:
        dbs = self.client.get_list_database()
        db_names = [d['name'] for d in dbs]
        if db_name not in db_names:
            self.client.create_database(db_name)
        self.client.switch_database(db_name)

    def insert_gps_loc(self, cat, time, lat, long, **fields) -> bool:
        data = {
            "measurement": "gps",
            "tags": {
                "user": cat
            },
            "time": time,
            "fields": {
                "lat": lat,
                "long": long,
                **fields
            }
        }
        json_data = json.dumps(data)

        return self.client.write_points(json_data)

    def get_gps_loc(self, cat):
        res = self.client.get_points(tags={"user": cat})
        return res
    
    def query(self, query):
        return self.client.query(query)