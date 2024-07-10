import json
import boto3
import botocore
import botocore.exceptions
import requests

from loguru import logger

from get_creds import get_param, get_secret
from urllib.parse import urlparse

def lambda_handler(event, context) -> json:
    """
    AWS Lambda function to fetch UK open data catalogues. 
    
    Loop through links and dump catalogue data to s3 bucket.  
    """
    
    catalogues_list = [
        "https://data.london.gov.uk/api/action/package_search",
        "https://opendata.bristol.gov.uk/api/feed/dcat-ap/2.1.1.json"
    ]
    
    try:
        # Fetch aws params and secrets
        secret_name = get_param("herding_cats_param")
        secret = get_secret(secret_name)
        bucket_name = secret["herding_cats_raw_data_bucket"]
        
        # Loop through the links
        for link in catalogues_list:
            response = requests.get(link, timeout=15)
            response.raise_for_status()
            data = response.json()
            logger.success(f"Data Successfully Fetched for {link}")
            
            # Extract domain name from the link
            domain = urlparse(link).netloc
            
            # Use domain as file name
            file_name = f"{domain}.json"
            
            # Dump data to S3
            s3 = boto3.client('s3')
            s3.put_object(
                Bucket=bucket_name,
                Key=file_name,
                Body=json.dumps(data),
                ContentType='application/json'
            )
            logger.success(f"Data Was Successfully Dumped to {file_name}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Data successfully fetched and dumped to S3'})
        }
    except requests.RequestException as e:
        print(f"An error occurred while fetching data: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Data fetch error: {str(e)}'})
        }
    except botocore.exceptions.ClientError as e:
        print(f"An error occurred while dumping to S3: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'S3 dump error: {str(e)}'})
        }
