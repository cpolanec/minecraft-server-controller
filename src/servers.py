"""Handlers for API operations at /server level."""

import json
import logging
import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_operation(event, context):  # pylint: disable=unused-argument
    """Get list of Minecraft game servers.

    Parameters
    ----------
    event: dict, required
        API Event Input Format
        https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html

    context: object, required
        Lambda Context runtime methods and attributes
        https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    -------
    API Gateway Lambda Proxy Output Format: dict
    https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    # gather data for HTTP response
    servers = gather_server_data()

    # return the HTTP payload
    return {
        'statusCode': 200,
        'body': json.dumps({
            'servers': servers
        })
    }


def gather_server_data():
    """Gather and format Minecraft server data from AWS EC2 instances."""
    # gather instance details from AWS
    reservations = gather_ec2_information()
    servers = process_instance_data(reservations)
    return servers


def gather_ec2_information():
    """Gather raw EC2 instance data."""
    # gather instance details from AWs
    ec2_client = boto3.client("ec2")
    reservations = ec2_client.describe_instances(
        Filters=[
            {'Name': 'tag:Application', 'Values': ['minecraft']}
        ]
    )
    return reservations


def process_instance_data(reservations):
    """Process raw EC2 instance data."""
    # consolidate the game server data
    servers = []
    for reservation in reservations.get('Reservations', []):
        logger.debug('reservation = %s', reservation)
        servers.extend(
            map(map_instance, reservation.get('Instances', []))
        )
    return servers


def map_instance(instance):
    """Map AWS EC2 instance data to response message format."""
    tags = instance.get('Tags', [])
    full_name = get_server_name(tags)
    return {
        'Name': full_name.split('-')[-1],
        'FullName': full_name,
        'Environment': get_environment(tags),
        'InstanceId': instance.get('InstanceId', ''),
        'State': instance.get('State', {}).get('Name', '')
    }


def get_server_name(tags):
    """Retrieve server name from AWS EC2 tags."""
    names = list(filter(lambda d: d.get('Key') == 'Name', tags))
    return names[0].get('Value', '') if len(names) > 0 else ''


def get_environment(tags):
    """Retrieve environment from AWS EC2 tags."""
    names = list(filter(lambda d: d.get('Key') == 'Environment', tags))
    return names[0].get('Value', '') if len(names) > 0 else ''
