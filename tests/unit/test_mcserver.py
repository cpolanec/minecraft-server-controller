"""Unit testing for 'mcserver' module."""

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
