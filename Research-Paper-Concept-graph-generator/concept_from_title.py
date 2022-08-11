#Generated concepts from title
import nltk
import requests,json,pickle
from pyPdf import PdfFileWriter, PdfFileReader
text=raw_input("Enter title\n")
sentence_re = r'''(?x)      
      ([A-Z])(\.[A-Z])+\.?  
    | \w+(-\w+)*           
    | \$?\d+(\.\d+)?%?      
    | \.\.\.                
    | [][.,;"'?():-_`]      
'''
lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()

grammar = r"""
    NBAR:
        {<NN.*|JJ>*<NN.*>}  
        
    NP:
        {<NBAR>}
        {<NBAR><IN><NBAR>} 
"""
chunker = nltk.RegexpParser(grammar)

toks = nltk.regexp_tokenize(text, sentence_re)
postoks = nltk.tag.pos_tag(toks)

#print postoks

tree = chunker.parse(postoks)

from nltk.corpus import stopwords
stopwords = stopwords.words('english')


def leaves(tree):
    for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
        yield subtree.leaves()

def normalise(word):
    word = word.lower()
    word = lemmatizer.lemmatize(word)
    return word

def acceptable_word(word):
    accepted = bool(2 <= len(word) <= 40
        and word.lower() not in stopwords)
    return accepted


def get_terms(tree):
    for leaf in leaves(tree):
        term = [ normalise(w) for w,t in leaf if acceptable_word(w) ]
        yield term

terms = get_terms(tree)
te=[]
for term in terms:
    for each in term:
    	print each
        resp=requests.get("https://api.idolondemand.com/1/api/sync/findrelatedconcepts/v1?text="+str(each)+"&indexes=&apikey=ca5b847d-3da1-4ea1-9d8f-be4f845a932c").json()
        for i in range(0,100):
            try:
                print resp['entities'][i]['text']
                te.append(resp['entities'][i]['text'])
            except:
                pass
