# -*- encoding: utf-8 -*-
"""
@File    :   __init__.py
@Time    :   2021/09/27 13:52:03
@Author  :   Gary.Wang
@Version :   1.0
@Contact :   wangyijun@shwfed.com
@License :   (C)Copyright 1990 - 2021, shwfed.com
@Desc    :   自定义模型包声明文件
"""

# here put the import lib
from junglead.model.extend_datetime import ExtendDatetime
from junglead.model.extend_decimal import ExtendDecimal


__all__ = [ExtendDatetime, ExtendDecimal]
