"""Unit testing for servers module."""
import pytest
import servers


@pytest.fixture(name='inst_jenny')
def fixture_inst_jenny():
    """Define example instance data: Jenny."""
    return {
        'InstanceId': '8675309',
        'State': {
            'Name': 'stopped'
        },
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
        'Name': 'jenny',
        'FullName': 'minecraft-main-server-jenny',
        'Environment': 'main',
        'InstanceId': '8675309',
        'State': 'stopped'
    }


def test_get_server_names():
    """Test get_server_names() function."""
    assert servers.get_server_name([]) == ''
    assert servers.get_server_name([{}]) == ''
    assert servers.get_server_name([{'Key': 'Name'}]) == ''
    assert servers.get_server_name([{'Key': 'Name', 'Value': ''}]) == ''
    assert servers.get_server_name(
        [{'Key': 'Name', 'Value': 'foo-bar'}]) == 'foo-bar'


def test_get_environment():
    """Test get_server_names() function."""
    assert servers.get_environment([]) == ''
    assert servers.get_environment([{}]) == ''
    assert servers.get_environment([{'Key': 'Environment'}]) == ''
    assert servers.get_server_name([{'Key': 'Environment', 'Value': ''}]) == ''
    assert servers.get_environment(
        [{'Key': 'Environment', 'Value': 'test'}]) == 'test'


def test_map_instance(inst_jenny, srvr_jenny):
    """Test map_instance() function."""
    assert servers.map_instance({}) == {
        'Name': '',
        'FullName': '',
        'Environment': '',
        'InstanceId': '',
        'State': ''
    }
    assert servers.map_instance(inst_jenny) == srvr_jenny


def test_process_instance_data(inst_jenny, srvr_jenny):
    """Test process_instance_data() function."""
    assert servers.process_instance_data({}) == []
    assert servers.process_instance_data({'Reservations': []}) == []
    assert servers.process_instance_data({
        'Reservations': [{
            'Instances': [inst_jenny]
        }]
    }) == [srvr_jenny]
