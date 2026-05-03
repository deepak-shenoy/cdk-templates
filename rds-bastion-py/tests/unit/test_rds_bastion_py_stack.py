import aws_cdk as core
import aws_cdk.assertions as assertions

from rds_bastion_py.rds_bastion_py_stack import RdsBastionPyStack

# example tests. To run these tests, uncomment this file along with the example
# resource in rds_bastion_py/rds_bastion_py_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = RdsBastionPyStack(app, "rds-bastion-py")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
