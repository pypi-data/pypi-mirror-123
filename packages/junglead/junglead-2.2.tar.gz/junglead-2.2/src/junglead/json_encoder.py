# -*- encoding: utf-8 -*-
"""
@File    :   json_encoder.py
@Time    :   2021/09/27 10:17:27
@Author  :   Gary.Wang
@Version :   1.0
@Contact :   wangyijun@shwfed.com
@License :   (C)Copyright 1990 - 2021, shwfed.com
@Desc    :   JSON自定义编码工具
"""

# here put the import lib
from datetime import datetime
from json import JSONEncoder
from decimal import Decimal
import json

from junglead.model import ExtendDatetime, ExtendDecimal


class JsonEncoder(JSONEncoder):

    def default(self, obj):
        """
        默认的转码方式
        """
        if obj is None or obj == '':
            return ''
        elif isinstance(obj, ExtendDatetime):
            return str(obj)
        elif isinstance(obj, ExtendDecimal):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, Decimal):
            return str(obj.quantize(Decimal('1.0000')))
        elif len(obj.__dict__) > 0:
            return json.dumps(obj.__dict__, ensure_ascii=False, cls=JsonEncoder)
        else:
            return JSONEncoder.default(self, obj)
