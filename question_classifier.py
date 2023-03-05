import os
import re
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
        self.college_qwd = ['学院', '院系', '专业', '院的']  # 所属学院
        self.title_qwd = ['职称', '教授']  # 所属职称
        self.gender_qwd = ['性别', '男', '女']  # 性别
        self.background_qwd = ['学术背景', '毕业于', '就读于', '学历']  # 学术背景
        self.direction_qwd = ['研究方向', '研究内容', '研究', '专攻']  # 研究方向
        self.award_qwd = ['奖', '荣誉']  # 奖项
        self.email_qwd = ['邮箱', '联系方式', '联络方式', 'email', 'e-mail']  # 邮箱
        self.tel_qwd = ['电话', '联系方式', '联络方式', 'tel']  # 电话
        self.des_qwd = ['介绍', '简介', '如何']
        self.www_qwd = ['哪些']

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
                teacher_dict = globals()['teachers_dict']
        # print("medical_dict:", teacher_dict)
        data['args'] = teacher_dict
        # 收集问句涉及实体类型
        types = []  # 实体类型
        for _type in teacher_dict.values():
            types += _type
        
        question_types = []  # 问句类型

        # 描述
        if self.check_words(self.des_qwd, question) and ('teacher' in types):
            question_type = 'teacher_describe'
            question_types.append(question_type)

        # 性别
        if self.check_words(self.gender_qwd, question) and ('teacher' in types):
            question_type = 'teacher_gender'
            question_types.append(question_type)

        # 学院
        if self.check_words(self.college_qwd, question) and ('teacher' in types):
            question_type = 'teacher_college'
            question_types.append(question_type)
        
        # 学术背景
        if self.check_words(self.background_qwd, question) and ('teacher' in types):
            question_type = 'teacher_background'
            question_types.append(question_type)
        
        # 奖项
        if self.check_words(self.award_qwd, question) and ('teacher' in types):
            question_type = 'teacher_award'
            question_types.append(question_type)

        # 职称
        if self.check_words(self.title_qwd, question) and ('teacher' in types):
            question_type = 'teacher_title'
            question_types.append(question_type)

        # 研究方向
        if self.check_words(self.direction_qwd, question) and ('teacher' in types):
            question_type = 'teacher_direction'
            question_types.append(question_type)

        # 邮箱
        if self.check_words(self.email_qwd, question) and ('teacher' in types):  
            question_type = 'teacher_mail'
            question_types.append(question_type)
        
        # 电话
        if self.check_words(self.tel_qwd, question) and ('teacher' in types):
            question_type = 'teacher_tel'
            question_types.append(question_type)
        
        # 哪些
        if self.check_words(self.www_qwd, question) and ('teacher' not in types):
            question_type = 'teacher_search'
            if(self.check_words(self.direction_qwd, question)):
                question_type += 'direction'
            if(self.check_words(self.college_qwd, question)):
                question_type += 'college'
            if(self.check_words(self.title_qwd, question)):
                question_type += 'title'
            question_types.append(question_type)

        # 没有类型
        if question_types == []:  
            teachersEntity = '和'.join([i for i in teacher_dict.keys()])
            try:
                question_types.append(self.compareSiliarity(teachersEntity, question))
            except:
                if question_types == []:
                    question_types.append('teacher_describe')
        
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
        # print("final_dict : ",final_dict)
        if 'teachers_dict' in globals():
            # print("teachers_dict : ",teachers_dict)
            pass
        else:
            pass
            # print("teachers_dict does not exist.")
        return final_dict
    
    def check_words(self, wds, question):  # 基于特征词进行分类
        for wd in wds:
            if wd in question:
                return True
        return False

    def sentenceSplit(self, sent):
        sentences = re.split(r'[;；,，。\.]\s*',sent)
        return sentences
    
    def compareSiliarity(teachersEntity, question):
        from question_similarity import vector_similarity
        if teachersEntity not in question:  # 没有主语
            question = teachersEntity + question
        exSentences = [
            teachersEntity + '属于哪个学院？', 
            teachersEntity + '的学院是？', 
            teachersEntity + '属于哪个院系？', 
            teachersEntity + '的院系是？', 
            teachersEntity + '属于哪个专业？', 
            teachersEntity + '的专业是？', 
            teachersEntity + '是哪个院的？', 
            teachersEntity + '是哪个院系的？', 
            teachersEntity + '是哪个专业的？', 
            teachersEntity + '是哪个学院的？', 
            teachersEntity + '的职称是？', 
            teachersEntity + '性别是？', 
            teachersEntity + '是男的吗？', 
            teachersEntity + '是女的吗？', 
            teachersEntity + '的学术背景是？', 
            teachersEntity + '毕业于？', 
            teachersEntity + '就读于？', 
            teachersEntity + '学历？', 
            teachersEntity + '研究方向是？', 
            teachersEntity + '研究内容是？', 
            teachersEntity + '专攻于？', 
            teachersEntity + '得过什么奖？', 
            teachersEntity + '获得什么荣誉？', 
            teachersEntity + '的邮箱是？', 
            teachersEntity + '的联系方式是？', 
            teachersEntity + '的联络方式是？', 
            teachersEntity + '的email', 
            teachersEntity + '电话是？', 
            teachersEntity + 'tel是', 
            teachersEntity + '如何联系？', 
            teachersEntity + '介绍一下', 
            teachersEntity + '的简介', 
            teachersEntity + '如何'
        ]
        dictSentences = {
            teachersEntity + '属于哪个学院？': 'teacher_college', 
            teachersEntity + '的学院是？': 'teacher_college', 
            teachersEntity + '属于哪个院系？': 'teacher_college', 
            teachersEntity + '的院系是？': 'teacher_college', 
            teachersEntity + '属于哪个专业？': 'teacher_college', 
            teachersEntity + '的专业是？': 'teacher_college', 
            teachersEntity + '是哪个院的？': 'teacher_college', 
            teachersEntity + '是哪个院系的？': 'teacher_college', 
            teachersEntity + '是哪个专业的？': 'teacher_college', 
            teachersEntity + '是哪个学院的？': 'teacher_college', 
            teachersEntity + '的职称是？': 'teacher_title', 
            teachersEntity + '性别是？': 'teacher_gender', 
            teachersEntity + '是男的吗？': 'teacher_gender', 
            teachersEntity + '是女的吗？': 'teacher_gender', 
            teachersEntity + '的学术背景是？': 'teacher_background', 
            teachersEntity + '毕业于？': 'teacher_background', 
            teachersEntity + '就读于？': 'teacher_background', 
            teachersEntity + '学历？': 'teacher_background', 
            teachersEntity + '研究方向是？': 'teacher_direction', 
            teachersEntity + '研究内容是？': 'teacher_direction', 
            teachersEntity + '专攻于？': 'teacher_direction', 
            teachersEntity + '得过什么奖？': 'teacher_award', 
            teachersEntity + '获得什么荣誉？': 'teacher_award', 
            teachersEntity + '的邮箱是？': 'teacher_mail', 
            teachersEntity + '的联系方式是？': 'teacher_mail', 
            teachersEntity + '的联络方式是？': 'teacher_mail', 
            teachersEntity + '的email': 'teacher_mail', 
            teachersEntity + '电话是？': 'teacher_tel', 
            teachersEntity + 'tel是': 'teacher_tel', 
            teachersEntity + '如何联系？': 'teacher_tel', 
            teachersEntity + '介绍一下': 'teacher_describe', 
            teachersEntity + '的简介': 'teacher_describe', 
            teachersEntity + '如何': 'teacher_describe'
        }
        lisSimilarity = [vector_similarity(question, i) for i in exSentences] 
        if max(lisSimilarity) < 0.3:
            return []
        else:
            return dictSentences[lisSimilarity.find(max(lisSimilarity))]
        