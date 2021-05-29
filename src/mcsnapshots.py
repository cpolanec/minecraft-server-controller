"""Handlers for API operations at /snapshots level."""

import datetime
import json
import logging
import boto3
import ebsmapper
import mcserver
import myutils

logger = myutils.get_logger(__name__, logging.INFO)

# =============================================================================
# REST API handler methods
# =============================================================================


@myutils.log_calls(level=logging.DEBUG)
def get_handler(event, context):  # pylint: disable=unused-argument
    """REST API GET method to list Minecraft game snapshots."""
    # gather data for http response
    server_name = event.get('pathParameters', {}).get('name')
    snapshots = gather(server_name)

    # return the HTTP payload
    return {
        'statusCode': 200,
        'body': json.dumps({
            'snapshots': snapshots
        })
    }


@myutils.log_calls(level=logging.DEBUG)
def post_handler(event, context):  # pylint: disable=unused-argument
    """REST API POST method to create new Minecraft game snapshots."""
    server_name = event.get('pathParameters', {}).get('name', None)
    event_name = json.loads(event.get('body')).get('event', '')

    server_data = mcserver.gather(server_name)
    instance_id = server_data.get('instanceId')
    server_name = server_data.get('name', '')
    environment = server_data.get('environment', '')

    volume_id = None
    if instance_id is not None:
        volume_id = fetch_volume_id(instance_id)

    snapshot = None
    if volume_id is not None:
        snapshot = create_snapshot(
            volume_id, event_name, server_name, environment)

    # return the HTTP payload
    response = {}
    if snapshot is not None:
        response = {
            'snapshotId': snapshot.get('SnapshotId', ''),
            'description': snapshot.get('Description', ''),
            'state': snapshot.get('State', '')
        }
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }


# =============================================================================
# REST API helper methods
# =============================================================================

@myutils.log_calls
def gather(server_name):
    """Return a list of Minecraft game snapshots."""
    # initialize AWS SDK query filters
    filters = []
    filters.append(myutils.get_application_filter())
    if server_name is not None:
        filters.append({
            'Name': 'tag:Server',
            'Values': [server_name]
        })

    # invoke AWS SDK to gather EBS snapshots
    ec2_client = boto3.client('ec2')
    sdk_snapshots = ec2_client.describe_snapshots(Filters=filters)

    # format raw AWS SDK data to user-friendly context
    snapshots = ebsmapper.parse(sdk_snapshots)
    return snapshots


@myutils.log_calls(level=logging.DEBUG)
def fetch_volume_id(instance_id):
    """Return the volume ID of the given server."""
    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_volumes(Filters=[
        {
            'Name': 'attachment.instance-id',
            'Values': [instance_id]
        },
        {
            'Name': 'attachment.device',
            'Values': ['/dev/sdm']
        }
    ])
    volumes = response.get('Volumes', [])
    return volumes[0].get('VolumeId', None) if len(volumes) else None


@myutils.log_calls(level=logging.DEBUG)
def create_snapshot(volume_id, event_name, server_name, environment):
    """Create a snapshot for the given volume ID."""
    now = datetime.datetime.now()
    timestamp = datetime.datetime.isoformat(now)
    desc = 'Snapshot of \'{}\' game server on {}'.format(
        server_name, timestamp
    )
    name = 'mcservers-{}-{}-{}'.format(
        environment,
        server_name,
        now.timestamp()
    )

    ec2_client = boto3.client('ec2')
    response = ec2_client.create_snapshot(
        Description=desc,
        VolumeId=volume_id,
        TagSpecifications=[
            {
                'ResourceType': 'snapshot',
                'Tags': [

                    {'Key': 'Name', 'Value': name},
                    {'Key': 'Application', 'Value': 'mcservers'},
                    {'Key': 'Environment', 'Value': environment},
                    {'Key': 'Event', 'Value': event_name},
                    {'Key': 'Server', 'Value': server_name},
                    {'Key': 'Timestamp', 'Value': timestamp}
                ]
            }
        ]
    )
    return response
