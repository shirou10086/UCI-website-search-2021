import os
import json
import re
import math

from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from bs4.element import Comment



def tokenizer(content):
    return re.findall(r"[A-Za-z0-9]+", content.lower())

def indexing(docid,content,inverted_index):

    soup = BeautifulSoup(content,"html.parser")
    texts = soup.findAll(text=True)
    text1 = " ".join(filter(all_text, texts))
    import_text2 = " ".join(filter(important_text, texts))
    # print(import_text2)
    #print(text1)
    ps = PorterStemmer()
    position = 0

    for i in tokenizer(text1):
        token = ps.stem(i)
        if token not in inverted_index.keys():
            inverted_index[token] = { docid: {'positions': [position], 'is_important': 0}}
        # if token was in invertedIndex, update it
        else:
            if docid not in inverted_index[token].keys():
                inverted_index[token][docid] = {'positions': [position], 'is_important': 0}
            else:
                inverted_index[token][docid]['positions'].append(position)
        position += 1

    for i in tokenizer(import_text2):
        token = ps.stem(i)
        if (token in inverted_index) and (docid in inverted_index[token]):
            inverted_index[token][docid]['is_important'] += 1

def TF_IDF(inverted_index):
    N = len(docid_url)
    for token, docid_dict in inverted_index.items():
        df = len(docid_dict)
        print(N)
        print(df)
        for docid, tfidf_dict in docid_dict.items():
            tfidf_dict["tf_idf"] = (1 + math.log(len(tfidf_dict["positions"])+tfidf_dict["is_important"], 10)) / math.log(N/df, 10)


def geturl_dic(folder):
    global  docid_url
    docid_url = {}  #  key: url,value: unique id num of doc
    inverted_index = {}  # inverted_index = {key: token; value: {docid: {tf_idf: INT, positions:[INT],is_important: 0}})
    #count th total number of files
    count1 = 0
    for (root, dirs, files) in os.walk(folder):
        count1 += len(files)

    stop_pos = count1 // 3
    #print(count1,stop_pos)

    count2 = 0
    num_pindex = 1
    for (root, dirs, files) in os.walk(folder):
        for page_name in files:
            count2 += 1
            file_loc = os.path.join(root, page_name)
            try:

                f = open(file_loc, 'rb')
                file_dic = json.loads(f.read())
                url = file_dic["url"]
                content = file_dic['content']
                f.close()
                if url not in docid_url.values():
                    docid = len(docid_url)
                    docid_url[url] = docid
                else:
                    docid = docid_url[url]

                #store index into three
                if count2 > stop_pos and num_pindex != 3:
                    jsonfile(inverted_index,num_pindex)
                    num_pindex += 1
                    count2 = 0
                    inverted_index = {}
                indexing(docid,content,inverted_index)
            except ValueError as e:
                print(e)
    #print(docid_url)
    jsonfile(inverted_index,num_pindex)
    writedict(docid_url)
    final_index = "mergeIndex.json"
    mergeTwoFile("partialIndex1.json", "partialIndex2.json", "partialIndex3.json", final_index)

def jsonfile(invert_index, num_pindex):
    with open("partialIndex"+str(num_pindex)+".json", "w") as f:
        line = json.dumps(invert_index)
        f.write(line)
def writedict(dictionary):
    with open("URLdictionary.json", "w") as f:
        line = json.dumps(dictionary)
        f.write(line)

def all_text(text):
    if text.parent.name in ['style', 'script', 'head', 'meta', 'title', '[document]']:
        return False
    if isinstance(text, Comment):
        return False
    return True

def important_text(text):
    if text.parent.name in ['b', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong']:
        return True
    return False

def mergeTwoFile(f1, f2, f3,  merge_file):

    #merge 1 and 2
    with open(f1, 'r') as f:
        partial1_dic = json.load(f)
    with open(f2, 'r') as f:
        partial2_dic = json.load(f)
    for tokens in partial2_dic:
        if tokens not in partial1_dic.keys():
            partial1_dic[tokens] = partial2_dic[tokens]
        else:
            for docId in partial2_dic[tokens].keys():
                partial1_dic[tokens][docId] = partial2_dic[tokens][docId]
    with open(merge_file, 'w') as f:
        f.write(json.dumps(partial1_dic))

    #merge 3 and 4
    with open(merge_file, 'r') as f:
        partialmerge_dic = json.load(f)
    with open(f3, 'r') as f:
        partial3_dic = json.load(f)
    for tokens in partial3_dic:
        if tokens not in partialmerge_dic.keys():
            partialmerge_dic[tokens] = partial3_dic[tokens]
        else:
            for docId in partial3_dic[tokens].keys():
                partialmerge_dic[tokens][docId] = partial3_dic[tokens][docId]

    #add tf-idf
    TF_IDF(partialmerge_dic)

    with open(merge_file, 'w') as f:
        f.write(json.dumps(partialmerge_dic))


if __name__ == '__main__':
    geturl_dic(r"C:/Users/frank/Downloads/developer/DEV")
    print("jieshu")