#!/usr/bin/env python3
#
# Build an RDS Database with access through a Bastion Swerver
# Deepak Shenoy
# May 3rd, 2026
#
import os

import aws_cdk as cdk

from rds_bastion_py.rds_bastion_py_stack import RdsBastionPyStack


app = cdk.App()
RdsBastionPyStack(app, "RdsBastionPyStack",
    )

app.synth()
