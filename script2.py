from bs4 import BeautifulSoup
import requests
from lxml import html

# s ='http://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/ENQ/EXPNOS/BIBENQ/13161956?QRY=CTIBIB%3C%20IRN(4682489)&QRYTEXT=What%20Alice%20forgot'
# page = requests.get(s)
# tree = html.fromstring(page.content)

# soup = BeautifulSoup(page.text, 'lxml')
# table = soup.find_all("table",{'class':'clsTab1'})[0]
# for tr in table.find_all('tr'):
#     library = tr.contents[0].contents[0].string
#     location = tr.contents[1].contents[0].string
#     callNum = tr.contents[2].contents[0].string
#     status = tr.contents[3].contents[0].string
#     print(library, location, callNum, status)
# print(table[0].prettify())
#Stores libraries as keys and the books available there as values
d = {}

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

# def getTree(s,book):
#     try:
#         page = requests.get(s,headers=headers)
#         tree = html.fromstring(page.content)
#         if "Bad Request" in tree.text_content():
#             raise BadRequestError

#     except BadRequestError:
#         print(book+" Bad Request")
    
#     finally:
#         return tree

def getAvailBooks(book,url):
    # print("\n"+book)
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.find_all("table",{'class':'clsTab1'})
    for i in range(len(table)): 
        for tr in table[i].find_all('tr'):
            library = tr.contents[0].contents[0].string
            location = tr.contents[1].contents[0].string
            callNum = tr.contents[2].contents[0].string
            status = tr.contents[3].contents[0].string

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