import requests
import xml.etree.ElementTree as ET

mybooks = {}

def getGoodreadsToReadList(userid):
    with open('key.txt', 'r') as f:
        key = f.readline()
    file = open('toread.txt', 'w') 
    
    reqtoreadshelf ="https://www.goodreads.com/review/list?id={}&shelf=to-read&key={}&page=1&per_page=200".format(userid,key) 
    r = requests.get(reqtoreadshelf)
    tree = ET.fromstring(r.content)

    books = tree[1]
    booklist = []
    # file.write("isbn, isbn13, title\n")
    for i in range(len(books)):
        isbn = books[i][1].text
        isbn13 = books[i][2].text
        title = books[i][5].text
        booklist.append([isbn13, title])
        file.write('{};{};{}\n'.format(isbn, isbn13, title))
    return booklist
# print(getGoodreadsToReadList('w'))
getGoodreadsToReadList('13399356')

class NewArrival:
    def __init__(self, title, isbn, lang, fiction, branchCode):
        self.title = title
        self.isbn = isbn
        self.lang = lang
        self.fiction = fiction
        self.branchCode = branchCode

    def getFiction(self):
        if self.fiction == 'N':
            return False
        return True

    def isEnglish(self):
        if self.lang == 'English':
            return True
        return False

    def __str__(self):
        return "{:30s} | {:20s} |{}({})".format(self.title, self.branchCode, self.lang, self.fiction)

def getNewArrivals():
#http://eservice.nlb.gov.sg/rss/libraries/
    newBooks = []
    r = requests.get("http://www.nlb.gov.sg/newarrivals/rss/")
    tree = ET.fromstring(r.content)
    channel = tree[0]
    for i in range(7, len(channel)):
        item = channel[i]
        title = item[0].text
        isbn = item[2].text
        lang = item[7].text #Chinese, English
        fiction = item[8].text # Y or N 
        branchCode = item[12].text
        book = NewArrival(title, isbn, lang, fiction, branchCode)
        newBooks.append(book)

    for i in newBooks:
        if i.getFiction() and i.isEnglish():
            print(i)

# getNewArrivals()


"""
Data for GoodReads Book
0 <Element 'id' at 0x00000198B5E0B908>
1 <Element 'isbn' at 0x00000198B5E0B958>
2 <Element 'isbn13' at 0x00000198B5E0B9A8>
3 <Element 'text_reviews_count' at 0x00000198B5E0BB38>
4 <Element 'title' at 0x00000198B5E0BB88>
5 <Element 'title_without_series' at 0x00000198B5E0BBD8>
6 <Element 'image_url' at 0x00000198B5E0BC28>
7 <Element 'small_image_url' at 0x00000198B5E0BC78>
8 <Element 'large_image_url' at 0x00000198B5E0BCC8>
9 <Element 'link' at 0x00000198B5E0BD18>
10 <Element 'num_pages' at 0x00000198B5E0BD68>
11 <Element 'format' at 0x00000198B5E0BDB8>
12 <Element 'edition_information' at 0x00000198B5E0BE08>
13 <Element 'publisher' at 0x00000198B5E0BE58>
14 <Element 'publication_day' at 0x00000198B5E0BEA8>
15 <Element 'publication_year' at 0x00000198B5E0BEF8>
16 <Element 'publication_month' at 0x00000198B5E0BF48>
17 <Element 'average_rating' at 0x00000198B5E0BF98>
18 <Element 'ratings_count' at 0x00000198B5E2D048>
19 <Element 'description' at 0x00000198B5E2D098>
20 <Element 'authors' at 0x00000198B5E2D138>
21 <Element 'published' at 0x00000198B5E2D4A8>
22 <Element 'work' at 0x00000198B5E2D4F8>


Data for NLB RSS New Arrivals
0 <Element 'title' at 0x00000198B5E2DB38>
1 <Element 'link' at 0x00000198B5E2DBD8>
2 <Element 'isbn' at 0x00000198B5E2DC28>
3 <Element 'description' at 0x00000198B5E2DC78>
4 <Element 'publisher' at 0x00000198B5E2DCC8>
5 <Element 'mediaDesc' at 0x00000198B5E2DD18>
6 <Element 'author' at 0x00000198B5E2DD68>
7 <Element 'language' at 0x00000198B5E2DE08>
8 <Element 'fiction' at 0x00000198B5E2DEF8>
9 <Element 'subject' at 0x00000198B5E2DF48>
10 <Element 'locationCode' at 0x00000198B5E2DF98>
11 <Element 'locationDesc' at 0x00000198B5E31048>
12 <Element 'branchCode' at 0x00000198B5E31098>
13 <Element 'branchName' at 0x00000198B5E310E8>
14 <Element 'imageStatusL' at 0x00000198B5E31188>
15 <Element 'imageStatusM' at 0x00000198B5E311D8>
16 <Element 'imageStatusS' at 0x00000198B5E31228>
"""