#Analysing sectionwise contents and plotting it 
import os,re
from multiprocessing import Process
import helper
import nltk,pickle,requests
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from random import randint
import json
l=[]
text=''
count=0

#json from BOW

with open('out.json','r') as f:
	#data=json.load(f)
	try:
		for i in range(0,100):
			text+=data['concepts'][i]['concept']+" "
	except:
		pass
#json from title

with open('concepts.json','r') as f:
	#data=json.load(f)
	try:
		for i in range(0,100):
			text+=(data['entities'][i]['text'])+" "
	except:
		pass

def section(input,output):
	os.system(("ps2ascii %s %s") %( input , output))
a=raw_input("Enter file\n")
section(a,"out.txt")
a=re.sub('.pdf','',a);
def pos(text):
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
	for word,tag in postoks:
		#print word,tag
		if(tag=="NN" or tag=="JJ"):
			count+=1
	if(count>=2):
		print "Inside"
		return true
	#tree = chunker.parse(postoks)
	#terms=get_terms(tree)
	return false
def leaves(tree):
    for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
        yield subtree.leaves()

def normalise(word):
    word = word.lower()
    #word = lemmatizer.lemmatize(word)
    return word

def acceptable_word(word):
    accepted = bool(2 <= len(word) <= 40
        and word.lower() not in stopwords)
    return accepted


def get_terms(tree):
    for leaf in leaves(tree):
        term = [ normalise(w) for w,t in leaf if acceptable_word(w) ]
        yield term
def analyser():
	msg="curl -s -X POST --form 'file=@sec.txt' https://api.idolondemand.com/1/api/sync/extractconcepts/v1 -F apikey=ca5b847d-3da1-4ea1-9d8f-be4f845a932c>inter.txt"
	os.system(msg)

#Analysing section

def analyse():
	f=open("out.txt",'r')
	temp=str(f.read())

	#regular expression for section wise splitting
	pattern=re.compile(r'\n[-+]?\d*\.\d+ [A-Z][a-z]+.*|\n\d+\. [A-Z][a-z]+.*|\n[-+]?\d*\.\d+\. [A-Z][a-z]+.*|\n[-+]?\d*\.\d+\.\d+\. [A-Z][a-z]+.*')
	#pattern=re.compile(r'[0-9]\.* [A-Z][a-z]+\n')
	section_list=pattern.findall(temp)
	before=temp
	n=len(section_list)
	mm=0
	res=['' for i in range(0,n)]
	ress=['' for i in range(0,n)]
	for i in range(len(section_list)-1,0,-1):
		print "Analysing Section:",abs(i-len(section_list))
		#print "\n******************\n"
		print section_list[i]
		if i==len(section_list)-1:
			before,curr,after=temp.partition(section_list[i])
			continue
		else:
			if "Elsevier" in section_list[i]:
				continue
			beforei,curr,after=temp.partition(section_list[i])
			t=''
			j=len(beforei)
			analyser_=''
			while j<len(before):
				t+=before[j]
				analyser_+=before[j]
				j+=1
			before=beforei
			m=open("sec.txt",'w')
			m.write(analyser_)
			m.close()
			p=Process(target=analyser,args=())
			p.start()
			p.join()
			with open('inter.txt') as out:
				data=json.load(out)
			y=" "
			for kk in range(0,100):
				try:
					#checking word length and removing stopwords
					if(len(str(data['concepts'][kk]['concept']))>5 and str(data['concepts'][kk]['concept'][-2]!='ly') and y in data['concepts'][kk]['concept']):
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

						toks = nltk.regexp_tokenize(data['concepts'][kk]['concept'], sentence_re)
						postoks = nltk.tag.pos_tag(toks)
						count=0
						#print len(postoks)
						for dd in range(0,len(postoks)):
							for each in postoks[dd]:
								if(each=="NN" or each=="JJ" or each=="VBG" or each=="NNS"):
									count+=1
						if(count>=2):
							#print mm,str(data['concepts'][kk]['concept']),"**"
							res[mm]+=str(data['concepts'][kk]['concept'])+'\n'
				except Exception as e:
						pass
			"""with open('refi.txt') as h:
				try:
					data=json.load(h)
					if(data['entities'][i]['text'] in analyser_):
						res[mm]+=str(data['entities'][i]['text'])
				except:
					pass"""
			ress[mm]=re.sub(r'\d|\.','',section_list[i])
			mm+=1

	f=open('g.dot'+a,'w')
	f.write('')
	f.close()
	graph=open('g.dot'+a,'a')
	i=1
	graph.write('digraph {\n');
	#graph contains syntactical code for drawing into the graphvix tool
	for ll in range(mm-1,-1,-1):
			if(res[ll]!=""):
				graph.write('Section'+str(i)+'[shape="box",label="'+ress[ll]+'\n\n'+res[ll]+'"];\n')
				if(ll!=0):
					graph.write('Section'+str(i)+'->'+ 'Section'+str(i+1)+';\n')
				i+=1
	for ll in range(mm-1,-1,-1):
			v1=randint(1,mm-1)
			v2=randint(1,mm-1)
			if(v2!=v1+1 and v1!=v2+1 and v1!=v2):
				graph.write('Section'+str(v1)+'->'+'Section'+str(v2)+';\n')
	graph.write('}')
	
analyse()
os.system("dot -Tjpeg g.dot"+a+" -o mod"+a+".jpeg")
os.system("open mod"+a+".jpeg")
	

