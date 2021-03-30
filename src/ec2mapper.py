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
    full_name = get_server_name(tags)
    return {
        'name': full_name.split('-')[-1],
        'fullName': full_name,
        'environment': get_environment(tags),
        'instanceId': instance.get('InstanceId', ''),
        'state': instance.get('State', {}).get('Name', ''),
        'publicIpAddress': instance.get('PublicIpAddress', '')
    }


def get_server_name(tags):
    """Retrieve server name from AWS EC2 tags."""
    names = list(filter(lambda d: d.get('Key') == 'Name', tags))
    return names[0].get('Value', '') if len(names) > 0 else ''


def get_environment(tags):
    """Retrieve environment from AWS EC2 tags."""
    names = list(filter(lambda d: d.get('Key') == 'Environment', tags))
    return names[0].get('Value', '') if len(names) > 0 else ''
