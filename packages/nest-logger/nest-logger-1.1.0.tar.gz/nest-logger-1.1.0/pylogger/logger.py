from loguru import logger


def logrecord(path="./", level='info', rotation='00:00', retention='7 days', compression='zip', traceback=True):
    '''
    :param path: 日志存储的路径,绝对路径
    :param level: 日志等级 ，默认info
    :param rotation: 每天几点新增日志, 默认 00:00分割日志
    :param retention: 日志保留最长时间, 默认7天
    :param compression: 日志压缩格式，默认zip
    :param traceback: 回溯日志, 默认True
    :return: 日志句柄
    '''
    # 日志等级大小写
    level = level.lower()
    # 等级列表
    level_config = ["debug", "info", "warning", "error"]
    # 判断level是否在等级列表中
    if level not in level_config: level = "info"
    # 需要打印的等级列表
    start = level_config.index(level)
    level_list = level_config[start:]
    # 删除日志流
    logger.remove()
    # 保存文件路径
    path = path.rstrip("/").rstrip("\\")
    # 添加日志等级记录
    for lev in level_list:
        logger.add(
            "%s/%s-{time:YYYYMMDD}.log" % (path, lev),
            rotation=rotation,
            retention=retention,
            level=lev.upper(),
            backtrace=traceback,
            compression=compression,
            encoding='utf-8',
            diagnose=True,
            enqueue=True
        )
    # 返回日志等级
    return logger
