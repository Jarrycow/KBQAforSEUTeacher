# coding: utf-8


from question_classifier import QuestionClassifier
from question_parser import QuestionPaser
from answer_search import AnswerSearcher

class ChatBotGraph:  # 问答类
    def __init__(self):
        self.classifier = QuestionClassifier()  # 问题分类
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat(self, sent):
        answer = '您好，我是导师查询小助手！祝您学业顺利'
        res_classify = self.classifier.classify(sent)  # 问题分类
        print(res_classify)
        if not res_classify:
            return '抱歉，小助手暂时无法回答您的问题，请前往学院官网查询。'
        res_sql = self.parser.paser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        return final_answers

if __name__ == '__main__':
    handler = ChatBotGraph()
    while 1:
        # question = input('用户:')
        question = "程光奖项是？"
        answer = handler.chat(question)
        print('小助手:', answer)

