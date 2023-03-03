#!/usr/bin/env python3
# coding: utf-8
# File: question_classifier.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

import os
import ahocorasick

class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        # 特征词路径
        self.teacher_path = os.path.join(cur_dir, 'data/dict/teacher.txt')
        self.college_path = os.path.join(cur_dir, 'data/dict/college.txt')
        self.direction_path = os.path.join(cur_dir, 'data/dict/direction.txt')
        self.title_path = os.path.join(cur_dir, 'data/dict/title.txt')
        self.deny_path = os.path.join(cur_dir, 'data/dict/deny.txt') # 语义词
        # 特征词提取
        self.teacher_wds = [i.strip() for i in open(self.teacher_path,encoding='utf-8') if i.strip()]
        self.college_wds = [i.strip() for i in open(self.college_path,encoding='utf-8') if i.strip()]
        self.direction_wds = [i.strip() for i in open(self.direction_path,encoding='utf-8') if i.strip()]
        self.title_wds = [i.strip() for i in open(self.title_path,encoding='utf-8') if i.strip()]
        self.deny_words = [i.strip() for i in open(self.deny_path,encoding='utf-8') if i.strip()]
        self.region_words = set(self.teacher_wds + self.college_wds + self.direction_wds + self.title_wds)  # 搜索词
        pass
        # 构建领域ACTREE
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句疑问句
        self.college_qwd = ['学院', '院系', '专业']  # 所属学院
        self.title_qwd = ['职称', '教授']  # 所属职称
        self.background_qwd = ['学术背景', '毕业于']  # 学术背景
        self.direction_qwd = ['研究方向', '研究内容']  # 研究方向
        self.award_qwd = ['奖项', '荣誉']  # 奖项
        self.email_qwd = ['邮箱', '联系方式', '联络方式', 'email', 'e-mail']  # 邮箱
        self.tel_qwd = ['电话', '联系方式', '联络方式', 'tel']  # 电话
        print('model init finished ......')

    def build_wdtype_dict(self):  # 构造词对应的类型
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.teacher_wds:
                wd_dict[wd].append('teacher')
            if wd in self.college_wds:
                wd_dict[wd].append('college')
            if wd in self.direction_wds:
                wd_dict[wd].append('direction')
            if wd in self.title_wds:
                wd_dict[wd].append('title')
        return wd_dict

    def build_actree(self, wordlist):  # 构造actree，加速过滤
        actree = ahocorasick.Automaton()         # 初始化trie树
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))     # 向trie树中添加单词
        actree.make_automaton()    # 将trie树转化为Aho-Corasick自动机
        return actree


    def classify(self, question):  # 分类主函数
        data = {}
        teacher_dict = self.check_teacher(question)
        if not teacher_dict:
            if 'teacher_dict' in globals():  # 判断是否为首次作用
                pass
            else:
                return {}
        print("medical_dict:", teacher_dict)
        data['args'] = teacher_dict
        # 收集问句涉及实体类型
        types = []  # 实体类型
        for _type in teacher_dict.values():
            types += _type
        
        question_types = []  # 问句类型

        # 学院
        if self.check_words(self.college_qwd, question) and ('teacher' in types):
            question_type = 'teacher_college'
            question_types.append(question_type)
        
        # 学术背景
        if self.check_words(self.direction_qwd, question) and ('teacher' in types):
            question_type = 'teacher_background'
            question_types.append(question_type)
        
        # 奖项
        if self.check_words(self.award_qwd, question) and ('teacher' in types):
            question_type = 'teacher_award'
            question_types.append(question_type)
        
        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types
        return data

    def check_teacher(self, question):  # 问句过滤
        region_wds = []
        for i in self.region_tree.iter(question):   # ahocorasick库 匹配问题  iter返回一个元组，i的形式如(3, (23192, '乙肝'))
            wd = i[1][1]      # 匹配到的词
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)       # stop_wds取重复的短的词，如region_wds=['乙肝', '肝硬化', '硬化']，则stop_wds=['硬化']
        final_wds = [i for i in region_wds if i not in stop_wds]     # final_wds取长词
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}  # 获取词和词所对应的实体类型
        global teachers_dict
        if final_dict:
            teachers_dict = final_dict
        print("final_dict : ",final_dict)
        if 'teachers_dict' in globals():
            print("teachers_dict : ",teachers_dict)
        else:
            print("teachers_dict does not exist.")
        return final_dict
    
    def check_words(self, wds, question):  # 基于特征词进行分类
        for wd in wds:
            if wd in question:
                return True
        return False