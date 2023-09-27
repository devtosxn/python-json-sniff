import json
import os
import sys
from sniffer import Sniffer

print("================================================")
print("Starting program ...")
print("================================================")
strict = False if len(sys.argv) > 1 and sys.argv[1] == 'nostrict' else True
print("Strict Mode: {}".format(strict))

schema_dir = "./schema"
os.makedirs(schema_dir, exist_ok=True)

#SPECIFY PATH TO YOUR JSON FILE HERE
JSON_FILE_PATH = "./data/data_1.json"

file_number = os.path.splitext(JSON_FILE_PATH)[0].split("_")[-1]
file_number = int(file_number) if file_number.isnumeric() else 0
schema_file = f"{schema_dir}/schema_{file_number}.json"
        

sniffer = Sniffer(JSON_FILE_PATH, strict=strict)
schema = sniffer.sniff_schema()

with open(schema_file, "w") as file:
    json.dump(schema, file, indent=2)
