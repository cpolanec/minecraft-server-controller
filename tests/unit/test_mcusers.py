"""Unit testing for 'mcusers' module."""

import boto3
import mock
import moto
import mcusers


def test_parse_mcrcon_list():
    """Test parse_mcrcon_list() function."""
    no_users = 'There are 0 of a max of 20 players online:'
    users = mcusers.parse_mcrcon_list(no_users)
    assert users['count'] == 0
    assert users['names'] == []

    multi_users = \
        'There are 2 of a max of 20 players online: User1, AnotherUser'
    users = mcusers.parse_mcrcon_list(multi_users)
    assert users['count'] == 2
    assert users['names'] == ['User1', 'AnotherUser']


@moto.mock_ssm
def test_gather():
    """Test gather() function."""
    ssm = boto3.client('ssm')
    ssm.put_parameter(
        Name='/minecraft/mcrcon/password',
        Value='foobar'
    )

    with mock.patch('mcusers.mcrcon.MCRcon'):

        with mock.patch(
                'mcusers.mcserver.gather',
                return_value={}):
            assert mcusers.gather('') == {}

        with mock.patch(
                'mcusers.mcserver.gather',
                return_value={'PublicIpAddress': '0.0.0.0'}):
            users = mcusers.gather('')
            assert users['count'] == 0
            assert users['names'] == []
