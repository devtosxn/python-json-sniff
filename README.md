# JSON Sniffer
This program reads a JSON file and creates a schema based on the data types of the values in the `message` attribute if it exists. The schema includes a unique key for each attribute, the attribute's data type, and common fields like "tag", "description", and "required".

## Setup
1. Clone the repository

```
git clone https://github.com/devtosxn/python-json-sniff.git
```
2. Switch into root directory

```
cd python-json-sniff
```

3. Create and activate a virtual environment

```
python3 -m venv venv
source venv/bin/activate
```
4. Install the requirements

```
pip3 install -r requirements.txt
```

## Running the Tests
To run the tests, from the project directory, run the command:

```
python3 -m unittest test_program.py
```

## Running the Program
To run the program, run the following command in the root directory:

```
python3 main.py
```
By default, the program runs in `strict` mode which means that any data type that was not defined in the `PROBLEM.md` specification will be returned as "undefined" based on the specified rules. This will populate `schema_1.json` with the results of the sniffing algorithm

To run the program for a different json file, specify the path to the file in `main.py` 