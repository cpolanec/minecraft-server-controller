"""Unit testing for 'myutils' module."""
import myutils


def test_get_first():
    """Test get_first() function."""
    assert myutils.get_first('', []) == ''
    assert myutils.get_first('Hello', []) == ''
    assert myutils.get_first('Hello', [{}]) == ''
    assert myutils.get_first('Hello', [{'Key': 'NotHello'}]) == ''
    assert myutils.get_first('Hello', [{'Key': 'Hello'}]) == ''
    assert myutils.get_first(
        'Hello', [{'Key': 'Hello', 'Value': 'World'}]) == 'World'
    assert myutils.get_first(
        'Hello',
        [
            {'Key': 'Hello', 'Value': 'World'},
            {'Key': 'Hello', 'Value': 'Bizarro'}
        ]
    ) == 'World'
