# 필요한 라이브러리들을 임포트
from bs4 import BeautifulSoup  # HTML 파싱을 위한 라이브러리
from selenium import webdriver  # 웹 브라우저 자동화를 위한 Selenium WebDriver
from time import sleep  # 실행 중 잠시 대기(sleep)하기 위한 모듈
from xlsxwriter import Workbook  # 엑셀 파일 작성을 위한 라이브러리
import os  # 운영체제 관련 기능(파일 및 폴더 관리 등)을 위한 모듈
import requests  # HTTP 요청을 보내기 위한 라이브러리
import shutil  # 파일 복사 및 이동 등의 작업을 위한 모듈
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# Instagram 이미지 및 캡션 스크래핑을 위한 App 클래스 정의
class App:
    def __init__(
        self,
        username="dataminer2060",
        password="WebScraper",
        target_username="dataminer2060",
        path="/Users/Lazar/Desktop/instaPhotos",
    ):
        """
        클래스 초기화 메소드
        :param username: Instagram 로그인 시 사용할 사용자 이름
        :param password: Instagram 로그인 시 사용할 비밀번호
        :param target_username: 스크래핑 대상 Instagram 계정의 사용자 이름
        :param path: 다운로드 받은 이미지와 캡션을 저장할 로컬 디렉토리 경로
        """
        self.username = username
        self.password = password
        self.target_username = target_username
        self.path = path
        # Chrome 옵션 설정
        self.options = Options()
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
        )
        self.options.add_argument(
            "disable-blink-features=AutomationControlled"
        )  # 자동화 탐지 방지
        self.options.add_experimental_option(
            "excludeSwitches", ["enable-automation"]
        )  # 자동화 표시 제거
        self.options.add_experimental_option(
            "useAutomationExtension", False
        )  # 자동화 확장 기능 사용 안 함

        # 웹드라이버 자동 설치 및 설정
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=self.options
        )
        # ChromeDriver의 경로를 지정하여 Selenium WebDriver 객체 생성
        # self.driver = webdriver.Chrome(
        #     "/Users/Lazar/Downloads/chromedriver"
        # )  # ChromeDriver 경로를 실제 환경에 맞게 수정해야 함.
        self.error = False
        self.main_url = "https://www.instagram.com"
        self.all_images = []  # 스크래핑한 이미지 정보를 저장할 리스트

        # Instagram 메인 페이지 접속
        self.driver.get(self.main_url)
        sleep(3)  # 페이지 로딩을 위해 잠시 대기

        # 로그인 시도
        self.log_in()

        # 로그인 성공 여부에 따라 이후 동작 수행
        if self.error is False:
            self.close_dialog_box()  # 로그인 후 나타나는 팝업창 닫기
            self.open_target_profile()  # 타겟 프로필로 이동

        if self.error is False:
            self.scroll_down()  # 페이지 스크롤을 통해 모든 이미지 로드

        if self.error is False:
            # 저장할 폴더가 없으면 생성
            if not os.path.exists(path):
                os.mkdir(path)
            self.downloading_images()  # 이미지 및 캡션 다운로드

        sleep(3)  # 다운로드 완료 후 잠시 대기
        self.driver.close()  # 브라우저 종료

    def write_captions_to_excel_file(self, images, caption_path):
        """
        스크래핑한 이미지의 캡션들을 엑셀 파일에 저장하는 함수
        :param images: 스크래핑한 이미지 데이터 (HTML 태그 객체 리스트)
        :param caption_path: 캡션 파일을 저장할 폴더 경로
        """
        print("writing to excel")
        # 엑셀 파일 생성 (경로와 파일명 지정)
        workbook = Workbook(os.path.join(caption_path, "captions.xlsx"))
        worksheet = workbook.add_worksheet()

        row = 0
        # 첫 번째 행에 헤더 작성
        worksheet.write(row, 0, "Image name")  # 이미지 파일 이름
        worksheet.write(row, 1, "Caption")  # 이미지 캡션
        row += 1

        # 각 이미지에 대해 파일 이름과 캡션 저장
        for index, image in enumerate(images):
            filename = "image_" + str(index) + ".jpg"
            try:
                caption = image["alt"]  # 이미지 태그의 alt 속성에서 캡션 추출
            except KeyError:
                caption = "No caption exists"  # 캡션이 없을 경우 처리
            worksheet.write(row, 0, filename)
            worksheet.write(row, 1, caption)
            row += 1

        workbook.close()  # 엑셀 파일 저장 및 종료

    def download_captions(self, images):
        """
        캡션들을 다운로드(저장)하는 함수
        :param images: 스크래핑한 이미지 데이터 (HTML 태그 객체 리스트)
        """
        # 캡션 파일을 저장할 하위 폴더 생성 (존재하지 않으면)
        captions_folder_path = os.path.join(self.path, "captions")
        if not os.path.exists(captions_folder_path):
            os.mkdir(captions_folder_path)
        # 캡션들을 엑셀 파일로 저장
        self.write_captions_to_excel_file(images, captions_folder_path)

        # 아래 주석 처리된 코드는 각 캡션을 개별 텍스트 파일로 저장하는 대체 방식임.
        """
        for index, image in enumerate(images):
            try:
                caption = image['alt']
            except KeyError:
                caption = 'No caption exists for this image'
            file_name = 'caption_' + str(index) + '.txt'
            file_path = os.path.join(captions_folder_path, file_name)
            link = image['src']
            with open(file_path, 'wb') as file:
                file.write(str('link:' + str(link) + '\n' + 'caption:' + caption).encode())
        """

    def downloading_images(self):
        """
        스크래핑한 이미지들을 로컬에 다운로드하는 함수
        """
        # 중복 이미지 제거를 위해 set() 사용 후 다시 list로 변환
        self.all_images = list(set(self.all_images))
        # 캡션 다운로드 함수 호출
        self.download_captions(self.all_images)
        print("Length of all images", len(self.all_images))
        # 각 이미지에 대해 다운로드 진행
        for index, image in enumerate(self.all_images):
            filename = "image_" + str(index) + ".jpg"
            image_path = os.path.join(self.path, filename)
            link = image["src"]  # 이미지 URL
            print("Downloading image", index)
            response = requests.get(
                link, stream=True
            )  # 이미지 데이터를 스트림 방식으로 요청
            try:
                # 파일 쓰기를 통해 이미지 저장
                with open(image_path, "wb") as file:
                    shutil.copyfileobj(
                        response.raw, file
                    )  # 응답 데이터를 파일에 복사 (원본 → 대상)
            except Exception as e:
                print(e)
                print("Could not download image number ", index)
                print("Image link -->", link)

    def scroll_down(self):
        """
        Instagram 페이지를 스크롤 다운하여 더 많은 이미지를 로드하는 함수
        """
        try:
            # 페이지 상단에 표시된 포스트 수 가져오기
            no_of_posts = self.driver.find_element_by_xpath(
                '//span[text()=" posts"]'
            ).text
            no_of_posts = no_of_posts.replace(" posts", "")
            no_of_posts = str(no_of_posts).replace(",", "")  # 예: "15,483" -> "15483"
            self.no_of_posts = int(no_of_posts)
            # 포스트 수가 12개 이상인 경우 스크롤 횟수 계산 (한 번에 12개씩 로드한다고 가정)
            if self.no_of_posts > 12:
                no_of_scrolls = int(self.no_of_posts / 12) + 3  # 추가 스크롤을 위해 +3
                try:
                    for value in range(no_of_scrolls):
                        # 현재 페이지의 HTML 소스 가져와서 BeautifulSoup으로 파싱
                        soup = BeautifulSoup(self.driver.page_source, "lxml")
                        # 모든 이미지 태그를 찾아 리스트에 추가
                        for image in soup.find_all("img"):
                            self.all_images.append(image)
                        # 자바스크립트를 이용하여 페이지 하단으로 스크롤
                        self.driver.execute_script(
                            "window.scrollTo(0, document.body.scrollHeight);"
                        )
                        sleep(2)  # 스크롤 후 로딩 대기
                except Exception as e:
                    self.error = True
                    print(e)
                    print("Some error occurred while trying to scroll down")
            sleep(10)  # 모든 스크롤 후 추가 대기 (이미지 로딩을 위한 시간)
        except Exception:
            print("Could not find no of posts while trying to scroll down")
            self.error = True

    def open_target_profile(self):
        """
        타겟 사용자의 프로필 페이지로 이동하는 함수
        """
        try:
            # 검색창 요소 찾기 (Instagram 검색창)
            search_bar = self.driver.find_element_by_xpath(
                '//input[@placeholder="Search"]'
            )
            search_bar.send_keys(self.target_username)  # 타겟 사용자 이름 입력
            target_profile_url = (
                self.main_url + "/" + self.target_username + "/"
            )  # 타겟 프로필 URL 생성
            self.driver.get(target_profile_url)  # 타겟 프로필 페이지로 이동
            sleep(3)  # 페이지 로딩 대기
        except Exception:
            self.error = True
            print("Could not find search bar")

    def close_dialog_box(self):
        """
        로그인 후 나타나는 대화상자(팝업)를 닫는 함수
        """
        # 현재 페이지를 다시 로드하여 팝업 발생을 최소화
        sleep(2)
        self.driver.get(self.driver.current_url)
        sleep(3)
        try:
            sleep(3)
            # "Not Now" 버튼을 찾아 클릭하여 팝업 창 닫기
            not_now_btn = self.driver.find_element_by_xpath('//*[text()="Not Now"]')
            sleep(3)
            not_now_btn.click()
            sleep(1)
        except Exception:
            # 만약 해당 팝업이 없으면 예외 발생을 무시
            pass

    def close_settings_window_if_there(self):
        """
        설정 창(다른 브라우저 탭 또는 팝업)이 열려있을 경우 이를 닫는 함수
        """
        try:
            # 두 번째 창(탭)이 열려 있다면 해당 창을 닫고, 다시 첫 번째 창으로 전환
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        except Exception as e:
            # 예외 발생 시 무시 (설정 창이 없는 경우)
            pass

    def log_in(self):
        """
        Instagram 로그인 과정을 수행하는 함수
        """
        print("log_in start")
        try:
            # "Log in" 링크를 찾아 클릭하여 로그인 페이지로 이동
            # log_in_button = self.driver.find_element_by_link_text("Log in")
            # log_in_button.click()
            sleep(3)
        except Exception:
            self.error = True
            print("Unable to find login button")
        else:
            try:
                # 사용자명 입력 필드 찾기 (전화번호, 사용자 이름 또는 이메일 입력란)
                # user_name_input = self.driver.find_element(
                #     "xpath", '//*[@id="loginForm"]/div[1]/div[1]/div/label/input'
                # )
                # user_name_input.send_keys(self.username)  # 사용자명 입력
                # sleep(1)
                # 웹 요소 찾기
                elements = self.driver.find_elements(
                    By.XPATH, '//*[@id="loginForm"]/div[1]/div[1]/div/label/input'
                )

                # 요소가 존재하는지 확인하여 출력
                if elements:
                    print("XPath exists on the page.")
                else:
                    print("XPath does not exist on the page.")

                user_name_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="loginForm"]/div[1]/div[1]/div/label/input')
                    )
                )
                user_name_input.send_keys(self.username)

                # 비밀번호 입력 필드 찾기
                # password_input = self.driver.find_element(
                #     "xpath", '//*[@id="loginForm"]/div[1]/div[2]/div/label/input'
                # )
                # password_input.send_keys(self.password)  # 비밀번호 입력
                # sleep(1)
                password_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="loginForm"]/div[1]/div[2]/div/label/input')
                    )
                )
                password_input.send_keys(self.password)

                # 사용자명 입력 필드에서 제출(submit)하여 로그인 요청 전송
                # user_name_input.submit()
                # sleep(1)
                bt_click = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="loginForm"]/div[1]/div[2]/div/label/input')
                    )
                )
                login_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="loginForm"]/div[1]/div[3]/button')
                    )
                )
                login_button.click()

                # 로그인 후 다른 창이 뜨면 닫기
                self.close_settings_window_if_there()
            except Exception:
                print(
                    "Some exception occurred while trying to find username or password field"
                )
                self.error = True


# 메인 실행부: 이 스크립트가 직접 실행될 경우 App 클래스를 인스턴스화하여 전체 과정을 시작
if __name__ == "__main__":
    app = App()

# -------------------------------------------------------------------------------
# 추가 참고 사항:
# 1. 이 코드는 Instagram의 웹 인터페이스를 기반으로 작성되었습니다.
#    Instagram은 자주 업데이트되므로 XPath나 페이지 구조가 변경될 수 있으며,
#    이 경우 코드는 정상적으로 작동하지 않을 수 있습니다.
#
# 2. Instagram의 서비스 약관(Terms of Service)을 위반하지 않도록 주의해야 합니다.
#    특히, 대량의 데이터 스크래핑은 계정 정지 등의 제재를 받을 수 있으므로 실제 사용 시
#    Instagram API 사용이나 합법적인 방법을 고려하시기 바랍니다.
#
# 3. Selenium WebDriver 사용 시, ChromeDriver의 버전과 Chrome 브라우저의 버전이 일치해야 합니다.
#    해당 경로와 버전을 정확히 확인하고 설정하시기 바랍니다.
#
# 4. sleep() 함수를 사용하여 페이지 로딩 및 이미지 로드를 위한 충분한 대기 시간을 제공하고 있습니다.
#    네트워크 상황에 따라 이 시간은 조정이 필요할 수 있습니다.
#
# 5. 코드는 에러 발생 시 간단한 예외 처리를 하고 있으나,
#    실제 프로젝트에서는 보다 정교한 예외 처리 및 로깅을 구현하는 것이 좋습니다.
# -------------------------------------------------------------------------------
