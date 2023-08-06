# 日期时间组件
日期时间组件根据底层 **datetime** 提供的一些类及方法封装了一些关于时区、时间的获取，日期时间比较及日期时间运算等操作方法。

引入组件的方法：
```Python
from junglead import DatetimeUtil
```

### 时区
时区是指服务器当前运行时间与UTC标准时间的时差，**Windows Server** 一般会忽视这个问题，直接根据网络时间获取。**Linux** 系统则一般要求显示配置时区。但是对于一些需要跨不同地区服务的系统来说，这就会有极大的问题。因此提供了两个方法来获取时区。
```Python
# 获取亚洲/上海 +8 时区
_tzinfo1 = DatetimeUtil.get_timezone_asia()
# 给定时差，返回对应的时区信息
_tzinfo2 = DatetimeUtil.get_timezone(1)
```

### 日期时间的比较
时间比较通常用于比较两个时间的大小，或者是否早于/晚于某个时间。
```Python
_tzinfo = DatetimeUtil.get_timezone_asia()
_dt1 = datetime(2021, 10, 1, 10, 0, 0, tzinfo=_tzinfo)
_dt2 = datetime(2025, 10, 18, 10, 0, 0, tzinfo=_tzinfo)
# 与当前时间做比较
print(DatetimeUtil.after_now(_dt1), DatetimeUtil.before_now(_dt1), DatetimeUtil.after_now(_dt2), DatetimeUtil.before_now(_dt2))
# 两个时间比较
print(DatetimeUtil.compare_date(_dt1, _dt2), DatetimeUtil.compare_date(_dt1, _dt1), DatetimeUtil.compare_date(_dt2, _dt1))

_dt1 = datetime(2021, 10, 1, 10, 0, 0)
_dt2 = datetime(2025, 10, 18, 10, 0, 0)
# 两个时间比较
print(DatetimeUtil.compare_date(_dt1, _dt2), DatetimeUtil.compare_date(_dt1, _dt1), DatetimeUtil.compare_date(_dt2, _dt1))
```
在日期时间比较中，请务必注意：

* 与当前日期时间比较，必须要用带有时区信息的对象比较，否则没有比较的意义，当然可以为当前时间指定不同的时区；
* 两个日期时间对象的比较，可以都包含时区，也可以都不包含时区，但是一个包含一个不包含则会没有意义，会抛出异常。

### 日期时间的计算
时间的计算，也是常用的功能。
```Python
_dt1 = datetime(2021, 10, 1, 10, 0, 0)
_dt2 = datetime(2021, 10, 2, 10, 0, 0)
# 计算日期时间差
print(DatetimeUtil.minus_datetime(_dt1, _dt2))
# 根据枚举对象增加
print(DatetimeUtil.plus_datetime(_dt2, 3, PlusFormat.DAY))
# 根据粒度化数值增加
print(DatetimeUtil.plus_datetime_material(_dt2, weeks=-1, days=1, hours=1, minutes=1))
# 无参数异常
print(DatetimeUtil.plus_datetime_material(_dt2))
```

* 与日期时间的比较相类似的一点，计算两个日期时间对象的差，要么都给时区，要么都不给时区，交叉时区会导致计算没有意义而抛出异常；
* 日期时间的增加，提供了枚举的单一添加和多参数添加的情况，并且均支持负值。枚举配置请见最后；
* 粒度化计算，至少需要传递一个添加纬度，否则会抛出异常。

### 日期时间转换
组件提供了从字符串以及时间戳转换为日期时间对象的方法。
```Python
# 从字符串转换
_dt1 = DatetimeUtil.convert_from_str('2021-10-01', '%Y-%m-%d')
_dt2 = DatetimeUtil.convert_from_str('2021-10-0110:01:01', '%Y-%m-%d%H:%M:%S')
# 从时间戳转换
_dt3 = DatetimeUtil.convert_from_timestamp(1634095098)
print(_dt1, _dt2, _dt3)
# 输出 ： 2021-10-01 00:00:00+08:00 2021-10-01 10:01:01+08:00 2021-10-13 11:18:18+07:00
```

* 从字符串转换时，无法自动识别字符串包含的格式，因此必须指定格式化字符串；
* 从时间戳转换，只支持10位的时间戳，13位会报错。

### 日期时间格式化输出
日期时间格式化，提供了日期时间的转换以及格式化输出的方法。
```Python
# 输出时间戳：1634098565592
print(f'输出时间戳：{DatetimeUtil.get_timestamp(13)}')
# 输出当前时间简单形式：20211013121649, 20211013121649083682
print(f'输出当前时间简单形式：{DatetimeUtil.get_current_simple_str(False)}, {DatetimeUtil.get_current_simple_str()}')
# 将指定日期输出为标准字符串：2021-10-01 10:01:01
print(f'将指定日期输出为标准字符串：{DatetimeUtil.to_standard_str(_dt2)}')
# 将指定日期输出为中文标准字符串：2021年10月01日 10时01分01秒{DatetimeUtil.to_Chinese_str(_dt2)}')print(DatetimeUtil.to_Chinese_str(_dt2))
```

* 时间戳是指格林威治时间1970年01月01日00时00分00秒(北京时间1970年01月01日08时00分00秒)起至现在的总秒数；
* 当前日期可以指定时区，以及是否包含毫秒。与时间戳完全不同，简单格式是指当前标准时间的简单化输出方式；


### 日期计算枚举对象
枚举对象 PlusFormat 包含4个属性：
* WEEK      : 周
* DAY         : 日
* HOUR     : 时
* MINUTE  : 分

### 关于日期时间格式化的符号定义
在 **Python** 中，**time** 类和 **datetime** 类均可以使用下面的绝大多数格式化符号进行输出。例如：
```Python
from datetime import datetime
import time
_dt = datetime.now()
print(_dt.strftime('%Y-%m-%d %H:%M:%S'), time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime()))
```

**strftime** 方法对于 **datetime** 来说是实例方法；对于 **time** 来说是静态方法。注意区分。

* %y 两位数的年份表示（00-99）
* %Y 四位数的年份表示（000-9999）
* %m 月份（01-12）
* %d 月内中的一天（0-31）
* %H 24小时制小时数（0-23）
* %I 12小时制小时数（01-12）
* %M 分钟数（00=59）
* %S 秒（00-59）
* %a 本地简化星期名称
* %A 本地完整星期名称
* %b 本地简化的月份名称
* %B 本地完整的月份名称
* %c 本地相应的日期表示和时间表示
* %j 年内的一天（001-366）
* %p 本地A.M.或P.M.的等价符
* %U 一年中的星期数（00-53）星期天为星期的开始
* %w 星期（0-6），星期天为星期的开始
* %W 一年中的星期数（00-53）星期一为星期的开始
* %x 本地相应的日期表示
* %X 本地相应的时间表示
* %Z 当前时区的名称 （datetime实例不支持）
* %% %号本身