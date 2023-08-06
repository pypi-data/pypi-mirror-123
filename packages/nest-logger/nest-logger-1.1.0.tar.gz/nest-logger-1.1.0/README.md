

## Installation

install as **pip**

```shell
pip install nest-logger==1.1.0
```

## Usage

- 导包并进行赋值操作

  > :param path: 日志存储的路径,绝对路径, 必填
  >
  > :param level: 日志等级 ，默认info
  >
  > :param rotation: 每天几点新增日志, 默认 00:00分割日志
  >
  > :param retention: 日志保留最长时间, 默认7天
  >
  > :param compression: 日志压缩格式，默认zip
  >
  > :param traceback: 回溯日志, 默认True

  ```shell
  >>> from pylogger import logger
  >>> log = logger.logrecord("/var/logs/nest")
  ```

- 使用日志

  ```shell
  >>> log.info("this is info test")
  >>> log.debug("this is debug test")
  ```

