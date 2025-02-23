from bs4 import BeautifulSoup
import requests

url = "https://boston.craigslist.org/search/sof#search=2~thumb~0"

# Getting the webpage, creating a Response object.
response = requests.get(url)
data = response.text

soup = BeautifulSoup(data, "lxml")

tags = soup.find_all(class_="cl-static-search-result")
# for tag in tags:
#     print(tag.prettify())


for tag in tags:
    span_tag = tag.find(class_="title")
    if span_tag:
        text = span_tag.text.strip()
        print("Job:", text)

    a_tag = tag.find("a")
    if a_tag:
        link = a_tag.get("href")
        print("URL:", link)
    # print(tag.get("span"))
