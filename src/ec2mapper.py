"""Helper methods for parsing EC2 instance data from AWS SDK."""

import logging
import myutils

logger = myutils.get_logger(__name__, logging.INFO)


@myutils.log_calls(level=logging.DEBUG)
def parse(reservations):
    """Process raw EC2 instance data."""
    # consolidate the game server data
    servers = []
    for reservation in reservations.get('Reservations', []):
        servers.extend(
            map(map_instance, reservation.get('Instances', []))
        )
    return servers


@myutils.log_calls(level=logging.DEBUG)
def map_instance(instance):
    """Map AWS EC2 instance data to response message format."""
    tags = instance.get('Tags', [])
    full_name = myutils.get_first('Name', tags)
    return {
        'name': get_short_name(full_name),
        'fullName': full_name,
        'environment': myutils.get_first('Environment', tags),
        'instanceId': instance.get('InstanceId', ''),
        'state': instance.get('State', {}).get('Name', ''),
        'publicIpAddress': instance.get('PublicIpAddress', '')
    }


def get_short_name(full_name):
    """Retrieve short server name from full name."""
    if full_name.startswith('mcservers-'):
        name = full_name.split('/')[1]
    else:
        name = full_name.split('-')[-1]
    return name
