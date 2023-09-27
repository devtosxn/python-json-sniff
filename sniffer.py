import json
from num2words import num2words

class Sniffer:
    data_types = {
        str: "string",
        int: "integer",
        bool: "boolean",
        list: "array",
        dict: "dictionary",
        "undefined": "undefined",
    }

    def __init__(self, json_file, strict=False):
        self.json_file = json_file
        self.strict = strict

    def _get_data_type(self, value):
        if isinstance(value, str):
            return self.data_types[str]
        elif isinstance(value, bool):
            if self.strict:
                return self.data_types["undefined"]
            return self.data_types[bool]
        elif isinstance(value, int):
            return self.data_types[int]
        elif isinstance(value, dict):
            if self.strict:
                return self.data_types["undefined"]
            return self.data_types[dict]
        elif isinstance(value, list):
            return self._get_list_data_type(value, strict=self.strict)
        else:
            return self.data_types["undefined"]

    def _get_list_data_type(self, lst, strict=False):
        if not lst and not strict:
            return "array"
        elif not lst and strict:
            return self.data_types["undefined"]

        contains_str = all(isinstance(item, str) for item in lst)
        contains_int = all(isinstance(item, int) for item in lst)
        contains_bool = all(isinstance(item, bool) for item in lst)
        contains_dict = all(isinstance(item, dict) for item in lst)

        if strict:
            if contains_str:
                return "enum"
            elif contains_dict:
                return "array"
            else:
                return self.data_types["undefined"]
        else:
            if contains_str or contains_int or contains_bool:
                return "enum"
            else:
                return "array"

    def _add_common_fields(self, schema):
        schema.update({"tag": "", "description": "", "required": False})

    def sniff_schema(self):
        try:
            with open(self.json_file, "r") as file:
                json_data = json.load(file)
                message_data = json_data.get("message", {})
                if not message_data:
                    print("No message data found")
                    return {}
                schema = {}
                for index, (key, value) in enumerate(message_data.items()):
                    new_key = "key_" + num2words(index + 1)
                    schema[new_key] = {"type": self._get_data_type(value)}
                    self._add_common_fields(schema[new_key])

                return schema
        except FileNotFoundError:
            print("File not found")
            return {}
