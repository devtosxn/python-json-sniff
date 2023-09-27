import unittest
import os
from sniffer import Sniffer


class TestSniffer(unittest.TestCase):

    def setUp(self):
        self.json_file_path = "./mock/test.json"
        self.invalid_json_file_path = "./mock/invalid.json"
        self.sniffer = Sniffer(self.json_file_path)
        self.strict_sniffer = Sniffer(self.json_file_path, strict=True)

    def tearDown(self):
        if os.path.exists(self.json_file_path):
            os.remove(self.json_file_path)

    def test_get_data_type_string(self):
        self.assertEqual(self.sniffer._get_data_type("test"), "string")

    def test_get_data_type_string_strict(self):
        self.assertEqual(self.strict_sniffer._get_data_type("test"), "string")

    def test_get_data_type_boolean(self):
        self.assertEqual(self.sniffer._get_data_type(True), "boolean")

    def test_get_data_type_boolean_strict(self):
        self.assertEqual(self.strict_sniffer._get_data_type(True), "undefined")

    def test_get_data_type_int(self):
        self.assertEqual(self.sniffer._get_data_type(10), "integer")

    def test_get_data_type_int_strict(self):
        self.assertEqual(self.strict_sniffer._get_data_type(10), "integer")

    def test_get_data_type_dict(self):
        self.assertEqual(self.sniffer._get_data_type(
            {"key": "value"}), "dictionary")

    def test_get_data_type_dict_strict(self):
        self.assertEqual(self.strict_sniffer._get_data_type(
            {"key": "value"}), "undefined")

    def test_get_data_type_list(self):
        self.assertEqual(self.sniffer._get_data_type([1, 2, 3]), "enum")

    def test_get_data_type_list_strict(self):
        self.assertEqual(self.strict_sniffer._get_data_type(
            [1, 2, 3]), "undefined")

    def test_get_list_data_type_array(self):
        self.assertEqual(self.sniffer._get_list_data_type(
            [{"key": "value"}, {"key": "value"}]), "array")

    def test_get_empty_list_data_type(self):
        self.assertEqual(self.sniffer._get_list_data_type([]), "array")

    def test_get_empty_list_data_type_strict(self):
        self.assertEqual(self.strict_sniffer._get_list_data_type(
            [], strict=True), "undefined")

    def test_add_common_fields(self):
        schema = {"key_1": {"type": "string"}}
        self.sniffer._add_common_fields(schema["key_1"])
        self.assertDictEqual(schema["key_1"], {
                             "type": "string", "tag": "", "description": "", "required": False})

    def test_sniff_schema(self):
        with open(self.json_file_path, "w") as file:
            file.write(
                '{"message": {"key1": "value1", "key2": {"nested_key": 10}, "key3": [1, 2, "test"]}}')

        expected_schema = {
            "key_one": {"type": "string", "tag": "", "description": "", "required": False},
            "key_two": {"type": "dictionary", "tag": "", "description": "", "required": False},
            "key_three": {"type": "array", "tag": "", "description": "", "required": False}
        }

        self.assertDictEqual(self.sniffer.sniff_schema(), expected_schema)

    def test_sniff_schema_strict(self):
        with open(self.json_file_path, "w") as file:
            file.write(
                '{"message": {"key1": "value1", "key2": {"nested_key": 10}, "key3": [1, 2, "test"]}}')

        expected_schema = {
            "key_one": {"type": "string", "tag": "", "description": "", "required": False},
            "key_two": {"type": "undefined", "tag": "", "description": "", "required": False},
            "key_three": {"type": "undefined", "tag": "", "description": "", "required": False}
        }

        self.assertDictEqual(
            self.strict_sniffer.sniff_schema(), expected_schema)

    def test_sniff_schema_no_message(self):
        with open(self.json_file_path, "w") as file:
            file.write('{"not_message": {"key1": "value1"}}')

        self.assertEqual(self.sniffer.sniff_schema(), {})

    def test_sniff_schema_no_message_strict(self):
        with open(self.json_file_path, "w") as file:
            file.write('{"not_message": {"key1": "value1"}}')

        self.assertEqual(self.strict_sniffer.sniff_schema(), {})

    def test_sniff_schema_file_not_found(self):
        self.assertEqual(self.sniffer.sniff_schema(), {})

    def test_sniff_schema_file_not_found_strict(self):
        self.assertEqual(self.strict_sniffer.sniff_schema(), {})
  
