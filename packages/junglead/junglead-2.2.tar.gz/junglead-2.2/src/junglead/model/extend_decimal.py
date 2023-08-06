# -*- encoding: utf-8 -*-
"""
@File    :   extend_decimal.py
@Time    :   2021/09/27 13:49:55
@Author  :   Gary.Wang
@Version :   1.0
@Contact :   wangyijun@shwfed.com
@License :   (C)Copyright 1990 - 2021, shwfed.com
@Desc    :   扩展的数字处理对象
"""

# here put the import lib
from decimal import Decimal


class ExtendDecimal(Decimal):
    """
    扩展货币对象
    """

    def __new__(cls, value: str, length: int = 0):
        """
        初始化方法

        :param value: 初始化值
        :param length: 小数位长度
        """
        cls.length = length
        return super().__new__(cls, value)

    def __str__(self):
        if self.length > 0:
            _f = '1.'.ljust(self.length + 2, '0')
            return str(self.quantize(Decimal(_f)))
        return str(self.quantize(Decimal('1.00')))

    def __repr__(self):
        if self.length > 0:
            _f = '1.'.ljust(self.length + 2, '0')
            return str(self.quantize(Decimal(_f)))
        return str(self.quantize(Decimal('1.00')))
