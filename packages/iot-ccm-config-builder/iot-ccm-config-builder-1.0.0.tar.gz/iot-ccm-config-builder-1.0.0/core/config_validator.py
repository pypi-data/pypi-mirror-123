import json
from jsonschema import validate


def check_config(file):
    json_file = json.load(file)
    schema_file = open("./docs/schema_IOT.json")
    json_schema = json.load(schema_file)
    schema_file.close()

    try:
        validate(instance=json_file, schema=json_schema)
        print("Congratulations! The configurations file validates the schema successfully!")
    except Exception as e:
        print(e)
        print("Error! The configurations file DOES NOT validate the schema...")
