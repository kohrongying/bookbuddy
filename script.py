from lxml import html
from lxml.etree import tostring
import requests

#Stores libraries as keys and the books available there as values
d = {}

headers = {
    # "Host": "api.sitescout.com",
    # "Authorization": "Basic YmVldGhvdmVuOmxldG1laW4=",
    "Content-Type": "text/html; charset=UTF-8"
    # "Accept": "application/json",
    # "Content-Length": "41"
}
def getTree(s,book):
	try:
		page = requests.get(s,headers=headers)
		tree = html.fromstring(page.content)
		if "Bad Request" in tree.text_content():
			raise BadRequestError

	except BadRequestError:
		print(book+" Bad Request")
	
	finally:
		return tree

class Error(Exception):
   """Base class for other exceptions"""
   pass

class BadRequestError(Error):
	"""Raised when getTree gives Bad Request"""
	pass

def getAvailBooks(book,url):
	avail=0
	# print("\n"+book)
	tree = getTree(url,book) 
	
	for table in tree.find_class('clsTab1'):
		for tr in table.findall('tr'):
			td_list = tr.findall('td')
			if td_list != []:
				#index 1 is location
				library = td_list[0].text_content()
				status = td_list[3].text_content()
				#index 2 is call number eg. English SHU
				if status == "Available":
					avail+=1
					# print(library)
					if library in d:
						d[library].append(book)
					else:
						d[library] = [book]

file = open('booklist.txt','r')

#to query d about library
def queryLibrary(lib):
	if lib in d:
		return d[lib]
	return 'None'

myLibList = [
		  'Marine Parade Public Library',
		  'Bedok Public Library'
			]

#to build dictionary, d
for line in file:
	lineList = line.split(';')
	book = lineList[0]
	url = lineList[1]
	getAvailBooks(book,url)

def getResults(libList):
	for lib in libList:
		print(lib)
		print(queryLibrary(lib))
		print("\n")

getResults(myLibList)
# print(d)
# print(getLibraryBooks('Marine Parade Public Library'))
# b = tree.xpath('//table[@class="clsTab1"]/text()')

"""TO DO
- Populate booklist.txt
- Change book as object
- display lib with top books
- ranked in order of preference of library
"""
