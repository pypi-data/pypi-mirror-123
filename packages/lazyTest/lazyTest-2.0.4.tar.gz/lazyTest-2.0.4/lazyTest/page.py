# -*- coding = UTF-8 -*-
# Author   : buxiubuzhi
# Project  : lazyTest
# FileName : page.py
# Describe :
# ---------------------------------------

import logging

import lazyTest
from lazyTest.file import *
from lazyTest.base import *


class Page(object):

    __configFile = "\\pytest.ini"

    __section = "pytest"

    def __init__(self, driver: WebOption):
        self.driver = driver
        self.lazyLog = logging.getLogger(self.getClassName())
        self.config = lazyTest.ReadIni(self.GetProjectPath() + self.__configFile)
        self.lazyLog.info(
            "元素文件: -> %s" % (
                    self.GetProjectPath() + self.__getFilePath() + self.getClassName() + self.__getSuffix()
            )
        )
        self.source = GetElementSource(
            self.GetProjectPath() + self.__getFilePath() + self.getClassName() + self.__getSuffix()
        )

    def __getFilePath(self):
        return self.config.GetIniConfig(self.__section, "elementPath")

    def __getSuffix(self):
        return self.config.GetIniConfig(self.__section, "suffix")

    def GetElement(self, key: str):
        return self.source.GetElement(key).Element

    def GetProjectPath(self) -> str: ...

    @classmethod
    def getClassName(cls):
        return cls.__name__
