import time
import datetime

from functools import wraps
from importlib import import_module


def timer_deco(logger):
    """

    :param logger:
    :return:
    """
    def wrapper(func):
        @wraps(func)
        def timer_func(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            logger.info("Name: {}, time_now: {},  consume: {}".format(func.__name__,
                                                                      datetime.datetime.now(),
                                                                      round(time.time() - start_time, 7)))
            return result
        return timer_func
    return wrapper


def load_object(path):
    """Load an object given its absolute object path, and return it.

    object can be a class, function, variable or an instance.
    path ie: 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware'
    """

    try:
        dot = path.rindex('.')
    except ValueError:
        raise ValueError("Error loading object '%s': not a full path" % path)

    module, name = path[:dot], path[dot+1:]
    mod = import_module(module)

    try:
        obj = getattr(mod, name)
    except AttributeError:
        raise NameError("Module '%s' doesn't define any object named '%s'" % (module, name))
    return obj


if __name__ == "__main__":
    pass

