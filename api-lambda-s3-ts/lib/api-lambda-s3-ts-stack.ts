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

import * as iam from 'aws-cdk-lib/aws-iam'

export class ApiLambdaS3TsStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);


    // Bucket creation
    const bucketSourceS3 = new s3.Bucket(this, "s3BucketLogicalId", {
      // This needs to be globally unique
      bucketName: 's3bucketdemo-abcd',
    })

    // IAM Role
    const iamRole = new iam.Role(this, "iamDemoRole", {
      assumedBy: new iam.ServicePrincipal("lambda.amazonaws.com"),
      description: 'Demo role for the lambda function that will acess the S3 bucket',
      roleName: 'demolambdarole'
    })

    iamRole.addManagedPolicy(iam.ManagedPolicy.fromAwsManagedPolicyName("AmazonS3FullAccess"));

  }
}
