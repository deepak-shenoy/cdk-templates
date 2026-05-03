#
# Build an RDS Database with access through a Bastion Swerver
#
# Main Stack Code
#
# Deepak Shenoy
# May 3rd, 2026
#

from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

class RdsBastionPyStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

