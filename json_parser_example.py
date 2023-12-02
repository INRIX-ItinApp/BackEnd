# This file is an example of how to parse JSON data in Python.
# To run this file, open a terminal and run the following command (make sure you are in the same directory):
# python3 json_parser_example.py  

import json

# Example JSON response with nested values
json_response = '''
{
  "person": {
    "name": "John",
    "age": 30,
    "address": {
      "city": "New York",
      "zipcode": "10001"
    }
  }
}
'''

# Parse the JSON response
try:
    # Load the JSON response into a Python dictionary
    data = json.loads(json_response)
    
    # Accessing nested values
    person_name = data['person']['name']
    person_age = data['person']['age']
    address_city = data['person']['address']['city']
    address_zipcode = data['person']['address']['zipcode']

    # Print the values
    print("Name:", person_name)
    print("Age:", person_age)
    print("City:", address_city)
    print("Zipcode:", address_zipcode)

except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
