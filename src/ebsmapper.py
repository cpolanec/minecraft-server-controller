"""Helper methods for parsing EBS-related data from AWS SDK."""

import logging
import myutils

logger = myutils.get_logger(__name__, logging.DEBUG)


@myutils.log_calls(level=logging.DEBUG)
def parse(sdk_snapshots):
    """Process raw EBS snapshot data."""
    snapshots = []
    snapshots.extend(
        map(map_snapshot, sdk_snapshots.get('Snapshots', []))
    )
    return snapshots


@myutils.log_calls(level=logging.DEBUG)
def map_snapshot(snapshot):
    """Map AWS EBS snapshot data to response message format."""
    tags = snapshot.get('Tags', [])
    return {
        'name': myutils.get_first('Name', tags),
        'server': get_server_name(tags),
        'snapshotId': snapshot.get('SnapshotId', ''),
        'event': myutils.get_first('Event', tags),
        'timestamp': myutils.get_first('Timestamp', tags)
    }


def get_server_name(tags):
    """Retrieve server name from across different tag scenarios."""
    server = myutils.get_first('Server', tags)
    if server is None or server == '':
        name_parts = myutils.get_first('Name', tags).split('-')
        prefix = name_parts[0] if len(name_parts) > 0 else ''
        if prefix == 'minecraft':
            server = name_parts[3] if len(name_parts) > 3 else ''
        else:
            server = name_parts[2] if len(name_parts) > 2 else ''
    return server
