#
# Build a simple website
# Deepak Shenoy
# May 1st, 2026
#
import aws_cdk as core
import aws_cdk.assertions as assertions

from website_template_py.website_template_py_stack import WebsiteTemplatePyStack

# example tests. To run these tests, uncomment this file along with the example
# resource in website_template_py/website_template_py_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = WebsiteTemplatePyStack(app, "website-template-py")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
