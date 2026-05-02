#!/usr/bin/env python3

#
# Build API using API Gateway
# Deepak Shenoy
# May 2nd, 2026
#

import os

import aws_cdk as cdk

from api_with_api_gateway_py.api_with_api_gateway_py_stack import ApiWithApiGatewayPyStack


app = cdk.App()
ApiWithApiGatewayPyStack(app, "ApiWithApiGatewayPyStack")

app.synth()
