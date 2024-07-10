import json
import boto3
import botocore
import botocore.exceptions
import requests

from loguru import logger


def get_param(parameter_name: str, region_name: str = "eu-west-2") -> str:
    """
    Retrieve a parameter from AWS Systems Manager Parameter Store.
    """
    ssm = boto3.client('ssm', region_name=region_name)
    try:
        response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
        return response['Parameter']['Value']
    except Exception as e:
        logger.error(f"Unable to retrieve parameter {parameter_name}: {str(e)}")
        raise e

def get_secret(secret_name: str, region_name: str = "eu-west-2") -> json:
    """
    Create an AWS Secrets Manager client. 
    
    Returns a JSON with env vars. 
    """
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager',
                            region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except Exception as e:
        logger.error(f"Unable to retrieve secret {secret_name}: {str(e)}")
        raise e
    else:
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)

def lambda_handler(event, context) -> json:
    """
    AWS Lambda function to fetch data catalogue from London Datastore and dump it to S3
    """
    try:
        secret_name = get_param("herding_cats_param")
        secret = get_secret(secret_name)
        bucket_name = secret["herding_cats_raw_data_bucket"]
        
        url = "https://data.london.gov.uk/api/action/package_search"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print("Data Successfully Fetched")

        # Dump data to S3
        s3 = boto3.client('s3')
        bucket_name = bucket_name
        file_name = 'london_datastore.json'
        
        s3.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=json.dumps(data),
            ContentType='application/json'
        )
        logger.success(f"Data Successfully Dumped")

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