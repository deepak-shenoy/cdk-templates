#!/usr/bin/env python3
"""
Run this script after CDK deploy to seed the RDS database.
It uses SSM Session Manager to execute SQL on the bastion host.

Usage:
    python3 scripts/seed_database.py --instance-id <BastionInstanceId> --region us-east-1
"""

import boto3
import argparse
import json
import time


def get_stack_outputs(stack_name, region):
    cf = boto3.client("cloudformation", region_name=region)
    response = cf.describe_stacks(StackName=stack_name)
    outputs = response["Stacks"][0]["Outputs"]
    return {o["OutputKey"]: o["OutputValue"] for o in outputs}


def get_db_credentials(secret_arn, region):
    sm = boto3.client("secretsmanager", region_name=region)
    response = sm.get_secret_value(SecretId=secret_arn)
    return json.loads(response["SecretString"])


def run_ssm_command(instance_id, command, region):
    ssm = boto3.client("ssm", region_name=region)
    response = ssm.send_command(
        InstanceIds=[instance_id],
        DocumentName="AWS-RunShellScript",
        Parameters={"commands": [command]},
    )
    command_id = response["Command"]["CommandId"]

    # Wait for command to complete
    time.sleep(5)
    for _ in range(12):
        result = ssm.get_command_invocation(
            CommandId=command_id,
            InstanceId=instance_id,
        )
        if result["Status"] in ("Success", "Failed", "TimedOut"):
            return result
        time.sleep(5)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--instance-id", required=True)
    parser.add_argument("--region", default="us-east-1")
    parser.add_argument("--stack-name", default="RdsBastionStack")
    args = parser.parse_args()

    print("📦 Fetching stack outputs...")
    outputs = get_stack_outputs(args.stack_name, args.region)

    rds_endpoint = outputs["RdsEndpoint"]
    secret_arn   = outputs["DbSecretArn"]

    print("🔑 Fetching DB credentials...")
    creds = get_db_credentials(secret_arn, args.region)

    seed_command = f"""
export PGPASSWORD='{creds["password"]}'
# Get seed SQL from SSM Parameter Store
aws ssm get-parameter --name /rds-bastion/seed-sql --region {args.region} --query Parameter.Value --output text > /tmp/seed.sql
# Run seed SQL
psql -h {rds_endpoint} -U {creds["username"]} -d appdb -f /tmp/seed.sql
echo "Seed complete"
"""

    print(f"🌱 Running seed script on bastion {args.instance_id}...")
    result = run_ssm_command(args.instance_id, seed_command, args.region)

    if result["Status"] == "Success":
        print("✅ Database seeded successfully!")
        print(result["StandardOutputContent"])
    else:
        print("❌ Seed failed:")
        print(result["StandardErrorContent"])


if __name__ == "__main__":
    main()