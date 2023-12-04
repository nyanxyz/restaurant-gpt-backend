from bs4 import BeautifulSoup
import requests


def attach_eul_reul(word):
    if "가" <= word[-1] <= "힣":
        last_char = ord(word[-1]) - ord("가")
        # 28로 나눈 나머지가 0이면 받침이 없는 것
        if last_char % 28 == 0:
            return word + "를"
        else:
            return word + "을"
    else:
        return word + "(을/를)"


def get_url_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    iframes = soup.find("iframe")

    if iframes is None:
        return None

    iframe_url = iframes.get("src")
    response = requests.get("https://blog.naver.com" + iframe_url)
    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.find("div", class_="se-main-container")

    if content is None:
        return None

    content = "\n".join(line for line in content.text.split("\n") if line.strip())

    return content
