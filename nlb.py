from zeep import Client
import json
import re
#python -mzeep http://openweb-stg.nlb.gov.sg/OWS/CatalogueService.svc?wsdl



bid='12218213'
isbn="000750182X"

def addSpace(string):
	result = ''
	for char in string:
		if char.isupper() and char != string[0]:
			result += ' ' + char
		else:
			result += char
	return result

# print(addSpace('HelloRY'))
with open('apikey.txt', 'r') as f:
	apikey = f.readline()
client = Client('http://openweb-stg.nlb.gov.sg/OWS/CatalogueService.svc?singleWsdl')

def jsonifyResult(result):
	s = str(result)
	s = re.sub('\s+','',s)
	s = re.sub('\'','"',s)
	s = s.replace('None', '"None"')
	return json.loads(s)

def getAvailabilityInfo(isbn):
	result = client.service.GetAvailabilityInfo(APIKey=apikey,ISBN=isbn)
	data = jsonifyResult(result)
	print(data)
	if data.get('Status') == 'OK':
		libraries = []
		items = data.get('Items', {})
		if items != 'None':
			items = items.get('Item', {})
			call_number = items[0].get('CallNumber', '')
			location = addSpace(items[0].get('LocationDesc', ''))
			for item in items:
				if item.get('StatusDesc') == 'NotOnLoan':
					library = addSpace(item.get('BranchName'))
					if library not in libraries:
						libraries.append(library)

			toReturn = {
					'libraries': libraries, 
					'call_number': call_number,
					'location': location
					}
		else:
			return None
	else:
		return None
	
	return toReturn

isbn = '9780451163967'
# print(getAvailabilityInfo(isbn))

def getMPBooks():
	mpbooks = []
	f = open('toread.txt', 'r')
	lines = f.readlines()
	for line in lines:
		isbn10, isbn13, title = line.split(';')
		result = client.service.GetAvailabilityInfo(APIKey=apikey,ISBN=isbn13)
		data = jsonifyResult(result)
		if data.get('Status') == 'OK':
			# print(title)
			items = data.get('Items', {})
			if items != 'None':
				items = items.get('Item', {})
				call_number = items[0].get('CallNumber', '')
				location = addSpace(items[0].get('LocationDesc', ''))
				for item in items:
					if item.get('StatusDesc') == 'NotOnLoan':
						library = addSpace(item.get('BranchName'))
						if library == 'Marine Parade Public Library':
							# mpbooks.append(title)
							print('{} {}'.format(title, call_number))
							break
	return mpbooks

print(getMPBooks())