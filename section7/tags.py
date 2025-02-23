from bs4 import BeautifulSoup


def read_file():
    file = open('tags.html')
    data = file.read()
    file.close()
    return data

soup = BeautifulSoup(read_file(),'lxml')


# Accessing tags

meta = soup.meta


# tag methods
'''

name
-- attributes
.get() method
dictionary

'''

# modify attributes

body = soup.body

body['style'] = 'some style'


'''
 Multi valued attributes

'''


print(body['class'])