"""Handlers for API operations at /server level."""

import json
import logging
import boto3
import ec2mapper

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_handler(event, context):  # pylint: disable=unused-argument
    """REST API GET method to list Minecraft game servers.

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
    logger.debug('event = %s', event)

    # gather data for HTTP response
    servers = gather()

    # return the HTTP payload
    return {
        'statusCode': 200,
        'body': json.dumps({
            'servers': servers
        })
    }


def gather():
    """Return a list of Minecraft game servers."""
    ec2_client = boto3.client("ec2")
    reservations = ec2_client.describe_instances(
        Filters=[
            {'Name': 'tag:Application', 'Values': ['minecraft']}
        ]
    )
    servers = ec2mapper.parse(reservations)
    return servers
