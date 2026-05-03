
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