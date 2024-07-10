import requests
from pyspark import errors
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, ArrayType, IntegerType, BooleanType, StringType
from typing import Dict

def london_datastore() -> Dict:
    """
    Fetch data catalogue from London Datastore
    """
    try:
        url = "https://data.london.gov.uk/api/action/package_search"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print("Data Successfully Fetched")
        return data
    except requests.RequestException as e:
        print(f"An error occurred in london_datastore: {str(e)}")
        raise

def create_metadata_dataframe(data: Dict):
    
    try: 
        # Create a SparkSession
        spark = SparkSession.builder.appName("LondonDatastoreMetadata").getOrCreate()

        # Extract the relevant data
        metadata = data['result']['result']

        # Create the data schema
        schema = StructType([
            StructField("owner_org", StringType(), True),
            StructField("maintainer", StringType(), True),
            StructField("relationships_as_object", ArrayType(StringType()), True),
            StructField("relationships_as_subject", ArrayType(StringType()), True),
            StructField("private", BooleanType(), True),
            StructField("maintainer_email", StringType(), True),
            StructField("num_tags", IntegerType(), True),
            StructField("odi-certificate", BooleanType(), True),
            StructField("revision_id", StringType(), True),
            StructField("id", StringType(), True),
            StructField("metadata_created", StringType(), True),
            StructField("metadata_modified", StringType(), True),
            StructField("author", StringType(), True),
            StructField("author_email", StringType(), True),
            StructField("state", StringType(), True),
            StructField("version", StringType(), True),
            StructField("license_id", StringType(), True),
            StructField("type", StringType(), True),
            StructField("num_resources", IntegerType(), True),
            StructField("resources", ArrayType(StructType([
                StructField("mimetype", StringType(), True),
                StructField("cache_url", StringType(), True),
                StructField("hash", StringType(), True),
                StructField("description", StringType(), True),
                StructField("name", StringType(), True),
                StructField("format", StringType(), True),
                StructField("url", StringType(), True),
                StructField("cache_last_updated", StringType(), True),
                StructField("package_id", StringType(), True),
                StructField("created", StringType(), True),
                StructField("state", StringType(), True),
                StructField("mimetype_inner", StringType(), True),
                StructField("last_modified", StringType(), True),
                StructField("position", IntegerType(), True),
                StructField("revision_id", StringType(), True),
                StructField("url_type", StringType(), True),
                StructField("id", StringType(), True),
                StructField("resource_type", StringType(), True),
                StructField("size", IntegerType(), True)
            ])), True),
            StructField("tags", ArrayType(StructType([
                StructField("vocabulary_id", StringType(), True),
                StructField("state", StringType(), True),
                StructField("display_name", StringType(), True),
                StructField("id", StringType(), True),
                StructField("name", StringType(), True)
            ])), True),
            StructField("groups", ArrayType(StructType([
                StructField("display_name", StringType(), True),
                StructField("description", StringType(), True),
                StructField("image_display_url", StringType(), True),
                StructField("title", StringType(), True),
                StructField("id", StringType(), True),
                StructField("name", StringType(), True)
            ])), True),
            StructField("creator_user_id", StringType(), True),
            StructField("name", StringType(), True),
            StructField("isopen", BooleanType(), True),
            StructField("url", StringType(), True),
            StructField("notes", StringType(), True),
            StructField("title", StringType(), True),
            StructField("extras", ArrayType(StructType([
                StructField("key", StringType(), True),
                StructField("value", StringType(), True)
            ])), True),
            StructField("license_title", StringType(), True),
            StructField("organization", StructType([
                StructField("description", StringType(), True),
                StructField("created", StringType(), True),
                StructField("title", StringType(), True),
                StructField("name", StringType(), True),
                StructField("is_organization", BooleanType(), True),
                StructField("state", StringType(), True),
                StructField("image_url", StringType(), True),
                StructField("revision_id", StringType(), True),
                StructField("type", StringType(), True),
                StructField("id", StringType(), True),
                StructField("approval_status", StringType(), True)
            ]), True)
        ])

        # Create a Pyspark DataFrame from the data
        df = spark.createDataFrame(metadata, schema)
        return df
    except errors.PySparkException as error:
        raise error

# Usage
if __name__ == "__main__":
    data = london_datastore()
    metadata_df = create_metadata_dataframe(data)
