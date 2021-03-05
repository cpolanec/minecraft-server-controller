"""Unit testing for 'mcserver' module."""

import boto3
import moto
import mcserver


@moto.mock_ec2
def test_gather():
    """Test gather() function."""
    server = mcserver.gather('foobar')
    assert server == {}


def test_process_ec2_data():
    """Test gather_server_data() function."""
    reservations = {'Reservations': []}
    server = mcserver.process_ec2_data(reservations)
    assert server == {}

    reservations = {'Reservations': [{'Instances': []}]}
    server = mcserver.process_ec2_data(reservations)
    assert server == {}

    reservations = {'Reservations': [{'Instances': [{}]}]}
    server = mcserver.process_ec2_data(reservations)
    assert server != {}

    reservations = {'Reservations': [{'Instances': [{}, {}]}]}
    server = mcserver.process_ec2_data(reservations)
    assert server != {}


@moto.mock_ec2
def test_change_server_state():
    """Test change_server_state() function."""
    ec2_client = boto3.client('ec2')
    image_id = ec2_client.describe_images()['Images'][0]['ImageId']
    reservation = ec2_client.run_instances(
        ImageId=image_id, MinCount=1, MaxCount=1)
    instance_id = reservation['Instances'][0]['InstanceId']
    server = {'name': 'test', 'instanceId': instance_id}

    new_state = mcserver.change_server_state(server, 'running')
    assert new_state == 'pending'

    new_state = mcserver.change_server_state(server, 'stopped')
    assert new_state == 'stopping'

    new_state = mcserver.change_server_state(server, 'rebooting')
    assert new_state == 'pending'

    new_state = mcserver.change_server_state(server, 'foobar')
    assert new_state is None
