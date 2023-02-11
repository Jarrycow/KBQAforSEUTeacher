# -*- coding:utf-8 -*-
import re

from getData.utils import readJson

from data.settings.get_args import get_args

class UrlManager(object):
    def __init__(self, rootSchool, jsonPath):
        UrlManager.collegeJson = readJson(jsonPath)  # 学院Json
        UrlManager.schoolRoot = rootSchool  # 学校根目录
        self.colleges = UrlManager.collegeJson.keys()
    
    @staticmethod
    def getRoot(url): # 返回根目录
        '''
        参数：
        - url: 输入url
        返回：
        '''
        school = UrlManager.schoolRoot  # 学校根目录
        iSchool = url.find(school)
        return url[:iSchool+len(school)]
    
    