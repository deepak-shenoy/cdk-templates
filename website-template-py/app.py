#!/usr/bin/env python3
#
# Entry Point for the CDK
# Deepak Shenoy
# May 1st, 2026
#

import os

import aws_cdk as cdk

from website_template_py.website_template_py_stack import WebsiteTemplatePyStack


app = cdk.App()
WebsiteTemplatePyStack(app, "WebsiteTemplatePyStack")
app.synth()
