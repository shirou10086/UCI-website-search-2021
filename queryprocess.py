from nltk.stem import PorterStemmer
import re
class query:
    def __init__(self,query):
        ps = PorterStemmer()
        self.dividedquery=[]
        self.query=re.findall(r"[A-Za-z0-9]+", ps.stem(query.lower()))
        self.stopwordlist=["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

    def getquery(self):
        return self.dividedquery
    def getsetquery(self):
        return self.dividedquery
    def getlistquery(self):
        return self.query
    def processquery(self):
        if len(list(set(self.query).difference(set(self.stopwordlist))))>1:
            self.dividedquery=list(set(self.query).difference(set(self.stopwordlist)))
        else:
            self.dividedquery=list(set(self.query))
    def getquerylength(self):
        return len(self.query)
