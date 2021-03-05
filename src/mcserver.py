"""Handlers for API operations at /server level."""

import json
import logging
import boto3
import ec2mapper

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
    # retrieve short name for server from path parameters
    name = event.get('pathParameters', {}).get('name')
    logger.debug('name = %s', name)

    # gather the server data
    server = gather(name)

    # return the HTTP payload
    return {
        'statusCode': 200,
        'body': json.dumps(server)
    }


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
    # retrieve short name for server from path parameters
    name = event.get('pathParameters', {}).get('name')
    logger.debug('name = %s', name)

    # retrieve POST body with proposed server changes
    body = json.loads(event.get('body'))
    logger.debug('body = %s', body)

    # review/change state of the server
    server = gather(name)
    change_server_state(server, body.get('state'))

    # gather latest server data for HTTP response
    server = gather(name)

    # return the HTTP payload
    return {
        'statusCode': 200,
        'body': json.dumps(server)
    }


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
            {'Name': 'tag:Name', 'Values': [main_name, test_name]}
        ]
    )

    server = process_ec2_data(reservations)
    return server


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


def change_server_state(server, state):
    """Review state of the server."""
    ec2_client = boto3.client('ec2')
    server_name = server.get('name')
    instance_id = server.get('instanceId')

    new_state = None
    if state == 'running':
        logger.info('%s: change state to "running"', server_name)
        resp = ec2_client.start_instances(InstanceIds=[instance_id])
        new_state = resp['StartingInstances'][0]['CurrentState']['Name']
    elif state == 'stopped':
        logger.info('%s: change state to "stopped"', server_name)
        resp = ec2_client.stop_instances(InstanceIds=[instance_id])
        new_state = resp['StoppingInstances'][0]['CurrentState']['Name']
    elif state == 'rebooting':
        logger.info('%s: change state to "rebooting"', server_name)
        resp = ec2_client.reboot_instances(InstanceIds=[instance_id])
        new_state = 'pending'
    else:
        logger.warning('%s: invalid state = %s', server_name, state)

    return new_state
