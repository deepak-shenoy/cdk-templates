#
# Build an RDS Database with access through AWS SSM
#
# Main Stack Code
#
# Deepak Shenoy
# May 3rd, 2026
#
from pydoc import describe

from aws_cdk import (
    Duration,
    Stack,
    RemovalPolicy,
    CfnOutput,
    SecretValue,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_iam as iam,
    aws_secretsmanager as secretsmanager,
    aws_ssm as ssm
)
from constructs import Construct

class RdsSSMPyStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #------------------------------------------------------------------------------------------------
        # Build a VPC with two public and two private subnets that are across
        # two availability zones.  No NAT Gateway to save costs.
        vpc = ec2.Vpc(self, "RDSVpc",
                      max_azs=2,
                      nat_gateways=0,
                      subnet_configuration=[
                          ec2.SubnetConfiguration(
                              name="Public",
                              subnet_type=ec2.SubnetType.PUBLIC,
                              cidr_mask=24
                          ),
                          ec2.SubnetConfiguration(
                              name="Private",
                              subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                              cidr_mask=24
                          )
                      ])
        #------------------------------------------------------------------------------------------------
        # VPC Endpoints - Needed for SSM without NAT
        vpc.add_interface_endpoint("SSMEndpoint",
                                   service=ec2.InterfaceVpcEndpointAwsService.SSM)
        vpc.add_interface_endpoint("SSMMessagesEndpoint",
                                   service=ec2.InterfaceVpcEndpointAwsService.SSM_MESSAGES)
        vpc.add_interface_endpoint("E2MessagesEndpoint",
                                   service=ec2.InterfaceVpcEndpointAwsService.EC2_MESSAGES)
        vpc.add_interface_endpoint("SecretsManagerEndpoint",
                                   service=ec2.InterfaceVpcEndpointAwsService.SECRETS_MANAGER)

        #------------------------------------------------------------------------------------------------
        # Security Groups

        # Database Tools SG - No inbound needed as SSM handles it
        db_tools_sg = ec2.SecurityGroup(self, "DbToolsSG",
              vpc=vpc,
              description="Database tools host security group - SSM only",
              allow_all_outbound=True)

        # RDS SG - only allow traffic from bastion
        rds_sg = ec2.SecurityGroup(self, "RDSSg",
               vpc=vpc,
               description="RDS security group",
               allow_all_outbound=False)

        # Ingress
        rds_sg.add_ingress_rule(
                peer=db_tools_sg,
                connection=ec2.Port.tcp(5432),
                description="Allow PostgreSQL from database tools only"
        )

        #------------------------------------------------------------------------------------------------
        # IAM Role for Database Tools (SSM and Secrets Manager Access)
        db_tools_role = iam.Role(self, "DbToolsRole",
                assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
                managed_policies=[
                    # Required for SSM session manager
                    iam.ManagedPolicy.from_aws_managed_policy_name(
                        "AmazonSSMManagedInstanceCore"
                    ),
                    iam.ManagedPolicy.from_aws_managed_policy_name(
                        "SecretsManagerReadWrite"
                    )
                ])

        #------------------------------------------------------------------------------------------------
        # Database Tools EC2 instance (this is in the public subnet so no key pair needed)
        db_tools = ec2.Instance(self, "DbToolsHost",
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.T3, ec2.InstanceSize.MICRO
            ),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC
            ),
            security_group=db_tools_sg,
            role=db_tools_role
            # No key pair - access via SSM only
        )

        #------------------------------------------------------------------------------------------------
        # Install PostgreSQL client and seed script on instance launch
        db_tools.add_user_data(
            "yum update -y",
            "amazon-linux-extras enable postgresql14",
            "yum install -y postgresql",
            "yum install -y jq"
        )

        #------------------------------------------------------------------------------------------------
        # RSS Database Credentials (secrets manager)
        db_secret = secretsmanager.Secret(self,"RDSSecret",
            secret_name="rds-bastion/db-credentials",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template='{"username": "dbadmin"}',
                generate_string_key="password",
                exclude_punctuation=True,
                include_space=False,
                password_length=16
            )
        )

        #------------------------------------------------------------------------------------------------
        # RDS Subnet group (private subnets only)
        rds_subnet_group = rds.SubnetGroup(self, "RDSSubnetGroup",
            description="RDS subnet group - private subnets",
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
            removal_policy=RemovalPolicy.DESTROY
        )

        #------------------------------------------------------------------------------------------------
        # PostgreSQL instance
        db_instance = rds.DatabaseInstance(self, "RdsInstance",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_14
            ),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.T3, ec2.InstanceSize.MICRO
            ),
            vpc=vpc,
            subnet_group=rds_subnet_group,
            security_groups=[rds_sg],
            credentials=rds.Credentials.from_secret(db_secret),
            database_name="appdb",
            allocated_storage=20,
            max_allocated_storage=100,
            backup_retention=Duration.days(7),
            deletion_protection=False,
            removal_policy=RemovalPolicy.DESTROY,
            publicly_accessible=False,
            multi_az=False
        )

        #------------------------------------------------------------------------------------------------
        # Seed database
        seed_sql = ssm.StringParameter(self, "SeedSql",
                                   parameter_name="/rds-bastion/seed-sql",
                                   string_value="""CREATE TABLE IF NOT EXISTS customers (id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL, email VARCHAR(150) UNIQUE NOT NULL, phone VARCHAR(20), created_at TIMESTAMP DEFAULT NOW());
CREATE TABLE IF NOT EXISTS products (id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL, description TEXT, price NUMERIC(10,2) NOT NULL, stock INT DEFAULT 0, created_at TIMESTAMP DEFAULT NOW());
CREATE TABLE IF NOT EXISTS orders (id SERIAL PRIMARY KEY, customer_id INT REFERENCES customers(id), product_id INT REFERENCES products(id), quantity INT NOT NULL, total NUMERIC(10,2) NOT NULL, status VARCHAR(20) DEFAULT 'pending', created_at TIMESTAMP DEFAULT NOW());
INSERT INTO customers (name, email, phone) VALUES ('Alice Johnson', 'alice@example.com', '555-0101'), ('Bob Smith', 'bob@example.com', '555-0102') ON CONFLICT (email) DO NOTHING;
INSERT INTO products (name, description, price, stock) VALUES ('Laptop Pro', '15-inch laptop', 1299.99, 50), ('Wireless Mouse', 'Ergonomic mouse', 29.99, 200) ON CONFLICT DO NOTHING;""",
                                   )

        # Grant database tools read access to seed SQL parameter
        seed_sql.grant_read(db_tools_role)

        #------------------------------------------------------------------------------------------------
        # Run seed SQL on first boot via user data
        # db_tools.add_user_data(
        #     # Retrieve DB credentials from Secrets Manager
        #     f'SECRET=$(aws secretsmanager get-secret-value --secret-id {db_secret.secret_arn} --region {self.region} --query SecretString --output text)',
        #     'DB_USER=$(echo $SECRET | jq -r .username)',
        #     'DB_PASS=$(echo $SECRET | jq -r .password)',
        #     # Retrieve seed SQL from SSM Parameter Store
        #     f'SEED_SQL=$(aws ssm get-parameter --name /rds-bastion/seed-sql --region {self.region} --query Parameter.Value --output text)',
        #     # Run seed SQL against RDS
        #     f'PGPASSWORD=$DB_PASS psql -h {db_instance.db_instance_endpoint_address} -U $DB_USER -d appdb -c "$SEED_SQL"'
        # )

        #------------------------------------------------------------------------------------------------
        # Outputs
        CfnOutput(self, "DbToolsInstanceId",
              value=db_tools.instance_id,
              description="Database Tools EC2 Instance ID — use this for SSM port forwarding",
              )

        CfnOutput(self, "RdsEndpoint",
              value=db_instance.db_instance_endpoint_address,
              description="RDS endpoint address",
              )

        CfnOutput(self, "RdsPort",
              value=db_instance.db_instance_endpoint_port,
              description="RDS port",
              )

        CfnOutput(self, "DbSecretArn",
              value=db_secret.secret_arn,
              description="Secrets Manager ARN for DB credentials",
              )

        CfnOutput(self, "DatabaseName",
              value="appdb",
              description="Database name",
              )


