import requests
from fake_useragent import UserAgent

# Background on user-agents

ua = UserAgent()

header = {"user-agent": ua.chrome}

page = requests.get("https://www.google.com", headers=header)
print(page.content)

# Background on Timeout

page = requests.get("https://www.google.com", timeout=3)  # 3초 타임아웃
