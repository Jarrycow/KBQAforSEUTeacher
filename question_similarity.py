import gensim
import jieba
import numpy as np
from scipy.linalg import norm

model_file = 'data/word2vec/news_12g_baidubaike_20g_novel_90g_embedding_64.bin'
model = gensim.models.KeyedVectors.load_word2vec_format(model_file, binary=True)

def vector_similarity(s1, s2):
    def sentence_vector(s):
        words = jieba.lcut(s)
        v = np.zeros(64)
        for word in words:
            v += model[word]
        v /= len(words)
        return v
    
    v1, v2 = sentence_vector(s1), sentence_vector(s2)
    return np.dot(v1, v2) / (norm(v1) * norm(v2))

if __name__ == '__main__':
    s1 = '你在干嘛'
    s2 = '你正做什么'
    print(vector_similarity(s1, s2))