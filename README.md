# LLM-SERVERLESS-API

# SageMaker LLM API

A serverless API deployment for inference with `google/flan-t5-small`, a lightweight instruction-tuned language model from Hugging Face, using AWS SageMaker and API Gateway.

## Project Overview

This project creates an API endpoint that allows users to send text inputs to a hosted `google/flan-t5-small` language model and receive generated responses. The architecture uses:

- **AWS SageMaker**: For deploying and hosting the Hugging Face LLM model
- **AWS Lambda**: To handle API requests and communicate with the SageMaker endpoint
- **API Gateway**: To expose the Lambda function as a RESTful API endpoint
- **AWS SAM**: For infrastructure as code deployment

## Architecture

+---------------+         +------------------+         +----------------------+         +--------------------------+
|  Client (curl |  --->   |  API Gateway     |  --->   | AWS Lambda Function |  --->   |  SageMaker Inference     |
|  or Postman)  |         |  (REST API)      |         | (Python handler)     |         | Endpoint with FLAN-T5    |
+---------------+         +------------------+         +----------------------+         +--------------------------+


## Components

### 1. SageMaker Model Deployment

The project deploys the `google/flan-t5-small` model from Hugging Face using SageMaker's Hugging Face container:

- Uses `ml.g4dn.xlarge` instance type for cost-effective GPU inference
- Configures the model with appropriate environment variables (`HF_MODEL_ID`)
- Handles container health checks with a 300s timeout

### 2. Lambda Function

A Python Lambda function that:
- Processes incoming API requests
- Extracts the input text from the request body
- Calls the SageMaker endpoint for inference
- Returns the model's response with appropriate HTTP status codes
- Includes error handling for robustness

### 3. AWS SAM Template

The infrastructure is defined using an AWS SAM template that:
- Creates the Lambda function with necessary permissions
- Sets up the API Gateway integration
- Configures logging and tracing
- Sets environment variables for the SageMaker endpoint name
- Defines the output values for reference

## Setup and Deployment

### Prerequisites

- AWS CLI configured with appropriate permissions
- AWS SAM CLI installed
- Python 3.12

### Deployment Steps

1. Clone this repository
2. Deploy the SageMaker model:
   ```bash
   python deploy_model.py
sam build
sam deploy --guided


curl -X POST \
  https://{api-id}.execute-api.{region}.amazonaws.com/Prod/predict/ \
  -H 'Content-Type: application/json' \
  -d '{"input": "Summarize: The Amazon rainforest is the largest tropical forest in the world."}'


{
  "response": ["The Amazon rainforest is the world's largest tropical forest."]
}
IAM Permissions
The Lambda function requires permissions to invoke the SageMaker endpoint. These permissions are defined in the SAM template.

Environment Variables
SAGEMAKER_ENDPOINT: The name of the deployed SageMaker endpoint
Monitoring and Maintenance
Logging is configured in JSON format
AWS X-Ray tracing is enabled for both Lambda and API Gateway
CloudWatch Logs can be used to monitor the application
