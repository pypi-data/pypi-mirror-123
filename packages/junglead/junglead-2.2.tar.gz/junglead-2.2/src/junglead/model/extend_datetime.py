# -*- encoding: utf-8 -*-
"""
@File    :   extend_datetime.py
@Time    :   2021/09/27 16:02:59
@Author  :   Gary.Wang
@Version :   1.0
@Contact :   wangyijun@shwfed.com
@License :   (C)Copyright 1990 - 2021, shwfed.com
@Desc    :   扩展的日期时间对象
"""

# here put the import lib
from datetime import datetime, timezone, timedelta


class ExtendDatetime(datetime):
    """
    扩展日期时间对象
    """

    def __init__(self, year: int, month: int, day: int, hour: int, minute: int, second: int, microsecond: int, tzinfo: timezone = None, date_format: str = '%Y-%m-%d %H:%M:%S'):
        """
        构造方法
        """
        self.date_format = date_format
        # self.year = year
        # self.month = month
        # self.day = day
        # self.hour = hour
        # self.minute = minute
        # self.second = second
        # self.microsecond = microsecond
        # self.tzinfo.update(tzinfo)

    def __new__(cls, year: int, month: int, day: int, hour: int, minute: int, second: int, microsecond: int, tzinfo: timezone = None, date_format: str = '%Y-%m-%d %H:%M:%S'):
        """
        初始化方法

        :param value: 初始化值
        :param date_format: 日期格式
        """
        cls.date_format = date_format
        return super().__new__(cls, year, month, day, hour, minute, second, microsecond, tzinfo)

    @staticmethod
    def now(tz: timezone = timezone(timedelta(hours=8)), date_format: str = "%Y-%m-%d %H:%M:%S"):
        """
        获取当前日期时间的扩展类型

        :param tz: timezone，时区
        :param date_format: 日期时间格式

        :return ExtendDatetime, 返回扩展日期时间格式
        """
        _dt = ExtendDatetime.convert(datetime.now(tz=tz), date_format=date_format)
        return _dt

    @staticmethod
    def convert(dt: datetime, date_format: str = "%Y-%m-%d %H:%M:%S"):
        """
        将标准日期时间格式转换为扩展类型

        :param dt: datetime, 标准的日期时间格式
        :param date_format: 日期时间格式

        :return ExtendDatetime, 返回扩展日期时间格式
        """
        return ExtendDatetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond, dt.tzinfo, date_format)

    def __str__(self):
        if self.date_format is None or self.date_format == '':
            self.date_format = '%Y-%m-%d %H:%M:%S'
        return self.strftime(self.date_format)

    def __repr__(self):
        if self.date_format is None or self.date_format == '':
            self.date_format = '%Y-%m-%d %H:%M:%S'
        return self.strftime(self.date_format)
