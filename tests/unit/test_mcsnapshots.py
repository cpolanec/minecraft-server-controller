"""Unit testing for 'mcsnapshots' module."""

import json
import boto3
import moto
import mcsnapshots
import myutils


@moto.mock_ec2
def test_gather():
    """Test gather() function."""
    snapshots = mcsnapshots.gather(None)
    assert snapshots == []

    snapshots = mcsnapshots.gather('foobar')
    assert snapshots == []


@moto.mock_ec2
def test_fetch_volume_id():
    """Test fetch_volume_id() function."""
    ec2 = boto3.resource('ec2')
    instance = ec2.create_instances(
        ImageId='ami-xxxxxx', MinCount=1, MaxCount=1)[0]

    volume_id = mcsnapshots.fetch_volume_id(instance.id)
    assert volume_id is None


@moto.mock_ec2
def test_create_snapshot():
    """Test create_snapshot() function."""
    ec2 = boto3.resource('ec2')
    volume = ec2.create_volume(AvailabilityZone='', Size=4)

    snapshot = mcsnapshots.create_snapshot(
        volume.id, 'unittest', 'foobar', 'pytest')
    assert snapshot.get('SnapshotId').startswith('snap-')
    assert snapshot.get('Description').startswith('Snapshot of')

    tags = snapshot.get('Tags', [])
    assert myutils.get_first('Application', tags) == 'mcservers'
    assert myutils.get_first('Environment', tags) == 'pytest'
    assert myutils.get_first('Event', tags) == 'unittest'
    assert myutils.get_first('Server', tags) == 'foobar'


@moto.mock_ec2
def test_get_handler():
    """Test get_handler() function."""
    response = mcsnapshots.get_handler({}, {})
    assert response.get('statusCode') == 200

    event = {'pathParameters': {'name': 'foobar'}}
    response = mcsnapshots.get_handler(event, {})
    assert response.get('statusCode') == 200


@moto.mock_ec2
def test_post_handler():
    """Test get_handler() function."""
    body = json.dumps({})
    event = {'body': body}
    response = mcsnapshots.post_handler({'body': body}, {})
    assert response.get('statusCode') == 200

    body = json.dumps({})
    event = {'body': body, 'pathParameters': {'name': 'foobar'}}
    response = mcsnapshots.post_handler(event, {})
    assert response.get('statusCode') == 200
