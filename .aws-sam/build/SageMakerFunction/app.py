import json, boto3, os

sagemaker_runtime = boto3.client("sagemaker-runtime")  # Connects to SageMaker endpoint runtime

ENDPOINT_NAME = os.environ.get("SAGEMAKER_ENDPOINT")   # Reads the deployed model name from Lambda env

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])              # Parses incoming request
        input_text = body.get("input", "Hello!")      # Gets user input (defaults to "Hello!")

        response = sagemaker_runtime.invoke_endpoint( # Calls SageMaker with input
            EndpointName=ENDPOINT_NAME,
            ContentType="application/json",
            Body=json.dumps({"inputs": input_text})
        )

        result = json.loads(response["Body"].read().decode())  # Gets response from model
        return {
            "statusCode": 200,
            "body": json.dumps({"response": result})   # Sends back response
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})     # Error handling
        }
