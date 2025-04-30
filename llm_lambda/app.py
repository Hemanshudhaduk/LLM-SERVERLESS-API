import json, boto3, os

sagemaker_runtime = boto3.client("sagemaker-runtime") 

ENDPOINT_NAME = os.environ.get("SAGEMAKER_ENDPOINT")   

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])             
        input_text = body.get("input", "Hello!")     

        response = sagemaker_runtime.invoke_endpoint( 
            EndpointName=ENDPOINT_NAME,
            ContentType="application/json",
            Body=json.dumps({"inputs": input_text})
        )

        result = json.loads(response["Body"].read().decode()) 
        return {
            "statusCode": 200,
            "body": json.dumps({"response": result})   
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})     
        }
