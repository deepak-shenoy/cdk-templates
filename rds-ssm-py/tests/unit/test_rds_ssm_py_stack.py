import aws_cdk as core
import aws_cdk.assertions as assertions

from rds_ssm_py.rds_ssm_py_stack import RdsSSMPyStack

# example tests. To run these tests, uncomment this file along with the example
# resource in rds_bastion_py/rds_ssm_py_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = RdsSSMPyStack(app, "rds-ssm-py")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
