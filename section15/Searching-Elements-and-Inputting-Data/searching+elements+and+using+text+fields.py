from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# driver = webdriver.Chrome('/Users/waqarjoyia/Downloads/chromedriver')
# Chrome 옵션 설정
options = Options()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
)
options.add_argument("disable-blink-features=AutomationControlled")  # 자동화 탐지 방지
options.add_experimental_option(
    "excludeSwitches", ["enable-automation"]
)  # 자동화 표시 제거
options.add_experimental_option(
    "useAutomationExtension", False
)  # 자동화 확장 기능 사용 안 함

# 웹드라이버 자동 설치 및 설정
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)


driver.get("https://www.google.com")

# search tag using id

search_bar = driver.find_element("id", "APjFqb")

# input data

search_bar.send_keys("I want to learn web scraping")


# submit the form

search_bar.submit()

sleep(10)

driver.close()
