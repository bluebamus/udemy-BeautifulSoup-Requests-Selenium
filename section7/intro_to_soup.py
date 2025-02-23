from bs4 import BeautifulSoup


def read_file():
    file = open('intro_to_soup_html.html')
    data = file.read()
    file.close()
    return data

# Make soup
# Syntax = BeautifulSoup(html_data,parser)
# Our parser is lxml or html.parser which we have installed

html_file = read_file()


soup = BeautifulSoup(html_file,'lxml')# or for those who haven't installed lxml - BeautifulSoup(html_file,'html.parser')



# soup prettify

print(soup.prettify())

# identify tags