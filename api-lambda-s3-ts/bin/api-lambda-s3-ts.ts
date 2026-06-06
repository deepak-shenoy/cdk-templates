#!/usr/bin/env node
//
// Deepak Shenoy
// API Gateway, Lambda and S3 setup
// June 5th, 2026
//
//
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { ApiLambdaS3TsStack } from '../lib/api-lambda-s3-ts-stack';

const app = new cdk.App();
new ApiLambdaS3TsStack(app, 'ApiLambdaS3TsStack', {

});