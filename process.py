import csv
import os 
from datetime import datetime


inputPath = 'input.csv'
outputPath = 'output.csv'
if os.path.isfile(outputPath):
	os.remove(outputPath)
outputCSVFile = open(outputPath, 'a')
def replaceWord(lst, replacementDict):
    return [replacementDict.get(w) for w in lst]

def parseDate(dateString):
	return datetime.strptime(dateString, '%m/%d/%Y %H:%M:%f') 

def parseMemo(memo):
    tokens = memo.split(' ')
    
    if tokens[-1].isdigit():
        try:
            return datetime.strptime('{0} {1}'.format(tokens[-2], tokens[-1]),
                                     '%b %d')
        except ValueError:
            pass

with open(inputPath, 'rb') as csvfile:
	reader=csv.reader(csvfile, dialect='excel')
	writer = csv.writer(outputCSVFile, dialect='excel')
	headers = []
	headersDict = dict()
	for i, row in enumerate(reader):
		print i
		if (i == 0):
			header = row
			print row
			headersDict = {value:idx for idx, value in enumerate(header)}
			row = replaceWord(row, {
			'date': 'Date',
			'amount':'Account Title',
			'category': 'Post Ref.',
			'description': 'Debit',
			'memo': 'Credit',
			'notes': 'Addendum'})
		else:
			data = dict(enumerate(row))

			date_obj = parseDate(data[headersDict.get('date')])
		
			memo_date = parseMemo(data[headersDict.get('memo')])
			result =[]

			if memo_date:
				date_col=memo_date.replace(year=date_obj.year).strftime("%Y-%m-%d")
			else:
				date_col=date_obj.strftime("%Y-%m-%d")
				

			amount=round(float(data[headersDict.get('amount')]), 2)
			account_title="Fireman Visa"
			post_ref="2011"
			addendum='{0}{1}'.format(data[headersDict.get('description')], data[headersDict.get('memo')])
			debit=abs(amount) if amount< 0 else ''
			credit=abs(amount) if amount > 0 else ''
			
			result.append(date_col)
			result.append(account_title)
			result.append(post_ref)
			result.append(debit)
			result.append(credit)
			result.append(addendum)

			print "RESULT:"
			row=result
		print row

		writer.writerow(row)
