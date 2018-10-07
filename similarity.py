import jieba
from gensim import corpora,models,similarities

dic={}
dic_simple={}
all_doc=[]
all_doc_list=[]
for id in range(3000):
    f=open('爬虫/'+str(id),'r',encoding='UTF-8')
    string=''
    string=f.read()
    all_doc.append(string)
    print(id)
for doc in all_doc:
    doc_list = [word for word in jieba.cut_for_search(doc)]
    all_doc_list.append(doc_list)
dictionary = corpora.Dictionary(all_doc_list)
corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]
tfidf = models.TfidfModel(corpus)
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))
_f=open('similarity/sim','w',encoding='UTF-8')
for id in range(3000):
    f=open('爬虫/'+str(id),'r',encoding='UTF-8')
    doc_test=f.read()
    doc_test_list = [word for word in jieba.cut_for_search(doc_test)]
    doc_test_vec = dictionary.doc2bow(doc_test_list)
    sim = index[tfidf[doc_test_vec]]
    enum=(sorted(enumerate(sim), key=lambda item: -item[1]))
    count=0
    for num,i in enum:
        if count==0:
            count+=1
            continue
        elif count<4:
            count+=1
            _f.write(str(num))
            _f.write(' ')
        else:
            _f.write('\n')
            break


