"""Unit testing for 'ec2mapper' module."""

import pytest
import ec2mapper


@pytest.fixture(name='inst_jenny')
def fixture_inst_jenny():
    """Define example instance data: Jenny."""
    return {
        'InstanceId': '8675309',
        'State': {
            'Name': 'stopped'
        },
        'PublicIpAddress': '10.11.12.13',
        'Tags': [{
            'Key': 'Name',
            'Value': 'minecraft-main-server-jenny'
        }, {
            'Key': 'Environment',
            'Value': 'main'
        }]
    }


@pytest.fixture(name='srvr_jenny')
def fixture_srvr_jenny():
    """Define example server data: Jenny."""
    return {
        'name': 'jenny',
        'fullName': 'minecraft-main-server-jenny',
        'environment': 'main',
        'instanceId': '8675309',
        'state': 'stopped',
        'publicIpAddress': '10.11.12.13'
    }


def test_get_full_name():
    """Test get_server_names() function."""
    assert ec2mapper.get_full_name([]) == ''
    assert ec2mapper.get_full_name([{}]) == ''
    assert ec2mapper.get_full_name([{'Key': 'Name'}]) == ''
    assert ec2mapper.get_full_name([{'Key': 'Name', 'Value': ''}]) == ''
    assert ec2mapper.get_full_name(
        [{'Key': 'Name', 'Value': 'foo-bar'}]) == 'foo-bar'


def test_get_short_name():
    """Test get_server_names() function."""
    assert ec2mapper.get_short_name('') == ''
    assert ec2mapper.get_short_name('minecraft-test-foobar') == 'foobar'
    assert ec2mapper.get_short_name(
        'mcservers-test/foobar/instance') == 'foobar'


def test_get_environment():
    """Test get_environment() function."""
    assert ec2mapper.get_environment([]) == ''
    assert ec2mapper.get_environment([{}]) == ''
    assert ec2mapper.get_environment([{'Key': 'Environment'}]) == ''
    assert ec2mapper.get_environment(
        [{'Key': 'Environment', 'Value': ''}]) == ''
    assert ec2mapper.get_environment(
        [{'Key': 'Environment', 'Value': 'test'}]) == 'test'


def test_map_instance(inst_jenny, srvr_jenny):
    """Test map_instance() function."""
    assert ec2mapper.map_instance({}) == {
        'name': '',
        'fullName': '',
        'environment': '',
        'instanceId': '',
        'state': '',
        'publicIpAddress': ''
    }
    assert ec2mapper.map_instance(inst_jenny) == srvr_jenny


def test_process_instance_data(inst_jenny, srvr_jenny):
    """Test process_instance_data() function."""
    assert ec2mapper.parse({}) == []
    assert ec2mapper.parse({'Reservations': []}) == []
    assert ec2mapper.parse({
        'Reservations': [{
            'Instances': [inst_jenny]
        }]
    }) == [srvr_jenny]
