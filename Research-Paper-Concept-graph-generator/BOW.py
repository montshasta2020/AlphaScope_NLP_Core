#Generates bag of words
import os,json,pickle
from pprint import pprint
from multiprocessing import Process

def func(a):
	a=a.replace(" ","+")
	msg="curl -s 'https://api.idolondemand.com/1/api/sync/findrelatedconcepts/v1?text="+a+"&indexes=&apikey=ca5b847d-3da1-4ea1-9d8f-be4f845a932c'>concepts.json"
	print "Generating bag of words...."
	os.system(msg)
aaa=raw_input("Set Corpus Path-Min 50\n")

inp=raw_input("Enter concept\n")
func(inp)
def connect(a):
	p=Process(target=func,args=(a,))
	p.start()
	p.join()
	with open('concepts.json') as out:
		data=json.load(out)
	for i in range(0,100):
		try:
			pprint(str(data['entities'][i]['text']))
		except:
			pass
