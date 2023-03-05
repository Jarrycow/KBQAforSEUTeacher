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
            if question_type == 'teacher_describe':
                sql = self.sql_transfer(question_type, entity_dict.get('teacher'))
            elif question_type == 'teacher_college':
                sql = self.sql_transfer(question_type, entity_dict.get('teacher'))
            elif question_type == 'teacher_award':
                sql = self.sql_transfer(question_type, entity_dict.get('teacher'))
            elif question_type == 'teacher_title':
                sql = self.sql_transfer(question_type, entity_dict.get('teacher'))
            elif question_type == 'teacher_direction':
                sql = self.sql_transfer(question_type, entity_dict.get('teacher'))
            elif question_type == 'teacher_mail':
                sql = self.sql_transfer(question_type, entity_dict.get('teacher'))
            elif question_type == 'teacher_tel':
                sql = self.sql_transfer(question_type, entity_dict.get('teacher'))
            elif question_type == 'teacher_gender':
                sql = self.sql_transfer(question_type, entity_dict.get('teacher'))
            elif question_type == 'teacher_background':
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

        
        if question_type == 'teacher_describe':  # 查询简介
            sql = ["MATCH (m:`教师`) where m.name = '{0}' return m.des".format(i) for i in entities]

        elif question_type == 'teacher_gender':  # 查询性别
            sql = ["MATCH (m:`教师`) where m.name = '{0}' return m.gender".format(i) for i in entities]

        elif question_type == 'teacher_college':  # 查询学院
            sql = ["MATCH(m:`教师`)-[r:belong_College]->(c:`学院`) WHERE m.name = '{0}' return c.name".format(i) for i in entities]
        
        elif question_type == 'teacher_direction':  # 查询研究方向
            sql = ["MATCH(m:`教师`)-[r:be_dir_for]->(d:`研究方向`) WHERE m.name = '{0}' return d.name".format(i) for i in entities]

        elif question_type == 'teacher_title':  # 查询职称
            sql = ["MATCH(m:`教师`)-[r:be_title_for]->(t:`职称`) WHERE m.name = '{0}' return t.name".format(i) for i in entities]

        elif question_type == 'teacher_background':  # 学术背景
            sql = ["MATCH (m:`教师`) where m.name = '{0}' return m.background".format(i) for i in entities]
        
        elif question_type == 'teacher_award':  # 奖项
            sql = ["MATCH (m:`教师`) where m.name = '{0}' return m.award".format(i) for i in entities]
        elif question_type == 'teacher_mail':  # 邮箱
            sql = ["MATCH (m:`教师`) where m.name = '{0}' return m.mail".format(i) for i in entities]
        elif question_type == 'teacher_tel':  # 电话
            sql = ["MATCH (m:`教师`) where m.name = '{0}' return m.tel".format(i) for i in entities]
        else:
            sql = ["MATCH (m:`教师`) where m.name = '{0}' return m.des".format(i) for i in entities]
        return sql