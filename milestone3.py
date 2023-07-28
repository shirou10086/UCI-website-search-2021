import json
import math
from collections import defaultdict
import requests
from bs4 import BeautifulSoup
import milestone1
import queryprocess
def inputquery(query):
    #return divided query list
    query= queryprocess.query(q)
    query.processquery()
    return query
#query="hi uci education"
#hi docid list=1 13 67 981
#uci docid 1 51 67 981
#education docid 1 13 67
def matchvaliddocid(query,invertedindex):
    querylist=[]
    querydict=dict()
    anslist=[]
    for token in query.getsetquery():
        if token in invertedindex:
            querydict[token]=invertedindex[token]
    querydict=sorted(querydict.items(),key=lambda x:len(x[1]),reverse=True)
    querydict={k:v for k,v in querydict}
    firstdict=list(querydict.items())[0][1]
    for key,value in querydict.items():
        if len(mergetwodict(value,firstdict))>=5:
            firstdict=mergetwodict(value,firstdict)
            querylist.append(key)
    for i in firstdict.keys():
        anslist.append(i)
    ansdict=gettfidf(list(query.getsetquery()),anslist,invertedindex)
    return ansdict
def search(query,urldict,invertedindex):
    # cited idea from https://blog.csdn.net/weixin_43907422/article/details/89322288
    answer=dict()
    validdocid=matchvaliddocid(query,invertedindex)
    querydict=getquerytfidf(query)
    if validdocid==None:
        return validdocid
    else:
        for key,value in validdocid.items():
            for docid,tfidf in value.items():
                sim1 = 0
                temp1 = 0
                temp2 = 0
                for i in querydict.keys():
                    if i in validdocid.keys() and docid in validdocid[i].keys():
                        sim1 += querydict[i] + validdocid[i][docid]
                        temp1 += querydict[i] ** 2
                        temp2 += validdocid[i][docid] ** 2
                if (math.sqrt(temp1) * math.sqrt(temp2))==0:
                    cos=0
                else:
                    cos = sim1 / (math.sqrt(temp1) * math.sqrt(temp2))
                answer[docid]=cos
    ans=dict(sorted(answer.items(), key=lambda item: item[1]))
    if len(list(ans.keys()))==0:
        print("No Page found")
    elif len(list(ans.keys()))<5:
        for i in ans.keys():
            print(geturl(urldict,i))
    else:
        anslist=[]
        for i in ans.keys():
            anslist.append(i)
        for i in anslist[:5]:
            print(geturl(urldict,i))
def geturl(urldict,docid):
    for k,v in urldict.items():
        if v==int(docid):
            return k
def gettfidf(query:list, docidlist:list, invertedindex:dict):
    return_dict = {}
    for i in query:
        for j in docidlist:
            if i in invertedindex.keys() and j in invertedindex[i]:
                if i not in return_dict:
                    return_dict[i] = {j: invertedindex[i][j]["tf_idf"]}
                else:
                    return_dict[i][j] = invertedindex[i][j]["tf_idf"]
    return return_dict

def mergetwodict(dict1,dict2):
    ansdict=dict()
    for docid,dict1value in dict1.items():
        if docid in dict2.keys():
            ansdict[docid]=dict1value
    return ansdict
def getcontent(url):
    output=[]
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)
    blacklist = ['[document]','noscript','header','html','meta','head','input','script','style']
    for t in text:
        if t.parent.name not in blacklist:
            output.append(t)
    return output
def getquerytfidf(query):
    frequencydict=dict()
    querytfidfdict=dict()
    count=0
    for i in query.getlistquery():
        if i in frequencydict.keys():
            frequencydict[i]=frequencydict.get(i)+1
        else:
            frequencydict[i]=1
    for key,value in frequencydict.items():
        querytfidfdict[key]=(1 + math.log10(value)) * (math.log10(query.getquerylength() / value))
    for k,v in querytfidfdict.items():
        count+=v**2
    count=math.sqrt(count)
    for k,v in querytfidfdict.items():
        if count!=0:
            querytfidfdict[k]=v/count
        else:
            querytfidfdict[k] =1
    return querytfidfdict
def getjson(jsonaddr):
    with open(jsonaddr, 'r') as fp:
        dict=json.load(fp)
    return dict
if __name__ == '__main__':
    import time
    #url=input("Input url address:")
    #milestone1.geturl_dic("r"+url)
    urldict= getjson("URLdictionary.json")
    invertedindex = getjson("mergeIndex.json")
    print("Program Start,stopwords will be ignored,input 'Quit' to quit")
    while True:
        q = input("Input query:")
        if q=="Quit":
            quit()
        start = time.time()
        query=inputquery(q)
        if len(query.getsetquery())==0:
            print("Not valid input")
        else:
            search(query,urldict,invertedindex)
        stop = time.time()
        print("time:", stop-start)


