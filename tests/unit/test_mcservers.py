"""Unit testing for 'mcservers' module."""

import moto
import mcservers


@moto.mock_ec2
def test_gather():
    """Test gather() function."""
    servers = mcservers.gather()
    assert servers == []
