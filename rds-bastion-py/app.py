#!/usr/bin/env python3
#
# Build an RDS Database that allows access through Session Manager
# Deepak Shenoy
# May 3rd, 2026
#
import os

import aws_cdk as cdk

from rds_ssm_py.rds_ssm_py_stack import RdsSSMPyStack


app = cdk.App()
RdsSSMPyStack(app, "RdsSSMPyStack")

app.synth()
