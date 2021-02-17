"""Handlers for API operations at /server level."""

import json
import logging
import boto3
import ec2mapper

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_handler(event, context):  # pylint: disable=unused-argument
    """Get Minecraft game server data.

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


def gather(name):
    """Return a Minecraft game server data (by server short name)."""
    # format tag names from short name
    main_name = 'minecraft-main-server-{}'.format(name)
    test_name = 'minecraft-test-server-{}'.format(name)

    # gather instance details from AWS
    ec2_client = boto3.client("ec2")
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
