# coding: utf-8


from question_classifier import QuestionClassifier
from question_parser import QuestionPaser
from answer_search import AnswerSearcher

class ChatBotGraph:  # 问答类
    def __init__(self):
        self.classifier = QuestionClassifier()  # 问题分类
        self.parser = QuestionPaser()  # 
        self.searcher = AnswerSearcher()  # 

    def chat(self, sent):
        if('结束' in sent):
            return -1
        final_answer = []
        sentences = self.classifier.sentenceSplit(sent)
        for sentence in sentences:
            res_classify = self.classifier.classify(sentence)  # 问题分类
            if not res_classify:
                return '抱歉，小助手暂时无法回答您的问题，请前往学院官网查询。'
            res_sql = self.parser.paser_main(res_classify)
            answers = self.searcher.search_main(res_classify, res_sql)
            final_answer.append(self.searcher.answer_prettify(answers))
        final_answers = '\n'.join(final_answer)
        return final_answers

if __name__ == '__main__':
    handler = ChatBotGraph()
    while 1:
        question = input('用户:')
        answer = handler.chat(question)
        print('小助手:', '\n' + answer)
        if(answer == -1):
            print('小助手:', '感谢您使用导师查询小助手')
            break

