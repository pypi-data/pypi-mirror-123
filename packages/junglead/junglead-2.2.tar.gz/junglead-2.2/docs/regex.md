# 正则表达式组件

正则表达式具备强大的文本搜索功能，比较常用的一般是判断文本格式，由于内容比较难于记忆，并且具有一定的通用性，因此组件封装了一些常见的正则校验方法，均已： **is\_** 开头。

组件提供了一些静态方法，用于对字符串进行格式验证。


```Python
from junglead import RegexUtil

# 判断字符串是否为电子邮件格式
RegexUtil.is_email(_email)

# 判断字符串列表是否为电子邮件格式，只要有一个错误，即返回错误，即具体的错误文本位置
RegexUtil.is_all_email(_emails)

# 是否国内11位的手机号码
RegexUtil.is_mobile(_mobile)

# 是否国内6位的邮政编码
RegexUtil.is_zipcode(_zipcode)

# 是否身份证号码
RegexUtil.is_idcard(_idcard)

# 是否标准账户
RegexUtil.is_account(_idcard, min_length = 2, max_length = 40)

# 是否强壮密码
RegexUtil.is_strong_passwd(_password, min_length = 5, max_length = 40)

# 是否税号
RegexUtil.is_tax_number(_tax_number)

# 是否整数
RegexUtil.is_integer(_str_int)

# 是否浮点类型
RegexUtil.is_float(_str_float)

# 是否日期
RegexUtil.is_date(_date)
```

所有的正则验证，均基于目前通用的使用习惯。例如：
* 电子邮件不允许超过100个字符
* 手机号只支持国内的11位手机号码
* 账户名称允许中文、大小写字母、数字和下划线
* 强密码要求大小写字母、数字、若干特殊字符
* 税号支持国内15-18位的税号
* 浮点判断允许科学记数法
* 日期判断，仅支持标准的 ： YYYY-MM-DD形式的日期文本