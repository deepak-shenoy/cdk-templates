
# Website CDK Template (Python)
## Overview
Create a static website using the AWS S3 bucket service for static website hosting.

The `cdk.json` file tells the CDK Toolkit how to execute your app.


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
```