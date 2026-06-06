"use strict";
//
// Deepak Shenoy
// API Gateway, Lambda and S3 setup
// June 5th, 2026
//
//
Object.defineProperty(exports, "__esModule", { value: true });
exports.ApiLambdaS3TsStack = void 0;
const cdk = require("aws-cdk-lib");
// At the time of writing, the documentation was found here:
// https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3-readme.html
const s3 = require("aws-cdk-lib/aws-s3");
class ApiLambdaS3TsStack extends cdk.Stack {
    constructor(scope, id, props) {
        super(scope, id, props);
        // The code that defines your stack goes here
        const bucketSourceS3 = new s3.Bucket(this, "s3BucketLogicalId", {
            bucketName: 's3BucketDemo',
        });
        // example resource
        // const queue = new sqs.Queue(this, 'ApiLambdaS3TsQueue', {
        //   visibilityTimeout: cdk.Duration.seconds(300)
        // });
    }
}
exports.ApiLambdaS3TsStack = ApiLambdaS3TsStack;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiYXBpLWxhbWJkYS1zMy10cy1zdGFjay5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzIjpbImFwaS1sYW1iZGEtczMtdHMtc3RhY2sudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IjtBQUFBLEVBQUU7QUFDRixnQkFBZ0I7QUFDaEIsbUNBQW1DO0FBQ25DLGlCQUFpQjtBQUNqQixFQUFFO0FBQ0YsRUFBRTs7O0FBRUYsbUNBQW1DO0FBR25DLDREQUE0RDtBQUM1RCw2RUFBNkU7QUFDN0UseUNBQXdDO0FBRXhDLE1BQWEsa0JBQW1CLFNBQVEsR0FBRyxDQUFDLEtBQUs7SUFDL0MsWUFBWSxLQUFnQixFQUFFLEVBQVUsRUFBRSxLQUFzQjtRQUM5RCxLQUFLLENBQUMsS0FBSyxFQUFFLEVBQUUsRUFBRSxLQUFLLENBQUMsQ0FBQztRQUV4Qiw2Q0FBNkM7UUFFN0MsTUFBTSxjQUFjLEdBQUcsSUFBSSxFQUFFLENBQUMsTUFBTSxDQUFDLElBQUksRUFBRSxtQkFBbUIsRUFBRTtZQUM5RCxVQUFVLEVBQUUsY0FBYztTQUMzQixDQUFDLENBQUE7UUFFRixtQkFBbUI7UUFDbkIsNERBQTREO1FBQzVELGlEQUFpRDtRQUNqRCxNQUFNO0lBQ1IsQ0FBQztDQUNGO0FBZkQsZ0RBZUMiLCJzb3VyY2VzQ29udGVudCI6WyIvL1xuLy8gRGVlcGFrIFNoZW5veVxuLy8gQVBJIEdhdGV3YXksIExhbWJkYSBhbmQgUzMgc2V0dXBcbi8vIEp1bmUgNXRoLCAyMDI2XG4vL1xuLy9cblxuaW1wb3J0ICogYXMgY2RrIGZyb20gJ2F3cy1jZGstbGliJztcbmltcG9ydCB7IENvbnN0cnVjdCB9IGZyb20gJ2NvbnN0cnVjdHMnO1xuXG4vLyBBdCB0aGUgdGltZSBvZiB3cml0aW5nLCB0aGUgZG9jdW1lbnRhdGlvbiB3YXMgZm91bmQgaGVyZTpcbi8vIGh0dHBzOi8vZG9jcy5hd3MuYW1hem9uLmNvbS9jZGsvYXBpL3YyL2RvY3MvYXdzLWNkay1saWIuYXdzX3MzLXJlYWRtZS5odG1sXG5pbXBvcnQgKiBhcyBzMyBmcm9tICdhd3MtY2RrLWxpYi9hd3MtczMnXG5cbmV4cG9ydCBjbGFzcyBBcGlMYW1iZGFTM1RzU3RhY2sgZXh0ZW5kcyBjZGsuU3RhY2sge1xuICBjb25zdHJ1Y3RvcihzY29wZTogQ29uc3RydWN0LCBpZDogc3RyaW5nLCBwcm9wcz86IGNkay5TdGFja1Byb3BzKSB7XG4gICAgc3VwZXIoc2NvcGUsIGlkLCBwcm9wcyk7XG5cbiAgICAvLyBUaGUgY29kZSB0aGF0IGRlZmluZXMgeW91ciBzdGFjayBnb2VzIGhlcmVcblxuICAgIGNvbnN0IGJ1Y2tldFNvdXJjZVMzID0gbmV3IHMzLkJ1Y2tldCh0aGlzLCBcInMzQnVja2V0TG9naWNhbElkXCIsIHtcbiAgICAgIGJ1Y2tldE5hbWU6ICdzM0J1Y2tldERlbW8nLFxuICAgIH0pXG5cbiAgICAvLyBleGFtcGxlIHJlc291cmNlXG4gICAgLy8gY29uc3QgcXVldWUgPSBuZXcgc3FzLlF1ZXVlKHRoaXMsICdBcGlMYW1iZGFTM1RzUXVldWUnLCB7XG4gICAgLy8gICB2aXNpYmlsaXR5VGltZW91dDogY2RrLkR1cmF0aW9uLnNlY29uZHMoMzAwKVxuICAgIC8vIH0pO1xuICB9XG59XG4iXX0=