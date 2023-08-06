import logging


class Logger(object):
    def __init__(self, error_def: dict, logger_name='ni.config'):
        # create logger
        self._core = logging.Logger(logger_name, logging.DEBUG)
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # create formatter
        formatter = logging.Formatter('%(levelname)s | %(name)s | %(asctime)s | %(message)s')
        # add formatter to ch
        ch.setFormatter(formatter)
        # add ch to logger
        self._core.addHandler(ch)
        self._error_def = error_def

    def debug(self, msg_args: list, *args, **kwargs):
        msg_id = str(msg_args[0])
        msg = self._error_def[msg_id].format(*msg_args)
        self._core.debug(msg, *args, **kwargs)

    def info(self, msg_args, *args, **kwargs):
        msg_id = str(msg_args[0])
        msg = self._error_def[msg_id].format(*msg_args)
        self._core.info(msg, *args, **kwargs)

    def warning(self, msg_args, *args, **kwargs):
        msg_id = str(msg_args[0])
        msg = self._error_def[msg_id].format(*msg_args)
        self._core.warning(msg, *args, **kwargs)

    def error(self, msg_args, *args, **kwargs):
        msg_id = str(msg_args[0])
        msg = self._error_def[msg_id].format(*msg_args)
        self._core.error(msg, *args, **kwargs)

    def critical(self, msg_args, *args, **kwargs):
        msg_id = str(msg_args[0])
        msg = self._error_def[msg_id].format(*msg_args)
        self._core.critical(msg, *args, **kwargs)


ERROR_DEF = {
    '1000': '[{0}] 待校验参数{1}类型或其值异常，验证不通过',
    '1001': '[{0}] 待校验参数{1}属于非法参数，验证不通过',
    '2000': '[{0}] Succeeded reading file "{1}".',
    '2001': '[{0}] {1} is not found.'
}

logger = Logger(ERROR_DEF)
