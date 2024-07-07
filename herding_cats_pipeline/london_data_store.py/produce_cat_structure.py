import requests

from pprint import pprint
from pyspark.sql.types import StructType, StructField, StringType, ArrayType

def london_datastore() -> dict:
    """
    Fetch data from London Datastore API and return 1 result as a JSON object.
    """
    try:
        num_rows = 1
        url = f"https://data.london.gov.uk/api/action/package_search?rows={num_rows}"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data: Status code {response.status_code}")
        data = response.json()
        result = data['result']['result'][0]  
        print("Successfully fetched 1 result as JSON")
        return result
    except Exception as e:
        print(f"An error occurred in london_datastore: {str(e)}")
        raise

def infer_pyspark_schema_from_json(json_obj: dict) -> StructType:
    """
    Infer PySpark schema from a JSON object.
    """
    def infer_field_type(value):
        if isinstance(value, dict):
            return StructType([StructField(k, infer_field_type(v), True) for k, v in value.items()])
        elif isinstance(value, list):
            if value:
                return ArrayType(infer_field_type(value[0]))
            else:
                return ArrayType(StringType())
        else:
            return StringType()

    return StructType([StructField(k, infer_field_type(v), True) for k, v in json_obj.items()])

def pretty_print_schema(schema, indent=0):
    for field in schema.fields:
        print("  " * indent + f"- {field.name}: {field.dataType}")
        if isinstance(field.dataType, StructType):
            pretty_print_schema(field.dataType, indent + 1)
        elif isinstance(field.dataType, ArrayType) and isinstance(field.dataType.elementType, StructType):
            print("  " * (indent + 1) + "Array of:")
            pretty_print_schema(field.dataType.elementType, indent + 2)
            

if __name__ == "__main__":
    # Get the JSON data
    json_data = london_datastore()
    
    print("Keys and their values in the JSON data:")
    for key, value in json_data.items():
        print(f"{key}:")
        
        # Check if the value is a list or dictionary for better formatting
        if isinstance(value, (list, dict)):
            print(f"  {value}")
        else:
            print(f"  {value}")
        
        print() 
