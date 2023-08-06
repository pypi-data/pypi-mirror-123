from functools import wraps
from typing import Callable, Iterable, Union, Set
import logging

__all__ = [
    'log_return', 'debug_log', 'log_exception', 'inject_logger', 'create_logger',
    'LogError'
]

__logger_names: Set[str] = set()


def logger_names():
    return __logger_names


class LogError(Exception):

    def __init__(self, message):
        self.message = message


def log_return(name: str, level=20):
    """
    Logs the value of the decorated function.
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ret = func(*args, **kwargs)
            logger = __get_logger(name)
            logger.log(level, ret)
            return ret
        return wrapper

    return decorator


def debug_log(name: str):
    """
    Debug logs the name, parameters and the return value of the decorated function.
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            ret = func(*args, **kwargs)
            logger = __get_logger(name)
            logger.debug(f'{func.__name__}({signature}), return value: {ret!r}')
            return ret
        return wrapper
    return decorator


def log_exception(name: str, exc_info=True):
    """
    Error logs any exception which occurred in the decorated function.

    Exception is re-raised after logging.
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                print()
                ret = func(*args, **kwargs)
                return ret
            except Exception as e:
                logger = __get_logger(name)
                msg = f'{e.__class__.__name__}: {e}'
                logger.error(msg=msg, exc_info=exc_info)
                raise
        return wrapper

    return decorator


def inject_logger(name: Union[Iterable[str], str]):
    """
    Adds the injected logger to your function.

    Get logger object: ``decorated_function.logger``.

    If you passed an iterable get it like this: ``decorated_function.logger[index]``

    :param name: String or iterable string
    :return: None
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if isinstance(name, str):
                wrapper.logger = __get_logger(name)
            else:
                wrapper.logger = [__get_logger(n) for n in name]

            ret = func(*args, **kwargs)
            return ret

        return wrapper

    return decorator


def create_logger(
    name: str,
    file_path: str = None,
    level: int = logging.DEBUG,
    console_log: bool = True,
    formatter: logging.Formatter = logging.Formatter(
        fmt='%(levelname)s:%(name)s:%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
):
    """
    :param name: Name of logger.
    :param file_path: If not None log to this file.
    :param level: Minimum log level. Logging below this level is ignored.
    :param console_log: Whether to allow console logging or not.
    :param formatter: Formats log messages.
    """

    if not console_log and file_path is None:
        raise LogError('Both console and file logging is disabled.')

    if name in __logger_names:
        raise LogError(f'Logger already created with {name}!')

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = 0

    if console_log and not __has_stream_handler(logger.handlers):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    if file_path is not None and not __has_file_handler(logger.handlers):
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    __logger_names.add(logger.name)
    return logger


def __get_logger(name: str):

    if name in __logger_names:
        return logging.getLogger(name)

    raise LogError(
        f'Logger with name: {name} does not exists. Call create_logger, to create a logger with this name!'
    )


def __has_file_handler(lst):
    from logging import FileHandler
    for e in lst:
        if isinstance(e, FileHandler):
            return True

    return False


def __has_stream_handler(lst):
    from logging import StreamHandler
    for e in lst:
        if isinstance(e, StreamHandler):
            return True

    return False
