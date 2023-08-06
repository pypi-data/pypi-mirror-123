# 邮件组件

封装了邮件操作的组件，支持原生 **SMTP** 方式发送带有附件的邮件。但是由于不想引入额外的组件依赖，因此不支持添加网络 **URL** 的文件，仅支持服务器本地文件。同时，支持原生的 **POP** 收取邮件。

### 使用组件并初始化对象
```Python
from junglead import EmailUtil

_util = EmailUtil(smtp_server, smtp_port, smtp_user, smtp_passwd, pop_server='', pop_port=0)
```

仅发送邮件的话，不需要配置两个 **pop** 相关信息。

### 发送邮件
```Python
_r, _msg = _util.send([], _nickname, _subject, _content, cc=[], attach_files=[])
```

发送邮件，支持群发，以及抄送和附件。由于不依赖第三方组件，因此附件只能是本地文件的绝对路径，不支持网络路径。

### 接收邮件
```Python
# is_delete 表示是否删除邮件
_emails = _util.receive(_email, _auth_code, is_delete = False)
```
收取邮件的方法返回的是邮件对象 **EmailItem** 的列表，具体类型后附。收取邮件的授权密码，对于现在多数邮箱来说，**不是邮箱密码** ，而是在邮件系统设置中单独配置的授权令牌。

### 邮件对象
```Python
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
```

