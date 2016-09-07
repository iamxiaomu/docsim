#coding:utf-8
#使用docsim方法：doc2bow、similarities判断相似性
from gensim import models,corpora,similarities
import jieba.posseg as pseg
import os

def a_sub_b(a,b):
    ret = []
    for el in a:
        if el not in b:
            ret.append(el)
    return ret
    
#读取文件
raw_documents=[]
walk = os.walk(os.path.realpath("/Users/muhongfen/sougou"))
for root, dirs, files in walk:
    for name in files:
        f = open(os.path.join(root, name), 'r')
    raw = str(os.path.join(root, name))+" "
    raw += f.read()
    raw_documents.append(raw)
stop = [line.strip().decode('utf-8') for line in open('stopword.txt').readlines() ]
#创建语料库
corpora_documents = []
for item_text in raw_documents:
    item_str=[]
    item= (pseg.cut(item_text)) #使用jieba分词
    for i in list(item):
        item_str.append(i.word)
    item_str=a_sub_b(item_str,list(stop))
    corpora_documents.append(item_str)

# 生成字典和向量语料
dictionary = corpora.Dictionary(corpora_documents) #把所有单词取一个set，并对set中每一个单词分配一个id号的map
corpus = [dictionary.doc2bow(text) for text in corpora_documents]  #把文档doc变成一个稀疏向量，[(0,1),(1,1)]表明id为0,1的词出现了1次，其他未出现。
similarity = similarities.Similarity('-Similarity-index', corpus, num_features=999999999)

test_data_1 = '本报讯 全球最大个人电脑制造商戴尔公司８日说，由于市场竞争激烈，以及定价策略不当，该公司今年第一季度盈利预计有所下降。'\
'消息发布之后，戴尔股价一度下跌近６％，创下一年来的新低。戴尔公司估计，其第一季度收入约为１４２亿美元，每股收益３３美分。此前公司预测当季收入为１４２亿至１４６亿美元，'\
'每股收益３６至３８美分，而分析师平均预测戴尔同期收入为１４５．２亿美元，每股收益３８美分。为抢夺失去的市场份额，戴尔公司一些产品打折力度很大。戴尔公司首席执行官凯文·罗林斯在一份声明中说，公司在售后服务和产品质量方面一直在投资，同时不断下调价格。戴尔公司将于５月１８日公布第一季度的财报。'
test_cut = pseg.cut(test_data_1)
test_cut_raw_1=[]
for i in list(test_cut):
    test_cut_raw_1.append(i.word)
test_corpus_1 = dictionary.doc2bow(test_cut_raw_1)
similarity.num_best = 5
print(similarity[test_corpus_1])  # 返回最相似的样本材料,(index_of_document, similarity) tuples
for i in similarity[test_corpus_1]:
    sim=""
    print('################################')
    print i[0];
    for j in corpora_documents[i[0]]:
        sim+=j
    print sim;