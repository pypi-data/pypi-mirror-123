# -*- encoding: utf-8 -*-
"""
@File    :   regex_util.py
@Time    :   2021/01/21 10:41:13
@Author  :   Gary.Wang
@Version :   1.0
@Contact :   wangyijun@shwfed.com
@License :   (C)Copyright 1990 - 2020, shwfed.com
@Desc    :   正则表达式工具
"""

# here put the import lib
import re


class RegexUtil:
    """
    正则表达式工具
    """

    @staticmethod
    def is_email(email: str):
        """
        是否邮箱

        :param email: 电子邮箱字符串

        :return bool, 返回检查结果
        """
        if email is None or email == '':
            return False
        elif not isinstance(email, str):
            return False
        elif len(email) > 100:
            return False
        _pattern = r"^[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?$"
        return re.match(_pattern, email) is not None

    @staticmethod
    def is_all_email(emails: list):
        """
        是否邮箱列表

        :param emails: 电子邮箱字符串列表

        :return tuple, 返回检查结果，只要有一个元素格式错误，也返回错误
        """
        if emails is None or len(emails) == 0:
            return False, '列表为空'
        _flag = True
        _i = 1
        _err = []
        for _email in emails:
            if not RegexUtil.is_email(_email):
                _flag = False
                _err.append(str(_i))
            _i += 1
        if _flag:
            return True, 'OK'
        else:
            return False, f'列表中的第：{",".join(_err)} 个元素格式错误'

    @staticmethod
    def is_mobile(mobile: str):
        """
        是否手机号

        :param mobile: 手机号码字符串

        :return bool, 返回检查结果
        """
        if mobile is None or mobile == '':
            return False
        _pattern = '^(13[0-9]|14[5|7]|15[0|1|2|3|4|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\\d{8}$'
        return re.match(_pattern, mobile) is not None

    @staticmethod
    def is_idcard(idcard: str):
        """
        是否身份证号，支持15和18位

        :param idcard: 身份证号字符串

        :return bool, 返回检查结果
        """
        if idcard is None or idcard == '':
            return False
        _pattern = '(^\\d{15}$)|(^\\d{18}$)|(^\\d{17}(\\d|X|x)$)'
        return re.match(_pattern, idcard) is not None

    @staticmethod
    def is_zipcode(zipcode: str):
        """
        是否邮政编码

        :param zipcode: 邮政编码

        :return bool, 返回检查结果
        """
        if zipcode is None or zipcode == '':
            return False
        _pattern = '^[1-9]\\d{5}(?!\\d)$'
        return re.match(_pattern, zipcode) is not None

    @staticmethod
    def is_ip(ip: str):
        """
        是否IPv4版本

        :param ip: 身份证号字符串

        :return bool, 返回检查结果
        """
        if ip is None or ip == '':
            return False
        _pattern = '^((2(5[0-5]|[0-4]\\d))|[0-1]?\\d{1,2})(\\.((2(5[0-5]|[0-4]\\d))|[0-1]?\\d{1,2})){3}$'
        return re.match(_pattern, ip) is not None

    @staticmethod
    def is_account(account: str, min_length: int = 2, max_length: int = 40):
        """
        是否帐号，支持中文，大小写字母和下划线

        :param account: 账户文本信息
        :param min: 要求最小长度
        :param max: 要求最大长度

        :return bool, 返回检查结果
        """
        if account is None or account == '':
            return False
        elif min_length < 2 and max_length > 40:
            return False
        _pattern = f'^[a-zA-Z0-9_\\u4e00-\\u9fa5]{{{min_length},{max_length}}}$'
        return re.match(_pattern, account) is not None

    @staticmethod
    def is_strong_passwd(password: str, min_length: int = 5, max_length: int = 40):
        """
        是否强壮密码，必须包含大小写字母、数字和特殊符号

        :param password: 账户文本信息
        :param min: 要求最小长度
        :param max: 要求最大长度

        :return bool, 返回检查结果
        """
        if password is None or password == '':
            return False
        elif min_length < 5 and max_length > 40:
            return False
        _pattern = f'^(?=(.*[a-z]))(?=(.*[A-Z]))(?=.*[0-9])[A-Za-z0-9\\!@\\#\\$\\%&\\^\\,\\.\\*\\(\\)]{{{min_length},{max_length}}}$'
        return re.match(_pattern, password) is not None

    @staticmethod
    def is_tax_number(tax_number: str):
        """
        判断给到的字符串是否中国的企业税号
        """
        if tax_number is None or tax_number == '':
            return False
        _pattern = r"^[1-9](([\dA-Z]{14})|([\dA-Z]{17}))$"
        return re.match(_pattern, tax_number) is not None

    @staticmethod
    def is_integer(data: str):
        if data is None or data == '':
            return False
        _pattern = r"^-?[1-9]\d*$"
        return re.match(_pattern, data) is not None

    @staticmethod
    def is_float(data: str):
        if data is None or data == '':
            return False
        _pattern = r"^-?(([1-9]\d*)|(0))\.\d*((e?\-?\d+))$"
        return re.match(_pattern, data) is not None

    @staticmethod
    def is_qq(qq: str):
        """
        判断给到的字符串是否QQ号码

        :param qq: 号码的文本信息

        :return bool, 返回判断结果
        """
        if qq is None or qq == '':
            return False
        _pattern = r"^[1-9][0-9]{4,}$"
        return re.match(_pattern, qq) is not None

    @staticmethod
    def id_date(dt: str):
        """
        判断给到的字符串是否日期格式，允许YYYYMMDD 和 YYYY-MM-DD两种格式

        :param dt: 字符串

        :return bool, 返回检查结果
        """
        if dt is None or dt == '':
            return False
        _pattern = r"^[1|2]\d{3}-?((0[1-9]{1})|(1[012]))-?((0[1-9]{1})|([12]{1}[0-9]{1})|3[01])$"
        return re.match(_pattern, dt) is not None

    @staticmethod
    def id_simple_date(dt: str):
        """
        判断给到的字符串是否 YYYYMM 的简单日期类型

        :param dt: 字符串

        :return bool, 返回检查结果
        """
        if dt is None or dt == '':
            return False
        _pattern = r"^[1|2]\d{3}((0[1-9]{1})|(1[012]))$"
        return re.match(_pattern, dt) is not None

    @staticmethod
    def is_ansi(content: str):
        """
        判断文本内容是否仅ANSI字符

        :param content: 文本内容

        :return bool, 返回检查结果
        """
        if content is None or content == '':
            return False
        _pattern = r'^[\u4e00-\u9fa5<>\?a-zA-Z0-9"\s=\./\*()-:、，（）\#\?]*$'
        return re.match(_pattern, content) is not None
