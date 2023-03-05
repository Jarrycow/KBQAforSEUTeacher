from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        # self.g = Graph(
        #     # "http://localhost:7474/db/data"  # py2neo 2.0.8写法
        #     host="127.0.0.1",  # py2neo 3写法
        #     user="neo4j",
        #     password="000614"
        # )
        self.g = Graph(  # neo4j 链接服务
            host="127.0.0.1",
            http_port=7474,
            user="neo4j",
            password="000614")
        self.num_limit = 30
    
    def search_main(self, res_classify, sqls):  # 执行 cypher 查询，返回结果
        teachers = [i for i in res_classify['args'].keys()]
        ressTeacher = [[i] for i in teachers]
        for _sql in sqls:
            queries = _sql['sql']
            answer = []
            for iquery in range(len(queries)):
                query = queries[iquery]
                ress = self.g.run(query).data()
                answer.append(ress)
                ressTeacher[iquery].append(ress)
        return ressTeacher
    
    def answer_prettify(self, answers):  # 根据对应问题类型，调用
        '''
        res_classify: 问题分类，包含人名
        answer: 回答
        '''
        finalTeacherAnswer = []
        for answer in answers:
            infoAnswer = self.sql_transfer_answer(answer)
            finalTeacherAnswer.append(infoAnswer)
        finalAnswer = '\n'.join(finalTeacherAnswer)
        return finalAnswer
    
    def sql_transfer_answer(self, answers):
        teacherName = answers[0]
        infosTeacher = []
        infoAnswers = ""
        for infoTeacher in answers[1:]:
            if {('m.gender' in i) for i in infoTeacher} == {True}:  # 性别
                infosTeacher.append('性别为' + infoTeacher[0]['m.gender'])
            elif {('c.name' in i) for i in infoTeacher} == {True}:  # 学院
                _college = '、'.join([i['c.name'] for i in infoTeacher])
                infosTeacher.append('属于' + _college)
            elif {('d.name' in i) for i in infoTeacher} == {True}:  # 研究方向
                _direction = '、'.join([i['d.name'] for i in infoTeacher])
                infosTeacher.append('研究方向是' + _direction)
            elif {('t.name' in i) for i in infoTeacher} == {True}:  # 职称
                infosTeacher.append('职称是' + infoTeacher[0]['t.name'])
            elif {('m.background' in i) for i in infoTeacher} == {True}:  # 学术背景
                infosTeacher.append('学术背景为' + infoTeacher[0]['m.background'])
            elif {('m.award' in i) for i in infoTeacher} == {True}:  # 奖项
                infosTeacher.append('所获奖项为' + infoTeacher[0]['m.award'])
            elif {('m.mail' in i) for i in infoTeacher} == {True}:  # 邮箱
                infosTeacher.append('邮箱为' + infoTeacher[0]['m.mail'])
            elif {('m.tel' in i) for i in infoTeacher} == {True}:  # 电话
                infosTeacher.append('电话为' + infoTeacher[0]['m.tel'])
            else:  # {('m.des' in i) for i in infosTeacher} == {True}:  # 简介
                infosTeacher.append('\n' + '简介：' + infoTeacher[0]['m.des'])

        infoAnswers = teacherName + '老师' + ', '.join(infosTeacher)
        return infoAnswers