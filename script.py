from lxml import html
from lxml.etree import tostring
import requests

toRead = {
		 'Caraval':'http://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/ENQ/EXPNOS/BIBENQ?ENTRY=caraval&ENTRY_NAME=BS&ENTRY_TYPE=K&GQ=caraval&SORTS=SQL_REL_TITLE',
		 'A Conjuring Of Light':'http://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/FULL/EXPNOS/BIBENQ/12926382/198926227,1',
		 'Scythe':'http://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/ENQ/EXPNOS/BIBENQ?BRN=202733463'
		 }

libList = []


def getTree(str):
	page = requests.get(str)
	tree = html.fromstring(page.content)
	return tree
# to print entire tree
# print(tostring(tree))
d = {}
for book,url in toRead.items():
	print (book)
	tree = getTree(url)
	for table in tree.find_class('clsTab1'):
		avail = 0
		for tr in table.findall('tr'):
			td_list = tr.findall('td')
			if td_list != []:
				#index 0 is library
				#index 1 is location
				#index 2 is call number eg. English SHU
				#index 3 is status
				if td_list[3].text_content() == "Available":
					avail+=1
					print (td_list[0].text_content())
				# d[]=td_list[3].text_content()
	if avail == 0:
		print("None Available\n")
	else:
		print("\n")
# print(d)

# b = tree.xpath('//table[@class="clsTab1"]/text()')