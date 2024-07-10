import boto3
import json
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
        logger.error(f"Unable to retrieve parameter: {str(e)}")
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
        logger.error(f"Unable to retrieve secret: {str(e)}")
        raise e
    else:
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)