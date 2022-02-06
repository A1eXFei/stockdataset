# -*- coding: UTF-8 -*-
import logging


class BaseInfo:
    def __init__(self, engine):
        self.logger = logging.getLogger("appLogger")
        self.engine = engine
