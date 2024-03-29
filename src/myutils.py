"""Utilities for this application (e.g. logging aspects)."""

import functools
import logging


def get_logger(module_name, level):
    """Create a common logger for app modules."""
    logger = logging.getLogger()
    for handler in logger.handlers:
        handler.setFormatter(logging.Formatter(
            '%(levelname)s %(aws_request_id)s %(message)s\n'
        ))

    logger = logging.getLogger(module_name)
    logger.setLevel(level)
    return logger


def log_calls(func=None, level=logging.INFO):
    """Define a decorator for logging a method call (args & returns)."""
    if not func:
        return functools.partial(log_calls, level=level)

    logger = logging.getLogger(func.__module__)

    @functools.wraps(func)
    def wrapper(*args, **kwds):
        # log before entering the function
        start = {
            'method': '{}.{}'.format(func.__module__, func.__name__),
            'state': 'entering',
            'args': [*args]
        }
        logger.log(level, '%s', start)

        # call the function
        result = func(*args, **kwds)

        # log after exiting the function
        if result is not None:
            end = {
                'method': '{}.{}'.format(func.__module__, func.__name__),
                'state': 'exited',
                'args': [*args],
                'result': result
            }
            logger.log(level, '%s', end)

        return result
    return wrapper


def get_application_filter():
    """Return SDK filter to return Minecraft application resources."""
    return {
        'Name': 'tag:Application',
        'Values': ['minecraft', 'mcservers']
    }


def get_instance_filter():
    """Return SDK filter to return active EC2 instances."""
    return {
        'Name': 'instance-state-name',
        'Values': [
            'pending', 'running',
            'shutting-down', 'stopping', 'stopped'
        ]
    }


def get_first(key, tags):
    """Return first tag value associated with the provided tag key."""
    values = list(filter(lambda d: d.get('Key') == key, tags))
    return values[0].get('Value', '') if len(values) > 0 else ''
