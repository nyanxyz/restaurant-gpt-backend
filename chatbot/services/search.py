import urllib.request
import urllib.parse
import json
import os

client_id = os.environ["NAVER_CLIENT_ID"]
client_secret = os.environ["NAVER_CLIENT_SECRET"]


def local_search(query):
    encoded_query = urllib.parse.quote(query)
    url = (
        "https://openapi.naver.com/v1/search/local?display=5&sort=comment&query="
        + encoded_query
    )

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    response = urllib.request.urlopen(request)
    status = response.getcode()

    if status == 200:
        response_body = response.read()
        return json.loads(response_body.decode("utf-8"))
    else:
        raise f"Error: {status} 에러가 발생했습니다. (local_search)"


def blog_search(query):
    encoded_query = urllib.parse.quote(query)
    url = "https://openapi.naver.com/v1/search/blog?display=3&query=" + encoded_query

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    response = urllib.request.urlopen(request)
    status = response.getcode()

    if status == 200:
        response_body = response.read()
        return json.loads(response_body.decode("utf-8"))
    else:
        raise f"Error: {status} 에러가 발생했습니다. (blog_search)"
