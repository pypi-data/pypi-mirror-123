# 日志组件

日志组件用于在项目中，将一些重要的或者错误的信息，保存在本地日志中进行记录。日志默认保存在 **当前** 项目的 **logs/\<level\>.log** 文件中，例如： **logs/info.log** 。当 **logs** 组件不存在时，组件会自动创建。

```Python
# 导入组件
from junglead import LoggerUtil, LoggerLevel

# 默认为info级别，文件名为 ：info.log
LoggerUtil().logger.info('记录info级别的日志')

# 带有级别参数，保存在指定级别的文件中
LoggerUtil(LoggerLevel.ERROR).logger.error('记录error级别的日志')

# 带有级别及前缀参数
LoggerUtil(prefix='mq').logger.info('带有前缀的日志记录')
```

**LoggerUtil** 类包含几个重要，但可选的参数：
* level : 日志等级。如果不使用枚举类型传输，则默认为 LoggerLevel.INFO 级别；
* prefix : 日志前缀。由于一些项目中可能希望把不同目的的日志，存储在不同文件中，可以增加 **prefix** 参数来区别存储名称，日志名会变成类似：\<prefix\>-\<level\>.log 的形式，例如上面中的代码，就会存储为 ：**logs/mq-info.log**。

日志对象的 **logger** 实例的日志写入方法，必须和构造函数中保持一致，否则无法写入日志。例如：LoggerLevel.ERROR 对应 error 方法；LoggerLevel.INFO 对应 info 方法。**务必注意！**

