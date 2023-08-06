# -*- encoding: utf-8 -*-
"""
@File    :   logger_util.py
@Time    :   2021/09/24 13:18:37
@Author  :   Gary.Wang
@Version :   1.0
@Contact :   wangyijun@shwfed.com
@License :   (C)Copyright 1990 - 2021, shwfed.com
@Desc    :   日志辅助工具
"""

# here put the import lib
from enum import Enum, unique
from logging import handlers
from pathlib import Path
import logging


@unique
class LoggerLevel(Enum):
    """
    日志级别，包括：
        DEBUG : 调试级别
        INFO : 信息级别
        WARNING : 警告级别
        ERROR : 错误级别
    """
    DEBUG = 'debug',
    INFO = 'info',
    WARNING = 'warning',
    ERROR = 'error'


class LoggerUtil(object):
    """
    日志工具类
    """

    __level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __checker_log_dir(self):
        """
        检查日志目录是否存在
        """
        _root = Path.cwd()
        _log_path = _root.joinpath('logs')
        if not _log_path.exists():
            _log_path.mkdir(0o766, exist_ok=True)

    def __init__(self, level: LoggerLevel = LoggerLevel.INFO, prefix='', when='midnight', backCount=5, fmt='%(asctime)s - %(filename)s - %(module)s - %(funcName)s - [line:%(lineno)d] - %(levelname)s: %(message)s'):
        """
        初始化日志类构造函数

        :param level: 日志级别包括：debug,info,warning,error。默认为--info
        :param prefix:  文件存储名前缀
        :param when: 间隔的时间单位，D 为每日
        :param backCount: 备份文件的数量
        :param fmt: 日志格式
        """
        self.__checker_log_dir()
        if not isinstance(level, LoggerLevel):
            level = LoggerLevel.INFO
        _level = level.value
        if isinstance(_level, tuple):
            _level = _level[0]

        _root = Path.cwd()
        _log_path = None
        if prefix != '':
            _log_path = _root.joinpath('logs', f'{prefix}-{_level}.log')
        else:
            _log_path = _root.joinpath('logs', f'{_level}.log')
        _filename = str(_log_path)

        self.logger = logging.getLogger(_filename)
        # 输出日志的格式
        format_str = logging.Formatter(fmt)
        self.logger.setLevel(self.__level_relations.get(_level))
        # 定义控制台日志控制器
        sh = logging.StreamHandler()
        sh.setFormatter(format_str)
        # 定义文件日志控制器
        th = handlers.TimedRotatingFileHandler(filename=_filename, when=when, interval=1, backupCount=backCount, encoding='utf-8')
        th.setFormatter(format_str)
        # 将日志控制器添加到日志对象中
        self.logger.addHandler(sh)
        self.logger.addHandler(th)
