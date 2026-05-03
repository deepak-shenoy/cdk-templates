# API with API Gateway CDK Template (Python)
## Overview
Create API with API Gateway.  Using the CDK framework with Python

## Accessing the API 
You will need to run the following to get the `x-api-key` that will need to go
into the HTTP header:

``get-api-key   --api-key <api_key>   --include-value   --query "value"   --output text``

Where `<api_key>`is output after running the CDK

## Setup
### Python

To manually setup the environment on UNIX/Linux based systems:

```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

To synthesize the CloudFormation template:

```
$ cdk synth
