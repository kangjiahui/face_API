# -*- coding: utf-8 -*-
"""
   File Name：     logger_helper.py
   Description :  the python log system
   Author :       yuanfang
   date：         2020/11/03
"""

import datetime
import logging
import logging.config
import os

from config import system_log


class ServerLogger(object):

    def __init__(self, log_name):
        # 检查目录
        if not os.path.exists(system_log):
            os.makedirs(system_log)

        # 日志配置
        LOGGER_CONFIG_DICT = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'detailed_fmt': {
                    'class': 'logging.Formatter',
                    'format': '%(asctime)s %(created)s %(levelname)-6s %(name)-15s %(processName)s:%(threadName)s %(message)s'
                    #  human-readable  timestamp levelname logger_name  processname threadname  message
                },
                'simple_fmt': {
                    'class': 'logging.Formatter',
                    'format': '%(asctime)s %(levelname)-8s %(name)-15s %(message)s'
                    #  human-readable  levelname logger_name message
                },
                'portal_fmt': {
                    'class': 'logging.Formatter',
                    # 'datefmt': '%Y-%m-%d %H:%M:%S,uuu',  # 实际默认格式就是这个
                    'format': '%(asctime)s %(levelname)-8s %(name)-15s  %(processName)-10s %(message)s'
                },
                'system_fmt': {
                    'class': 'logging.Formatter',
                    'format': '%(asctime)s %(name)-15s %(levelname)-8s %(processName)-10s %(message)s'
                },
            },
            'handlers': {
                'file_size_rotate_hd': {
                    # 'class': 'logging.handlers.RotatingFileHandler',
                    'class': 'mrfh.MultiprocessRotatingFileHandler',  # 这里就是用到mrfh了。
                    'filename': system_log + '/{}-info-{}.log'.format(log_name, datetime.datetime.now().strftime("%Y-%m-%d")),  # 日志文件路径
                    'mode': 'a',
                    'maxBytes': 1024 * 1024 * 500,
                    'backupCount': 100,
                    'formatter': 'portal_fmt'
                },
                'errors_hd': {
                    'class': 'logging.FileHandler',
                    'filename': system_log + '/{}-error-{}.log'.format(log_name, datetime.datetime.now().strftime("%Y-%m-%d")),  # 日志文件路径
                    'formatter': 'detailed_fmt',
                    'level': 'ERROR'  # 只会错误40及以上的日志
                },
                'system_hd': {
                    'class': 'logging.FileHandler',
                    'filename': system_log + '/{}-sys-{}.log'.format(log_name, datetime.datetime.now().strftime("%Y-%m-%d")),  # 日志文件路径
                    'formatter': 'simple_fmt'
                }
            },
            'loggers': {
                'selfservices': {
                    'level': 'INFO',
                    'propagate': False,
                    'handlers': ['file_size_rotate_hd', 'errors_hd']
                },
            },
            'root': {
                'level': 'DEBUG',
                'handlers': ['file_size_rotate_hd', 'errors_hd']
            },
        }
        logging.config.dictConfig(LOGGER_CONFIG_DICT)
        self.logger = logging.getLogger(log_name)

    def get_logger(self):
        return self.logger
