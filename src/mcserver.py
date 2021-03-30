"""Handlers for API operations at /server level."""

import json
import logging
import boto3
import ec2mapper
import myutils

logger = myutils.get_logger(__name__, logging.INFO)


@myutils.log_calls(level=logging.DEBUG)
def get_handler(event, context):  # pylint: disable=unused-argument
    """REST API GET method to get data about a Minecraft game server.

    Parameters
    ----------
    event: dict, required
        API Event Input Format

    context: object, required
        Lambda Context runtime methods and attributes

    Returns
    -------
    API Gateway Lambda Output Format: dict
    """
    # gather the server data
    name = event.get('pathParameters', {}).get('name')
    server = gather(name)

    # return the HTTP payload
    return {
        'statusCode': 200,
        'body': json.dumps(server)
    }


@myutils.log_calls(level=logging.DEBUG)
def post_handler(event, context):  # pylint: disable=unused-argument
    """REST API POST method to change a Minecraft game server.

    Parameters
    ----------
    event: dict, required
        API Event Input Format

    context: object, required
        Lambda Context runtime methods and attributes

    Returns
    -------
    API Gateway Lambda Output Format: dict
    """
    # gather the server data
    name = event.get('pathParameters', {}).get('name')
    server = gather(name)

    # review/change state of the server
    body = json.loads(event.get('body'))
    change_server_state(server, body.get('state'))

    # gather latest server data for HTTP response
    server = gather(name)

    # return the HTTP payload
    return {
        'statusCode': 200,
        'body': json.dumps(server)
    }


@myutils.log_calls
def gather(name):
    """Return a Minecraft game server data (by server short name)."""
    # format tag names from short name
    main_name = 'minecraft-main-server-{}'.format(name)
    test_name = 'minecraft-test-server-{}'.format(name)

    # gather instance details from AWS
    ec2_client = boto3.client('ec2')
    reservations = ec2_client.describe_instances(
        Filters=[
            {'Name': 'tag:Application', 'Values': ['minecraft']},
            {'Name': 'tag:Name', 'Values': [main_name, test_name]},
            {'Name': 'instance-state-name',
                'Values': [
                    'pending', 'running',
                    'shutting-down', 'stopping', 'stopped'
                ]
             }
        ]
    )

    server = process_ec2_data(reservations)
    return server


@myutils.log_calls(level=logging.DEBUG)
def process_ec2_data(reservations):
    """Gather and format Minecraft server data from AWS EC2 instances."""
    # map reservations to consolidated data model
    servers = ec2mapper.parse(reservations)

    # reduce list of server data
    server = {}
    if len(servers) > 0:
        server = servers[0]
    if len(servers) > 1:
        logger.warning(
            'expected 1 EC2 instance but found %d matches', len(servers))

    return server


@myutils.log_calls
def change_server_state(server, state):
    """Review state of the server."""
    ec2_client = boto3.client('ec2')
    server_name = server.get('name')
    instance_id = server.get('instanceId')

    new_state = None
    if state == 'running':
        resp = ec2_client.start_instances(InstanceIds=[instance_id])
        new_state = resp['StartingInstances'][0]['CurrentState']['Name']
    elif state == 'stopped':
        resp = ec2_client.stop_instances(InstanceIds=[instance_id])
        new_state = resp['StoppingInstances'][0]['CurrentState']['Name']
    elif state == 'rebooting':
        resp = ec2_client.reboot_instances(InstanceIds=[instance_id])
        new_state = 'pending'
    else:
        logger.warning('%s: invalid state = %s', server_name, state)

    return new_state
