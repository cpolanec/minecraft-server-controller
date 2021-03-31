"""Handlers for API operations /servers/{server}/users level."""

import json
import logging
import boto3
import parse
import mcrcon
import mcserver
import myutils

logger = myutils.get_logger(__name__, logging.INFO)


@myutils.log_calls(level=logging.DEBUG)
def get_handler(event, context):  # pylint: disable=unused-argument
    """REST API GET method to list users on a Minecraft game server.

    Parameters
    ----------
    event: dict, required
        CloudWatch Event Input Format

    context: object, required
        Lambda Context runtime methods and attributes

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict
    """
    # gather the HTTP payload
    name = event.get('pathParameters', {}).get('name')
    users = gather(name)

    # return the HTTP payload
    return {
        'statusCode': 200,
        'body': json.dumps(users)
    }


@myutils.log_calls
def gather(name):
    """Return data about the users on a Minecraft game server."""
    users = {}

    # get IP address of the game server for login
    server = mcserver.gather(name)
    address = server.get('publicIpAddress')
    if address is None or address == '':
        logger.error('could not find public IP address for %s', name)
        return users

    # get mcrcon from parameter store
    ssm = boto3.client('ssm')
    mcrcon_pw_param = ssm.get_parameter(
        Name='/minecraft/mcrcon/password',
        WithDecryption=True
    )
    mcrcon_pw = mcrcon_pw_param.get('Parameter').get('Value')

    # get users from the game server
    with mcrcon.MCRcon(address, mcrcon_pw) as mcr:
        resp = mcr.command('list')
        logger.debug('mcrcon "list" command returned = "%s"', resp)
    users = parse_mcrcon_list(resp)

    return users


@myutils.log_calls(level=logging.DEBUG)
def parse_mcrcon_list(response):
    """Parse the mcrcon 'list' command response."""
    # set default values
    count = 0
    names = []

    # retrieve data from string
    split_response = response.split(':')
    if len(split_response) == 2:
        results = parse.parse(
            'There are {:d} of a max of {:d} players online',
            split_response[0])
        count = results[0]
        csv = split_response[1].replace(' ', '')
        names = [] if csv == '' else csv.split(',')

    # return result
    return {
        'count': count,
        'names': names
    }
