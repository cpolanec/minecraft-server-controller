"""Handlers for API operations at /server level."""

import json
import logging
import boto3
import ec2mapper
import myutils

logger = myutils.get_logger(__name__, logging.INFO)


@myutils.log_calls(level=logging.DEBUG)
def get_handler(event, context):  # pylint: disable=unused-argument
    """REST API GET method to list Minecraft game servers.

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
    # gather data for HTTP response
    servers = gather()

    # return the HTTP payload
    return {
        'statusCode': 200,
        'body': json.dumps({
            'servers': servers
        })
    }


@myutils.log_calls
def gather():
    """Return a list of Minecraft game servers."""
    # initialize AWS SDK query filters
    filters = []
    filters.append(myutils.get_application_filter())
    filters.append(myutils.get_instance_filter())

    # invoke the AWS SDK to get relevant EC2 instances
    ec2_client = boto3.client('ec2')
    reservations = ec2_client.describe_instances(Filters=filters)

    servers = ec2mapper.parse(reservations)
    return servers
