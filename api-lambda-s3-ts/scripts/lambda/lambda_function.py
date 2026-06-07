#
# Demo Lambda Function
# Deepak Shenoy
# June 6th, 20206
#
#
import json
import boto3

s3_client = boto3.client('s3')

# ---------------------------------------------------------------------
# Lambda Function
# ---------------------------------------------------------------------
def lambda_handler(event, context):
    #
    # To-do - Get the contents from the S3 bucket
    #
    response = json.loads('{"message": "Test Data"}')
    # response = s3_client.get_object(
    #     Bucket = 's3bucketdemo-abcd',
    #     Key = 'SampleFile.json'
    # )

    data_body = response['message']

    # To do
    # Test output - use the contents from the S3 bucket
    return {
        'statusCode': 200,
        'body': json.dumps(data_body)
    }