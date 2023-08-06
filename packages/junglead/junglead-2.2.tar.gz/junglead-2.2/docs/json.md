# 序列化组件

**Python** 自带的 **json** 组件，仅支持序列化最基础的数字、字符串类型，对于稍微复杂点的类型均不提供支持。同时由于 **Python** 是弱语言类型，导致也无法像其他强类型语言一样根据反射机制来获取属性配置，从而对于过于复杂的对象类型，也无法做到通用的配置。因此只能封装几个比较简单的特殊类型。

### 使用方法
```Python
from junglead.model import ExtendDecimal, ExtendDatetime
from junglead import JsonEncoder

class SubDemo:
    def __init__(self, id: int = 1):
        self.id = id
        self.dt = ExtendDatetime.now(date_format='%Y%m%d')


class Demo:
    def __init__(self, dt: ExtendDatetime = None, dc: ExtendDecimal = None):
        self.dt = dt
        self.dc = dc
        self.sub_demo = SubDemo()

_origin = datetime(2021, 10, 1, 10, 0, 0)
_dt = ExtendDatetime.convert(_origin)
_dc = ExtendDecimal('0.1112345678', 6)
_demo = Demo(dt=_dt, dc=_dc)
print(json.dumps(_demo.__dict__, ensure_ascii=False, cls=JsonEncoder))

# 输出
{"dt": "2021-10-01 10:00:00", "dc": "0.111235", "sub_demo": "{\"id\": 1, \"dt\": \"20211012\"}"}
```

### 日期时间扩展
对于标准日期时间对象 **datetime** ，已经提供了格式为 ： 2021-10-10 10:00:00 的默认序列化输出。考虑到有时需要序列化为特殊格式，因此提供了封装的 **ExtendDatetime** 对象，用于实例化指定格式的日期时间对象。例如：
```Python
# 转换标准的日期时间对象为扩展类型
_dt1 = ExtendDatetime.convert(dt=datetime.now(), date_format='%Y%m')

# 获取当前时间，指定时区
_dt2 = ExtendDatetime.now(tz=timezone(timedelta(hours=8)), date_format='%Y%m')
```
扩展日期时间组件，不能直接实例化，需要用 **ExtendDatetime** 提供的静态方法转换。

### 货币类型扩展
对于标准货币对象 **Decimal** ，默认输出小数点后 **4** 位。针对于不同的小数位数需求，提供了封装的 **ExtendDecimal** 对象，用于根据给定的小数位数，序列化对象。例如：
```Python
_dc = ExtendDecimal('0.1112345678', 6)
```

### 通用类型
为了尽可能简化序列化操作，实际上 **JsonEncoder** 还是针对特殊类，给到了序列化方法。即针对不能识别的对象属性，如果对象包含了 \_\_dict\_\_ 属性，则将该属性进行序列化。但是不能保证适用于所有类的序列化。 