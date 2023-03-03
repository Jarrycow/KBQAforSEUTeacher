#encoding:utf8
import os
import re
import json
import codecs
import threading
from py2neo import Graph
import pandas as pd 
import numpy as np 
from tqdm import tqdm 

def print_data_info(data_path):  # 打印数据形式
    triples = []
    i = 0
    with open(data_path,'r',encoding='utf8') as f:
        for line in f.readlines():
            data = json.loads(line)
            print(json.dumps(data, sort_keys=True, indent=4, separators=(', ', ': '),ensure_ascii=False))
            i += 1
            if i >=5:
                break
    return triples

class MedicalExtractor(object):
    def __init__(self):
        super(MedicalExtractor, self).__init__()
        self.graph = Graph(  # neo4j 链接服务
            host="127.0.0.1",
            http_port=7474,
            user="neo4j",
            password="000614")

        # 定义节点
        self.teacher = []  # 姓名
        self.college = []  # 学院
        self.direction = []  # 研究方向

        self.teacher_infos = []  # 教师信息（有属性）

        # 构建节点实体关系
        self.rels_name_college = []  # 所属学院
        self.rels_name_title = []  # 教师职称
        self.rels_name_direction = []  # 研究方向
        
    def extract_triples(self,data_path):  # 从json文件中转换抽取三元组
        print("从json文件中转换抽取三元组")
        with open(data_path,'r',encoding='utf8') as f:
            for line in tqdm(f.readlines(),ncols=80):
                if(line == '[\n' or line == ',\n' or line == ']\n' or line == '\n'):
                    continue
                data_json = json.loads(line)  
                teachers_dict = {}
                teacher = data_json['name']
                teachers_dict['name'] = teacher
                
                self.teacher.append(teacher)
                teachers_dict['gender'] = ""  # 性别
                teachers_dict['des'] = ""  # 简介
                teachers_dict['background'] = ""  # 教育背景
                teachers_dict['direction'] = ""  # 研究方向
                teachers_dict['award'] = ""  # 奖项
                teachers_dict['mail'] = ""  # 邮箱
                teachers_dict['tel'] = ""  # 电话

                # 
                if 'gender' in data_json:  # json 中有性别
                    teachers_dict['gender'] = data_json['gender']
                
                if 'college' in data_json:  # 所属学院
                    colleges = data_json['college'].split(',')
                    for college in colleges:
                        self.college.append(college)
                        self.rels_name_college.append([teacher, 'belong_College', college])
                                  
                if 'title' in data_json:  # 所属职称
                    title = data_json['title']
                    self.title.append(title)
                    self.rels_name_title.append([teacher, 'be_title_for', title])

                if 'des' in data_json:  # 个人简介
                    teachers_dict['des'] = data_json['des']

                if 'background' in data_json:  # 教育背景属性
                    teachers_dict['background'] = data_json['background']

                if 'direction' in data_json:  # 研究方向
                    directions = data_json['direction']
                    directions = directions.replace('，',',')
                    directions = directions.replace('。',',')
                    directions = directions.replace('；',',')
                    directions = directions.replace(';',',')
                    directions = directions.replace('\n',',')
                    directions = directions.split(',')
                    for direction in directions:
                        if direction == '':
                            continue
                        self.direction.append(direction)
                        self.rels_name_direction.append([teacher, 'be_dir_for', direction])

                if 'award' in data_json:  # 奖项属性
                    teachers_dict['award'] = data_json['award']
                
                if 'mail' in data_json:  # 邮箱属性
                    teachers_dict['mail'] = data_json['mail']

                if 'tel' in data_json:  # 电话属性
                    teachers_dict['tel'] = data_json['tel']

                self.teacher_infos.append(teachers_dict)

    def write_nodes(self,entitys,entity_type):  # 向neo4j中写入节点
        print("写入 {0} 实体".format(entity_type))
        for node in tqdm(set(entitys),ncols=80):
            if node in self.teacher:
                teacher = self.teacher_infos[self.teacher.index(node)]
                cql = self.set_teacher_attribute(teacher, entity_type)
            else:
                cql = """MERGE(n:{label}{{name:'{entity_name}'}})""".format(
                    label=entity_type,entity_name=node.replace("'",""))
            try:
                self.graph.run(cql)
            except Exception as e:
                print(e)
                print(cql)
        
    def write_edges(self,triples,head_type,tail_type):  # 写入边
        print("写入 {0} 关系".format(triples[0][1]))
        for head,relation,tail in tqdm(triples,ncols=80):
            cql = """MATCH(p:{head_type}),(q:{tail_type})
                    WHERE p.name='{head}' AND q.name='{tail}'
                    MERGE (p)-[r:{relation}]->(q)""".format(
                        head_type=head_type,tail_type=tail_type,head=head.replace("'",""),
                        tail=tail.replace("'",""),relation=relation)
            try:
                self.graph.run(cql)
            except Exception as e:
                print(e)
                print(cql)

    def set_attributes(self,entity_infos,etype):  # 针对实体写入属性
        print("写入 {0} 实体的属性".format(etype))
        for e_dict in tqdm(entity_infos[892:],ncols=80):
            name = e_dict['name']
            del e_dict['name']
            for k,v in e_dict.items():
                if k in ['cure_department','cure_way']:
                    cql = """MATCH (n:{label})
                        WHERE n.name='{name}'
                        set n.{k}={v}""".format(label=etype,name=name.replace("'",""),k=k,v=v)
                else:
                    cql = """MATCH (n:{label})
                        WHERE n.name='{name}'
                        set n.{k}='{v}'""".format(label=etype,name=name.replace("'",""),k=k,v=v.replace("'","").replace("\n",""))
                try:
                    self.graph.run(cql)
                except Exception as e:
                    print(e)
                    print(cql)

    def set_teacher_attribute(self, teacher, label):  # 设置属性
        cql = "MERGE(n:" + label + "{"
        cql += ("name:" + "'" + teacher['name'] + "'")
        for key in teacher.keys():
            # print(key, teacher[key])
            
            if(teacher[key] != '' and key != 'name'):
                cql += "," + key + ":" + "'" + teacher[key] + "'"
        cql += "})"
        return cql

    def create_entitys(self):  # 创建实体
        self.write_nodes(self.teacher, '教师')
        self.write_nodes(self.college, '学院')
        self.write_nodes(self.title, '职称')
        self.write_nodes(self.direction, '研究方向')

    def create_relations(self):  # 创建关系
        self.write_edges(self.rels_name_title, '教师', '职称')
        self.write_edges(self.rels_name_college, '教师', '学院')
        self.write_edges(self.rels_name_direction, '教师', '研究方向')

    def set_teachers_attributes(self): 
        t=threading.Thread(target=self.set_attributes,args=(self.teacher_infos,"教师"))
        t.setDaemon(False)
        t.start()

    def export_entitys_relations(self):
        self.export_data(self.teacher, './data/teacher.json')
        self.export_data(self.college, './data/college.json')
        self.export_data(self.title, './data/title.json')
        
        self.export_data(self.rels_name_college, './data/rels_name_college.json')


if __name__ == '__main__':
    path = "./data/teachers.json"
    # print_data_info(path)
    extractor = MedicalExtractor()  # 构造 eno4j 类
    extractor.extract_triples(path)  # 从json文件中转换抽取三元组
    extractor.create_entitys()
    extractor.create_relations()
    extractor.set_teachers_attributes()
    # extractor.export_entitys_relations()
    pass