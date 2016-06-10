import csv
import re
from nltk.stem.wordnet import WordNetLemmatizer

lmtzr = WordNetLemmatizer()
rule1=re.compile(r'[^a-zA-z\s\n\t]')

def root(str):
	tmp = rule1.sub('', str)
	try:
		tmp = tmp.split(' ')
	except:
		tmp = ''
	data = []
	for i in tmp:
		i = lmtzr.lemmatize(i)
		data.append(i)
	string = ' '.join(data)
	return string

def readcsv(fway):
	csvfile = file(fway, 'rb')
	reader = csv.reader(csvfile)
	f1 = csv.writer(file('use.csv', 'wb'))
	f2 = csv.writer(file('no_use.csv', 'wb'))
	f1.writerow(['star', 'title', 'date', 'length', 'review'])
	f2.writerow(['star', 'title', 'date', 'length', 'review'])
	for i,line in enumerate(reader):
		string = root(line[3])
		length = len(line[3])
		if string:
			print i
			sign = choose(string)
    			if sign:
    				f1.writerow([line[1],  line[2], line[4], length, string])
    			else:
    				f2.writerow([line[1],  line[2], line[4], length, string])
    	csvfile.close()
    	f1.close()
    	f2.close()

def choose(string):
	print string
	print '================================='
	if len(str(string)) > 120:
		return True
	signal = raw_input()
	if signal:
		return True
	else:
		return False




