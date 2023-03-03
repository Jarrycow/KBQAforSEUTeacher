class QuestionPaser:

    def build_entitydict(self, args):  # 构建实体节点
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)
        return entity_dict

    def paser_main(self, res_classify):  # 解析主函数
        args = res_classify['args']  # 实体和实体类型
        entity_dict = self.build_entitydict(args)  # 构建实体节点
        question_types = res_classify['question_types']  # 问题类型
        sqls = []
        for question_type in question_types:
            _sql = {}
            _sql['question_type'] = question_type


            sql = []
            if question_type == 'teacher_college':
                sql = self.sql_transfer(question_type, entity_dict.get('teacher'))
            elif question_type == 'teacher_award':
                sql = self.sql_transfer(question_type, entity_dict.get('teacher'))

            if sql:
                _sql['sql'] = sql
                sqls.append(_sql)
        return sqls

    def sql_transfer(self, question_type, entities):  # 针对不同问题进行分开处理
        if not entities:
            return []
        
        # 查询语句
        sql = []

        # 查询学院
        if question_type == 'teacher_college':
            sql = ["MATCH (m:teacher) where m.name = '{0}' return m.name, m.college".format(i) for i in entities]
        
        elif question_type == 'teacher_background':
            sql = ["MATCH (m:`教师`) where m.name = '{0}' return m.name, m.college".format(i) for i in entities]
        
        elif question_type == 'teacher_award':
            sql = ["MATCH (m:`教师`) where m.name = '程光' return m.award".format(i) for i in entities]
            
        print(sql)
        return sql