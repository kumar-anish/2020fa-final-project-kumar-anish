import os
import luigi
import requests
import json

url = "http://127.0.0.1:8000/querylog/"

payload = {}
headers = {}
LOCAL_ROOT = os.path.abspath('data')
response = requests.request("GET", url, headers=headers, data=payload)

class SQLLogsToJSON(luigi.Task):
    json_path = LOCAL_ROOT + "/query_logs.json"

    def run(self):
        with self.output().open('w') as qlog_file:
            json.dump(self.response.text, qlog_file)

    def output(self):
        return luigi.LocalTarget(self.json_path)