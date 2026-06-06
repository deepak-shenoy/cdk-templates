//
// Deepak Shenoy
// API Gateway, Lambda and S3 setup
// June 5th, 2026
//
//

import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';

// At the time of writing, the documentation was found here:
// https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3-readme.html
import * as s3 from 'aws-cdk-lib/aws-s3'

export class ApiLambdaS3TsStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here

    const bucketSourceS3 = new s3.Bucket(this, "s3BucketLogicalId", {
      bucketName: 's3BucketDemo',
    })

    // example resource
    // const queue = new sqs.Queue(this, 'ApiLambdaS3TsQueue', {
    //   visibilityTimeout: cdk.Duration.seconds(300)
    // });
  }
}
