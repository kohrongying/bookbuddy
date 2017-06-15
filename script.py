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

class Error(Exception):
   """Base class for other exceptions"""
   pass

class BadRequestError(Error):
	"""Raised when getTree gives Bad Request"""
	pass

class Book:
	def __init__(self, title, location, callNumber):
		self.title = title
		self.location = location
		self.callNumber = callNumber

	def getLocation(self):
		return self.location

	def getCallNumber(self):
		return self.callNumber

	def __str__(self):
		return "{:30s} | {:20s} | {:20s}".format(self.title, self.location, self.callNumber)
		
class Library:
	availBooks = []
	def __init__(self, name):
		self.name = name

	def addBook(self,book):
		availBooks.append(book)

	def getBooks(self):
		return availBooks

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

def getAvailBooks(book,url):
	# print("\n"+book)
	tree = getTree(url,book) 
	
	for table in tree.find_class('clsTab1'):
		for tr in table.findall('tr'):
			td_list = tr.findall('td')
			if td_list != []:
				library = td_list[0].text_content()
				location = td_list[1].text_content()
				callNum = td_list[2].text_content()
				status = td_list[3].text_content()

				if status == "Available":
					newBook = Book(book, location, callNum)
					# print(library)
					if library in d:
						d[library].append(newBook)
					else:
						d[library] = [newBook]

#to query d about library
def queryLibrary(lib):
	if lib in d:
		for b in d[lib]:
			print(b)

def getResults(libList):
	for lib in libList:
		print(lib)
		queryLibrary(lib)
		print('\n')
	
myLibList = [
		  'Marine Parade Public Library',
		  'Bedok Public Library',
		  'Geylang East Public Library',
		  'Central Public Library'
			]

file = open('booklist.txt','r')

#to build dictionary, d
for line in file:
	lineList = line.split(';')
	book = lineList[0]
	url = lineList[1]
	getAvailBooks(book,url)

getResults(myLibList)
# print(d)
# b = tree.xpath('//table[@class="clsTab1"]/text()')