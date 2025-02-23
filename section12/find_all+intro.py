from bs4 import BeautifulSoup



def read_file():
    file = open('three_sisters.html')
    data = file.read()
    file.close()
    return data

soup = BeautifulSoup(read_file(),'lxml')

# Signature: find_all(name, attrs, recursive, string, limit, **kwargs)

# name parameter


# regex object - string - True - function

a_tags = soup.find_all('a')


# attrs parameter

# dicitonary

attr = {'class':'story'}
first_a = soup.find_all(attrs=attr)
#print(first_a)


# limit parameter

a_tags = soup.find_all('a',limit=2)
print(a_tags)