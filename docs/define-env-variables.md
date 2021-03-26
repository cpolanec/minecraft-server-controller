# Define environment variables

Environment variables need to be defined in an `.env` file at the root level of the project. There are three set of variables that need to be defined (which are specified in the sections below):

- [CloudFormation deployment parameters](#cloudformation-deployment-parameters)
- [AWS service role specifications](#aws-service-role-specifications)
- [REST API parameters](#rest-api-parameters)

## CloudFormation deployment parameters

The following variables are needed to define the CloudFormation stack and deploy the resources:

| Variable                  | Description                                               |
| ------------------------- | --------------------------------------------------------- |
| `STACK_NAME`              | Name to give the CloudFormation stack                     |
| `ENVIRONMENT`             | Name to separate any development and production stacks    |
| `S3_DEPLOYMENT_BUCKET`    | Bucket to deploy AWS SAM build artifacts                  |
| `CLOUDFORMATION_ROLE_ARN` | IAM role with permissions to deploy CloudFormation stacks |

## AWS service role specifications

The following variables specify the IAM roles that will be assumed by the application's AWS services:

| Variable                | Description                                               |
| ----------------------- | --------------------------------------------------------- |
| `EVENTBRIDGE_ROLE_ARN`  | IAM role to allow EventBridge to execute State Machines   |
| `FUNCTION_ROLE_ARN`     | IAM role to allow Lambda functions to execute (see above) |
| `STATEMACHINE_ROLE_ARN` | IAM role to allow State Machines to invoke functions      |

## REST API parameters

The following variables are needed to configure the API Gateway and Route53 hosted zone:

| Variable          | Description                                    |
| ----------------- | ---------------------------------------------- |
| `HOSTED_ZONE_ID`  | Hosted Zone ID of Route53 domain               |
| `CERTIFICATE_ARN` | Certificate associated with the Route53 domain |
| `API_DOMAIN_NAME` | Name of the Route53 domain                     |
| `API_KEY`         | API key created in the API usage plan          |

## Example `.env` file

```properties
# sample .env file

STACK_NAME=minecraft-controller
ENVIRONMENT=test
S3_DEPLOYMENT_BUCKET=my-deployments
CLOUDFORMATION_ROLE_ARN=arn:aws:iam::123456789123:role/cloudformation-role

EVENTBRIDGE_ROLE_ARN=arn:aws:iam::123456789123:role/eventbridge-role
FUNCTION_ROLE_ARN=arn:aws:iam::123456789123:role/function-role
STATEMACHINE_ROLE_ARN=arn:aws:iam::123456789123:role/statemachine-role

HOSTED_ZONE_ID=ABC123DEF456GHI789JKL
CERTIFICATE_ARN=arn:aws:acm:us-east-1:123456789123:certificate/abcdefgh-1234-ijkl-5678-mnopqrstuvwx
API_DOMAIN_NAME=api-test.mydomain.net
API_KEY=abcABC123defDEF456ghiGHI789jklJKLmnoMNOP
```
