import os,json,pickle
from pprint import pprint
from multiprocessing import Process
a=raw_input("Enter file\n")
def func(a):
	msg="curl -s -X POST --form 'file=@"+a+"' https://api.idolondemand.com/1/api/sync/extractconcepts/v1 -F apikey=35fabcae-4924-4ddb-a66f-8440a4e6a901"
	print "Getting necessary keywords from file...."
	#print msg
	os.system(msg)
p=Process(target=func,args=(a,))
p.start()
p.join()
"""l=[]
with open('out.json') as out:
	data=json.load(out)
for i in range(0,100):
	try:
		
   		with open("tout.json") as fout: 
                
		pprint((str(data['concepts'][i]['concept'])) > out.json)
	except:
		pass"""
