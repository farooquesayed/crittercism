import time
from yopenstackqe_tests.exceptions import TimeoutException


def wait_for_event(timeout, period, timeout_message, func, *args, **kwargs):
    """Waits until func(*args, **kwargs) returns non None result.
    Function 'func' invoked each 'period' seconds until 'timeout' is reached.
    'func' is responsible for suppressing of all expected exceptions itself.
    :param timeout: maximum waiting time in seconds
    :param period: time between run of 'func' function in seconds
    :param timeout_message: detailed exception description in case of timeout
    :return: function 'func' result or rises TimeoutException if timeout has been reached
    """
    start_time = time.time()
    while time.time() - start_time <= timeout:
        result = func(*args, **kwargs)
        if result:
            return result
        time.sleep(period)
    raise TimeoutException(timeout_message + ". Timeout after: %s sec." % timeout)
