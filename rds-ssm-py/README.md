
# RDS Database with AWS Systems Manager Session Manager
This solution uses the AWS Systems Manager
Session Manager (that does not need to have inbound traffic
ports) to connect to a database server in the AWS cloud.

A session is a connection to a node that uses a bi-directional channel between
the client and the AWS cloud.  Traffic is encrypted and signed.  The Session Manager plug-in
to the existing AWS CLI needs to be installed.

To start the process you need to run the following command:

`aws ssm start-session`

This opens up an encrypted websocket connection to the AWS Systems Manager (SSM) service
over port 443.  Since this is normal outbound internet traffic, no firewalls rules are generally
needed

The server (bastion) that is running doesn't have any inbound port or SSH
keys; it also sits on a public subnet.  The SSM Agent running on this node maintains a persistent outbound connection to the SSM
service.  When a session starts, SSM routes traffic through this connection.  The traffic is then passed
to the database server that sits on a private subnet network.

![Slide1.jpeg](artifacts/docs/Overview/Slide1.jpeg)

### Security Benefits

- No open inbound ports
- No SSH keys needed
- RDS is completely unreachable from the internet
- All traffic is encrypted in transit
- IAM controls who can connect
- Credentials are stored in Secrets Manager

### How To Connect

```text
aws secretsmanager get-secret-value \
  --secret-id arn:aws:secretsmanager:{your secrets ARN} \
  --region us-east-1 \
  --query SecretString \
  --output text | python3 -c "import sys,json; print(json.load(sys.stdin)['password'])"
```

Then
```text
aws ssm start-session \
  --target {instance_name} \
  --document-name AWS-StartPortForwardingSessionToRemoteHost \
  --parameters host="{full host name}",portNumber="5432",localPortNumber="5432" \
  --region us-east-1
```
Then open your database client to connect to `127.0.0.1:5432`
