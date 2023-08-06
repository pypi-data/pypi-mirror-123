#!/usr/bin/env python
# -*- coding: utf-8 -*-
from logger.es_logger import EsLogger


class LoggerFactory:

    @staticmethod
    def get_logger(config, **kwargs):
        return EsLogger(config['host'], config['port'], config['index'],**kwargs)

