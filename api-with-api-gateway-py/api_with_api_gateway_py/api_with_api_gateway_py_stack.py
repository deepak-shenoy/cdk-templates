from aws_cdk import (
    Duration,
    Stack,
    RemovalPolicy,
    CfnOutput,
    aws_apigateway as apigw,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_iam as iam,
    aws_logs as logs
)
from constructs import Construct

class ApiWithApiGatewayPyStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #------------------------------------------------------------------------------------------------
        # Build a lambda function for the backend
        lambda_function = _lambda.Function(self, "APIHandler",
                                           runtime=_lambda.Runtime.PYTHON_3_12,
                                           handler="index.handler",
                                           code=_lambda.Code.from_asset("artifacts/scripts"),
                                           timeout=Duration.seconds(30),
                                           memory_size=256,
                                           log_retention=logs.RetentionDays.ONE_WEEK
                                           )

        #------------------------------------------------------------------------------------------------
        # API Gateway Log Group
        log_group = logs.LogGroup(self, "APIGatewayLogs",
                                  retention=logs.RetentionDays.ONE_WEEK,
                                  removal_policy=RemovalPolicy.DESTROY)



        #------------------------------------------------------------------------------------------------
        # Build the API Gateway
        api = apigw.RestApi(self, "RestAPI",
                            rest_api_name="MyApi",
                            description="Template API",
                            default_cors_preflight_options=apigw.CorsOptions(
                                allow_origins=apigw.Cors.ALL_ORIGINS,
                                allow_methods=apigw.Cors.ALL_METHODS,
                                allow_headers=[
                                    "Context-Type",
                                    "Authorization",
                                    "X-Api-Key"
                                ]
                            ),

            # Access Logging
            deploy_options = apigw.StageOptions(
                stage_name = "prod",
                logging_level = apigw.MethodLoggingLevel.INFO,
                data_trace_enabled=True,
                metrics_enabled=True,
                access_log_destination=apigw.LogGroupLogDestination(log_group),
                access_log_format=apigw.AccessLogFormat.json_with_standard_fields(
                    caller=True,
                    http_method=True,
                    ip=True,
                    protocol=True,
                    request_time=True,
                    resource_path=True,
                    response_length=True,
                    status=True,
                    user=True,
                ),
            ),
        )

        #------------------------------------------------------------------------------------------------
        # Build the role for the API to write to CloudWatch
        cloudwatch_role = iam.Role(self, "ApiGatewayCloudWatchRole",
                                   assumed_by=iam.ServicePrincipal("apigateway.amazonaws.com"),
                                   managed_policies=[
                                       iam.ManagedPolicy.from_aws_managed_policy_name(
                                           "service-role/AmazonAPIGatewayPushToCloudWatchLogs"
                                       )
                                   ]
                        )

        #------------------------------------------------------------------------------------------------
        # Assign the role to the API Gateway
        apigw.CfnAccount(self, "ApiGatewayAccount",
                         cloud_watch_role_arn=cloudwatch_role.role_arn
                  )

        # Lambda integration
        lambda_integration = apigw.LambdaIntegration(lambda_function,
                                                     request_templates={"application/json": '{ "statusCode": "200" }'})

        #------------------------------------------------------------------------------------------------
        # API Routes
        # The first resource test is a GET
        resource_01 = api.root.add_resource("test1")
        resource_01.add_method("GET", lambda_integration, api_key_required=True)

        # The second resource is a POST
        resource_02 = api.root.add_resource("test2")
        resource_02.add_method("POST", lambda_integration, api_key_required=True)

        #------------------------------------------------------------------------------------------------
        # API Key and Usage Plan
        api_key = api.add_api_key("ApiKey",
                                  api_key_name="my-api-key",
                                  description="API Key for MyApi")

        usage_plan = api.add_usage_plan("UsagePlan",
                                        name = "StandardPlan",
                                        throttle=apigw.ThrottleSettings(
                                            rate_limit=100,
                                            burst_limit=200,
                                        ),
                                        quota=apigw.QuotaSettings(
                                            limit=10000,   # Requests per day
                                            period=apigw.Period.DAY
                                        ),
                                )

        usage_plan.add_api_key(api_key)
        usage_plan.add_api_stage(
            api=api,
            stage=api.deployment_stage
        )

        #------------------------------------------------------------------------------------------------
        # Output
        CfnOutput(self,
                  "ApiURL",
                  value=api.url,
                  description="API Gateway URL")

        CfnOutput(self, "ApiKeyId",
                  value=api_key.key_id,
                  description="API Key Id - Retrieve value with aws apigateway get-api-key --api-key <id> --include-value")