"""Setup unit test environment."""

import sys
import os


def updatepath():
    """Update sys.path with *src* directory."""
    mypath = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, mypath + '/../src/')


updatepath()
