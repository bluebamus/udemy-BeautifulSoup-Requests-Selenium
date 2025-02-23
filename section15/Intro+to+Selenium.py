from selenium import webdriver  # imports
from time import sleep
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# make a webdriver object   -    chrome driver path for my system -- >    /Users/waqarjoyia/Downloads/chromedriver


# driver = webdriver.Chrome('/Users/waqarjoyia/Downloads/chromedriver')

# Chrome 옵션 설정
options = Options()

# 웹드라이버 자동 설치 및 설정
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

# open some page using get method       - url -- > parameters

driver.get("https://www.facebook.com")

# driver.page_source

soup = BeautifulSoup(driver.page_source, "lxml")

print(soup.prettify())


# close webdriver object

driver.close()
