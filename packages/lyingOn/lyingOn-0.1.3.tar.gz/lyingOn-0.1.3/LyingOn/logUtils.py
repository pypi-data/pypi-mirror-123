import logging
import os
from datetime import datetime

'''
@author lyingOn
@desc 日志工具类
@date 2021-09-17
'''


class LogUtils():
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    time = datetime.now()
    date = time.strftime('%Y-%m-%d')

    def __init__(self):
        self.create_txt()

    def setLog(self, level, handler):
        self.logger.setLevel(level)
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)

    def removeLog(self, handler):
        self.logger.removeHandler(handler)

    # 创建日志文件
    def create_txt(self):
        # 当前路径
        file_name = os.path.abspath(os.path.dirname(__file__)) + "\\log\\" + self.date + ".log"
        if not os.path.exists(file_name):
            # windows系统创建文件
            if os.name == "nt":
                fp = open(file_name, 'wb')
                fp.close()
            # unix/OS X系统创建文件
            else:
                os.mknod(file_name)

    # 根据日志类型写入日志
    # type 日志类型
    # msg 日志消息
    # exception 异常信息，只在warning、error、critical级别日志会打印
    def logging_msg(self, type, msg, exception):
        file_log = os.path.abspath(os.path.dirname(__file__)) + "\\log\\" + self.date + ".log"
        fileHandler = logging.FileHandler(file_log, mode='a', encoding='utf-8')
        if type == 'debug':
            self.setLog(logging.DEBUG, fileHandler)
            self.logger.debug(msg)
        elif type == "info":
            self.setLog(logging.INFO, fileHandler)
            self.logger.info(msg)
        elif type == "warning":
            self.setLog(logging.WARNING, fileHandler)
            self.logger.warning(msg + "\n" + exception)
        elif type == "error":
            self.setLog(logging.ERROR, fileHandler)
            self.logger.error(msg + "\n" + exception)
        elif type == "critical":
            self.setLog(logging.CRITICAL, fileHandler)
            self.logger.critical(msg + "\n" + exception)
        else:
            raise Exception("This log type is not supported,暂不支持此日志类型")
        self.removeLog(fileHandler)
