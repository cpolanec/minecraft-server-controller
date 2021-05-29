"""Unit testing for 'ebsmapper' module."""
import ebsmapper


def test_parse():
    """Test parse() function."""
    assert len(ebsmapper.parse({'Snapshots': [{}, {}]})) == 2


def test_map_snapshot():
    """Test map_snapshot() function."""
    assert ebsmapper.map_snapshot({}) == {
        'name': '',
        'server': '',
        'snapshotId': '',
        'event': '',
        'timestamp': ''
    }
    assert ebsmapper.map_snapshot({
        'SnapshotId': 'snap-0123456789',
        'Tags': [
            {'Key': 'Name', 'Value': 'mcservers-test-foobar-0123456789'},
            {'Key': 'Event', 'Value': 'test.unit'},
            {'Key': 'Timestamp', 'Value': '1955-11-12T06:00Z'}
        ]
    }) == {
        'name': 'mcservers-test-foobar-0123456789',
        'server': 'foobar',
        'snapshotId': 'snap-0123456789',
        'event': 'test.unit',
        'timestamp': '1955-11-12T06:00Z'
    }


def test_get_server_name():
    """Test get_server_name() function."""
    assert ebsmapper.get_server_name([]) == ''
    assert ebsmapper.get_server_name([{}]) == ''
    assert ebsmapper.get_server_name([{'Key': 'Server'}]) == ''
    assert ebsmapper.get_server_name([
        {'Key': 'Server', 'Value': 'foobar'}]) == 'foobar'
    assert ebsmapper.get_server_name([{
        'Key': 'Name',
        'Value': 'minecraft-test-servers-foobar'
    }]) == 'foobar'
    assert ebsmapper.get_server_name([{
        'Key': 'Name',
        'Value': 'mcservers-test-foobar'
    }]) == 'foobar'
