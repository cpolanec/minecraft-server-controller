# Prepare the AWS account

Follow these steps to complete the one-time setup of your [AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/):

1. **Configure IAM roles and policies.** Deploying and running the application will require the following IAM resources:

   - Role to permit CloudFormation to create the resources defined in the AWS SAM template
   - Role to permit Lambda functions to modify EC2 instance state, write to CloudWatch log streams, and get SSM parameters
   - Role to permit Step Functions to invoke Lambda functions
   - Role to permit CloudWatch events to execute Step Function state machines

1. **Create IAM user for deployments.** Deploying the application will require the user to have the following permissions:

   - Creating, modifying, and deleting CloudFormation stacks
   - Writing objects to a S3 bucket (e.g. AWS SAM deployment artifacts)
   - Passing the CloudFormation role (defined in step #1) to the CloudFormation service
   - Describing and executing State Machines (during end-to-end testing)

1. **Create SSM parameter for `mcrcon` connection.** The password used to communicate between the `mcrcon` client and Minecraft servers needs to be added to the Parameter Store.

   - _Note: Secrets Manager would also be a good location for this parameter but a SecureString parameter is a more economical location for this use case._

1. **Create Route53 Hosted zone.** A Route53 Hosted zone is needed to provide a pretty URL for the REST API created by this application.

1. **Create certificate in Certificate Manager.** The API Gateway configuration is expecting a digital certificate to secure the REST API endpoint.
