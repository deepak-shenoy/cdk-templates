#
# Build API using API Gateway
# Deepak Shenoy
# May 2nd, 2026
#

import aws_cdk as core
import aws_cdk.assertions as assertions

from api_with_api_gateway_py.api_with_api_gateway_py_stack import ApiWithApiGatewayPyStack

# example tests. To run these tests, uncomment this file along with the example
# resource in api_with_api_gateway_py/api_with_api_gateway_py_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ApiWithApiGatewayPyStack(app, "api-with-api-gateway-py")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
