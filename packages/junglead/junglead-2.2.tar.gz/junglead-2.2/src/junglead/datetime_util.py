# -*- encoding: utf-8 -*-
"""
@File    :   datetime_util.py
@Time    :   2021/09/24 14:36:56
@Author  :   Gary.Wang
@Version :   1.0
@Contact :   wangyijun@shwfed.com
@License :   (C)Copyright 1990 - 2021, shwfed.com
@Desc    :   日期时间帮助工具
"""

# here put the import lib
from datetime import datetime, timezone, timedelta
from enum import Enum, unique
from time import time
import locale


@unique
class PlusFormat(Enum):
    """
    时间日期的计算格式枚举对象，仅支持Python官方支持的
    """
    WEEK = '周',
    DAY = '日',
    HOUR = '时',
    MINUTE = '分'


class DatetimeUtil:
    """
    日期时间工具类
    """

    @staticmethod
    def get_timezone_asia():
        """
        获取亚洲/上海时区

        :return tzinfo, 返回默认的时区
        """
        return timezone(timedelta(hours=8))

    @staticmethod
    def get_timezone(time_difference: int):
        """
        根据给定的时差返回时区对象

        :param time_difference: 时差

        :return tzinfo, 返回默认的时区
        """
        return timezone(timedelta(hours=time_difference))

    @staticmethod
    def after_now(dt: datetime, tz: timezone = timezone(timedelta(hours=8))):
        """
        给定时间是否晚于、大于当前时间

        :param dt: 给定时间。必须包含时区，否则会抛出异常
        :param tz: 当前日期时间的时区， 默认为亚洲/上海时间

        :return bool, 返回比较结果
        """
        _now = datetime.now(tz=tz)
        if dt.tzinfo is None:
            raise Exception("给定的比较时间，不包含时区")
        return (dt - _now).total_seconds() > 0

    @staticmethod
    def before_now(dt: datetime, tz: timezone = timezone(timedelta(hours=8))):
        """
        给定时间是否早于、小于当前时间

        :param dt: 给定时间。必须包含时区，否则会抛出异常
        :param tz: 当前日期时间的时区， 默认为亚洲/上海时间

        :return bool, 返回比较结果
        """
        _now = datetime.now(tz=tz)
        if dt.tzinfo is None:
            raise Exception("给定的比较时间，不包含时区")
        return (_now - dt).total_seconds() > 0

    @staticmethod
    def compare_date(dt1: datetime, dt2: datetime):
        """
        比较两个日期的大小，与时区无关

        :param dt1: 第一个日期时间对象
        :param dt2: 第二个日期时间对象

        :return int, 返回两个时间的比较结果。1、0 或者 -1
        """
        _diff = DatetimeUtil.diff_date(dt1, dt2)
        return 1 if _diff > 0 else (-1 if _diff < 0 else 0)

    @staticmethod
    def minus_datetime(dt1: datetime, dt2: datetime):
        """
        计算两个日期之间的差距，与时区无关

        :param dt1: 第一个日期时间对象
        :param dt2: 第二个日期时间对象

        :return int, 两个时间之间的差距，单位是秒，负数表示第二时间晚于第一时间。
        """
        _delta = dt1 - dt2
        return _delta.total_seconds()

    @staticmethod
    def plus_datetime(dt: datetime, increment: int, compare_format: PlusFormat):
        """
        计算日期时间

        :param dt: 给定的日期时间，与时区无关
        :param increment: 计算增量，支持负数
        :param compare_format: 比较格式

        :return datetime, 返回计算后的结果
        """
        if compare_format == PlusFormat.WEEK:
            return dt + timedelta(weeks=increment)
        elif compare_format == PlusFormat.DAY:
            return dt + timedelta(days=increment)
        elif compare_format == PlusFormat.HOUR:
            return dt + timedelta(hours=increment)
        elif compare_format == PlusFormat.MINUTE:
            return dt + timedelta(minutes=increment)
        else:
            raise Exception("不支持的计算格式")

    @staticmethod
    def plus_datetime_material(dt: datetime, weeks: float = 0, days: float = 0, hours: float = 0, minutes: float = 0):
        """
        更加粒度化的计算时间

        :param dt: 给定的日期时间，与时区无关
        :param weeks: 增加的周数
        :param days: 增加的天数
        :param hours: 增加的小时数
        :param minutes: 增加的分钟数

        :return datetime, 返回计算后的结果
        """
        if weeks == 0 and days == 0 and hours == 0 and minutes == 0:
            raise Exception("请至少输入一个增加纬度")
        return dt + timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes)

    @staticmethod
    def convert_from_str(dt: str, date_format: str = '%Y-%m-%d %H:%M:%S', tz: timezone = timezone(timedelta(hours=8))):
        """
        把字符串转换为日期时间对象

        :param dt: 标准格式的字符串，标准格式为：YYYY-mm-dd HH:MM:SS
        :param date_format: 日期时间格式

        :return datetime, 返回带有时区信息的日期时间
        """
        return datetime.strptime(dt, date_format).replace(tzinfo=tz)

    @staticmethod
    def convert_from_timestamp(t: float, tz: timezone = timezone(timedelta(hours=8))):
        """
        把时间戳换为日期时间对象

        :param t: 标准时间戳，仅支持10位长度
        :param date_format: 日期时间格式

        :return datetime, 返回带有时区信息的日期时间
        """
        return datetime.fromtimestamp(t).replace(tzinfo=tz)

    @staticmethod
    def get_timestamp(length: int = 10):
        """
        返回当前时间戳

        :param length: 时间戳长度。Python默认返回为10位，标准应该是13位。

        :return int, 返回当前时间戳
        """
        _now = time()
        return int(_now) if length == 10 else int(_now*1000)

    @staticmethod
    def get_current_simple_str(include_ms: bool = True, tz: timezone = timezone(timedelta(hours=8))):
        """
        根据指定时区，返回当前时间的标识码格式

        :param include_ms: 是否包含毫秒
        :param tz: 时区，默认为亚洲/上海时间

        :return str, 返回当前时间标识码
        """
        return datetime.now(tz=tz).strftime('%Y%m%d%H%M%S%f' if include_ms else '%Y%m%d%H%M%S')

    @staticmethod
    def to_standard_str(dt: datetime):
        """
        返回年月日日时分的常见格式字符串，不包含毫秒

        :param dt: 转换的日期

        :return str, 返回字符串
        """
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def to_Chinese_str(dt: datetime):
        """
        返回年月日日时分的标准中文字符串

        :param dt: 转换的日期

        :return str, 返回字符串
        """
        locale.setlocale(locale.LC_CTYPE, 'chinese')
        '{2}年{3}月{4}日 {12}点{14}分{15}秒'
        return dt.strftime('%Y年%m月%d日 %H时%M分%S秒')
