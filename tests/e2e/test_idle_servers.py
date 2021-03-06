"""Integration testing for "idle servers" state machine."""
import os
import boto3


def test_idle_server_statemachine():
    """Test "idle servers" state machine."""
    # gather CloudFormation stacks
    cf_client = boto3.client('cloudformation')
    stack_name = 'minecraft-{}-controller'.format(os.getenv('ENVIRONMENT'))
    stacks = cf_client.describe_stacks(StackName=stack_name)

    # gather ARN for StopIdleServersWorkflow
    state_machine_arn = None
    stack_outputs = stacks['Stacks'][0]['Outputs']
    for output in stack_outputs:
        if output['OutputKey'] == 'StopIdleServersWorkflowARN':
            state_machine_arn = output['OutputValue']

    # invoke the StopIdleServersWorkflow
    sfn_client = boto3.client('stepfunctions')
    response = sfn_client.start_execution(
        stateMachineArn=state_machine_arn
    )
    execution_arn = response['executionArn']

    # wait for execution to complete
    status = 'RUNNING'
    while status == 'RUNNING':
        response = sfn_client.describe_execution(
            executionArn=execution_arn
        )
        status = response['status']

    assert status == 'SUCCEEDED'
