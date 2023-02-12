# -*- coding:utf-8 -*-
from data.settings.get_args import get_args
import requests
from getData.utils import writeJson
from bs4 import BeautifulSoup

from getData.UrlManager import UrlManager
import urllib.request
import urllib.parse

class SpiderMain(object):
    def __init__(self, rootSchool, jsonPath):
        '''
        参数: jsonPath 参数
        '''
        self.urlsManger = UrlManager(rootSchool, jsonPath)  # url管理初始化
        self.colleges = self.urlsManger.colleges
        self.dictUrls = self.urlsManger.collegeJson
        SpiderMain.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/51.0.2704.63 Safari/537.36'}
        pass

    @staticmethod
    def codeCollege(url):  # 从 url 解析出学院代码
        college = url[url.find('//'):url.find('.seu')][2:]
        return college

    @staticmethod
    def urlsCyber(headers, url):  # 网安院导师urls
        teacherUrls = []
        root = UrlManager.getRoot(url)
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req)
        html = res.read()
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup)
        class_a_tags = soup.select('.tc-ul')
        for tag in class_a_tags:
            link_tags = tag.select('a')
            for link_tag in link_tags:
                # print(root+link_tag['href'])
                teacherUrls.append(root+link_tag['href'])
        return teacherUrls

    @staticmethod
    def teacherUrls(url):  # html 解析
        headers = SpiderMain.headers
        code = SpiderMain.codeCollege(url)
        if(code == 'cyber'):
            teacherUrls = SpiderMain.urlsCyber(headers, url)
        return teacherUrls

    @staticmethod
    def getTeacher(url):
        headers = SpiderMain.headers
        code = SpiderMain.codeCollege(url)
        if(code == 'cyber'):
            teacher = SpiderMain.getCyberTeacher(headers, url)
        return teacher

    @staticmethod
    def getCyberTeacher(headers, url):
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req)
        html = res.read()
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup)
        name = ""  # 姓名
        age = ""  # 年龄
        gender = ""  # 性别
        college = ""  # 学院
        title = ""  # 职称
        des = ""  # 简介
        background = ""  # 教育背景
        direction = ""  # 研究方向
        award = ""  # 奖项
        mail = ""  # 邮箱
        tel = ""  # 电话
        try:
            class_message_tags = soup.select('.right_c')
        except:
            return 
        for _message in class_message_tags:
            # print(_message.text)
            if("姓名" in _message.text):
                name = _message.text[3:]
            elif('职称' in _message.text):
                title = _message.text[3:]
            elif('电话' in _message.text):
                tel = _message.text[3:]
            elif('邮箱' in _message.text):
                mail = _message.text[3:]
            elif('个人主页' in _message.text):
                des = _message.text[5:]
        
        class_tfather_tags = soup.select('.tfather')
        for _message in class_tfather_tags:
            if('教育背景' in _message.text):
                background = _message.text[6:]
            elif('研究领域' in _message.text):
                direction = _message.text[6:]
            elif('奖励与荣誉' in _message.text):
                award = _message.text[7:]
            # print(_message)

        teacher = dict(
            name = name,  # 姓名
            age = age,  # 年龄
            gender = gender,  # 性别
            college = college,  # 学院
            title = title,  # 职称
            des = des,  # 简介
            background = background,  # 教育背景
            direction = direction,  # 研究方向
            award = award,  # 奖项
            mail = mail,  # 邮箱
            tel = tel,  # 电话
        )
        return teacher

def craw():
    parser = get_args()
    jsonPath = parser.jsonCollege
    rootSchool = parser.schoolUrl
    spider = SpiderMain(rootSchool, jsonPath)
    for college in spider.colleges: # 迭代每个学院
        print(spider.dictUrls[college])
        url = spider.dictUrls[college]
        teacherUrls = SpiderMain.teacherUrls(url)
        dictTeachers = []
        for teacherUrl in teacherUrls:
            teacher = SpiderMain.getTeacher((teacherUrl))
            if(teacher == None):
                continue
            dictTeachers.append(teacher)
    writeJson(dictTeachers)



