# -*- encoding: utf-8 -*-
"""
@File    :   email_util.py
@Time    :   2021/09/24 15:47:47
@Author  :   Gary.Wang
@Version :   1.0
@Contact :   wangyijun@shwfed.com
@License :   (C)Copyright 1990 - 2021, shwfed.com
@Desc    :   邮件发送帮助工具
"""

# here put the import lib
from email.utils import formatdate, make_msgid, formataddr
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.header import decode_header, Header
from email.mime.text import MIMEText
from email.utils import parseaddr
from email.message import Message
from email.parser import Parser
from os import path
import smtplib
import poplib

from junglead.logger_util import LoggerUtil as logger_util
from junglead.regex_util import RegexUtil


class EmailAttachmentItem:
    """
    邮件附件对象
    """
    def __init__(self, filename: str, content_type: str, data: str):
        """
        构造函数

        :param filename: 文件名
        :param content_type: 文件类型
        :param data: 数据内容，BASE64格式
        """
        self.filename = filename
        self.content_type = content_type
        self.data = data


class EmailItem:
    """
    邮件条目对象
    """
    def __init__(self, from_address: str = '', nickname: str = '', to_address: str = '', subject: str = ''):
        """
        构造函数

        :param from_address: 发件人邮箱
        :param nickname: 发件人称呼
        :param to_address: 收件人邮箱
        :param subject: 邮件主题
        """
        self.from_address = from_address
        self.nickname = nickname
        self.to_address = to_address
        self.subject = subject
        # 附件列表
        self.attachment = []


class EmailUtil:
    """
    电子邮件工具

    :param smtp_server: SMTP服务器地址
    :param smtp_port: SMTP服务器端口
    :param smtp_user: SMTP登录用户
    :param smtp_passwd: SMTP登录密码
    """

    def __get_content_from_uri(self, uri: str):
        """
        读取文件内容

        :param uri 统一资源定位符

        :return 返回获取到的二进制内容
        """
        content = None
        with open(uri, 'rb') as tf:
            content = tf.read()
        return content

    def __attach_file(self, files: list):
        """
        附加文件
        """
        result = []
        if files is not None and len(files) > 0:
            for _file in files:
                _file_content = self.__get_content_from_uri(_file)
                if _file_content is not None:
                    _part_file = MIMEApplication(_file_content)
                    _part_file.add_header('Content-Disposition', 'attachment', filename=path.split(_file)[-1])
                    result.append(_part_file)
        return result

    def __convert_email_content(self, msg: Message, email_item: EmailItem = None, indent=0):
        """
        转换邮件内容

        :param msg: 消息对象
        :param email_item: 递归解析的邮件对象

        :return EmailItem, 返回邮件解析后的对象
        """
        if email_item is None:
            email_item = EmailItem()
        # 为0表示主内容
        if indent == 0:
            for header in ['From', 'To', 'Subject']:
                value = msg.get(header, '')
                if value:
                    if header == 'Subject':
                        value = self._decode_str(value)
                        email_item.subject = value
                    else:
                        hdr, addr = parseaddr(value)
                        name = self._decode_str(hdr)
                        if header == 'From':
                            email_item.from_address = addr
                            email_item.nickname = name
                        else:
                            email_item.to_address = addr
        else:
            # 叠加内容，增加属性
            pass
        # 获取内容
        if (msg.is_multipart()):
            # 多级内容的获取
            parts = msg.get_payload()
            for _n, _part in enumerate(parts):
                self.__convert_email_content(_part, email_item, indent + 1)
        else:
            content_type = msg.get_content_type()
            if content_type == 'text/plain' or content_type == 'text/html':
                content = msg.get_payload(decode=True)
                charset = self._guess_charset(msg)
                if charset:
                    content = content.decode(charset)
                email_item.content = content
            else:
                content_disposition = msg.get_content_disposition()
                value1 = msg.get('Content-Disposition', '')
                if value1 != '':
                    _dispositions = content_disposition.strip().split(";")
                    if _dispositions[0].lower() == 'attachment':
                        attach_data = msg.get_payload(decode=True)
                        attach_content_type = msg.get_content_type()
                        attach_name = self._decode_str(msg.get_filename())
                        email_item.attachment.append(EmailAttachmentItem(attach_name, attach_content_type, attach_data))
                        # attach_size = len(attach_data)
        return email_item

    def _decode_str(self, s: str):
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value

    def _guess_charset(self, msg: Message):
        charset = msg.get_charset()
        if charset is None:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset

    def __init__(self, smtp_server: str, smtp_port: int, smtp_user: str, smtp_passwd: str, pop_server: str = '', pop_port: int = 25):
        """
        构造函数

        :param smtp_server: SMTP服务器地址
        :param smtp_port: SMTP服务器端口
        :param smtp_user: SMTP登录用户
        :param smtp_passwd: SMTP登录密码
        :param pop_server: POP服务器地址
        """
        self.__smtp_server = smtp_server
        self.__smtp_port = smtp_port
        self.__smtp_user = smtp_user
        self.__smtp_passwd = smtp_passwd

        self.__pop_server = pop_server
        self.__pop_port = pop_port

    def send(self, recipients: list, sender_nickname: str, subject: str, content: str, cc: list = [], attach_files: list = []):
        """
        发送邮件

        :param recipients: 收件人列表，必须每个邮箱格式都正确，否则会直接返回错误
        :param sender_nickname: 发件人的称呼
        :param subject: 邮件主题
        :param content: 邮件内容

        :param cc: 抄送人列表；选填项，如果输入，则必须全部格式正确
        :param attach_files: 附件列表；选填项，仅支持本地文件
        :return bool, 返回发送结果
        """
        if recipients is None or len(recipients) == 0 or not RegexUtil.is_all_email(recipients):
            return False, '收件人列表中有错误的邮箱格式'
        if cc is not None and len(cc) > 0 and not RegexUtil.is_all_email(cc):
            return False, '如果输入了抄送人信息，则必须全部格式正确'
        message = MIMEMultipart('alternative')
        message['Subject'] = Header(subject, 'utf-8')
        message['From'] = formataddr((Header(sender_nickname, 'utf-8').encode(), self.__smtp_user))
        message['To'] = ', '.join(recipients)
        message['Message-id'] = make_msgid()
        message['Date'] = formatdate()
        # 1.如果有抄送人，添加抄送人
        if cc is not None and len(cc) > 0:
            message['Cc'] = ', '.join(cc)

        # 2.增加文本内容
        _part_content = MIMEText(content, 'html', 'utf-8')
        message.attach(_part_content)

        # 3.增加附件内容
        if attach_files is not None and len(attach_files) > 0:
            _part_attachfiles = self.__attach_file(attach_files)
            if _part_attachfiles is not None and len(_part_attachfiles) > 0:
                for _part_attachfile in _part_attachfiles:
                    message.attach(_part_attachfile)

        try:
            server = smtplib.SMTP()
            server.connect(self.__smtp_server, self.__smtp_port)
            server.set_debuglevel(0)
            server.login(self.__smtp_user, self.__smtp_passwd)
            server.sendmail(from_addr=self.__smtp_user, to_addrs=recipients, msg=message.as_string())
            server.quit()
            return True, 'OK'
        except smtplib.SMTPConnectError as e:
            logger_util.error(f'邮件发送失败，连接失败:{e.smtp_code}，{e.smtp_error}')
        except smtplib.SMTPAuthenticationError as e:
            logger_util.error(f'邮件发送失败，认证错误:{e.smtp_code}，{e.smtp_error}')
        except smtplib.SMTPSenderRefused as e:
            logger_util.error(f'邮件发送失败，发件人被拒绝:{e.smtp_code}，{e.smtp_error}')
        except smtplib.SMTPRecipientsRefused as e:
            logger_util.error(f'邮件发送失败，收件人被拒绝:{e.smtp_code}，{e.smtp_error}')
        except smtplib.SMTPDataError as e:
            logger_util.error(f'邮件发送失败，数据接收拒绝:{e.smtp_code}，{e.smtp_error}')
        except smtplib.SMTPException as e:
            logger_util.error(f'邮件发送失败:{e.smtp_code}，{e.smtp_error}')
        except Exception as ex:
            logger_util.error(f'邮件发送失败: {ex}')
        return False, '邮件发送发生系统错误，请联系管理员！'

    def receive(self, email: str, auth_code: str, is_delete: bool = False):
        """
        接收邮件

        :param email: POP账户
        :param auth_code: 授权码。多数邮箱均已不支持密码登录，这里是单独生成的授权码
        :param is_delete: 是否删除已经拉取的文件

        :return list, 返回
        """
        _server = poplib.POP3_SSL(self.__pop_server, self.__pop_port)
        _server.user(email)
        _server.pass_(auth_code)
        # b'+OK', 邮件id列表，25
        _resp, _mails, _octets = _server.list()
        _emails = []
        # 索引从 1 开始
        for _index in range(1, len(_mails) + 1):
            # b'+OK 7528'， 邮件每一行列表，邮件编号
            _resp, _lines, _octets = _server.retr(_index)
            # 直接编码会引发错误
            _msg_content = b'\r\n'.join(_lines).decode('utf-8', errors="replace")
            # 解析后的文本还是无法处理的信息
            _msg = Parser().parsestr(_msg_content)
            _emails.append(self.__convert_email_content(_msg))
            # 转换并添加
            if is_delete:
                _server.dele(_index)
        _server.quit()
        return _emails
