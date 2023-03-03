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
    
    def search_main(self, sqls):  # 执行 cypher 查询，返回结果
        final_answers = []
        for _sql in sqls:
            question_type = _sql['question_type']
            queries = _sql['sql']
            answer = []
            for query in queries:
                # query = "MATCH (m:`教师`) where m.name = '程光' return m.name, m.background"
                ress = self.g.run(query).data()
                answer.append(ress)
            final_answer = self.answer_prettify(question_type, answer)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers
    
    def answer_prettify(self, question_type, answers):  # 根据对应问题类型，调用
        return answers[0]