import os

from json2parquet import convert_json

# Given PyArrow schema
import pyarrow as pa

def Json2Parq(args=None):
    schema = pa.schema([
        pa.field('QueryID', pa.string),
        pa.field('QueryText', pa.string),
    ])
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    input_filename = "/data/query_logs.json"
    output_filename = "/Users/ka/2020fa-final-project-kumar-anish/data/query_logs.parquet"
    convert_json(input_filename, output_filename)
    print("done...")


if __name__ == "__main__":
    Json2Parq()