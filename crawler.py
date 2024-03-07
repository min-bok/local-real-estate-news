import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def get_now_date():
    now = datetime.today()
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)
    return "-".join([year, month, day])

def get_src(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 오류 발생시 예외처리
    response.encoding = None
    soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')
    return soup

# 부동산 일반 뉴스
def get_general():
    url = "https://sedaily.com/NewsList/GB07"
    soup = get_src(url)

    news_list = soup.select('.sub_news_list li')

    data = []  # 각 기사 정보를 저장할 리스트

    for news in news_list:
        title = news.select_one(".article_tit").get_text().strip()  # 기사 제목
        date = news.select_one(".text_info > .date").get_text().strip()  # 기사 작성일

        if news.select_one('.thumb img') is not None:
            thumb = news.select_one('.thumb img')['src']  # 기사 썸네일
        else:
            thumb = 'none'
        link = news.select_one("a")['href']  # 기사 링크

        # 리스트에 기사 정보를 추가
        data.append({"title": title, "date": date, "thumb": thumb, "link": link})

    # DataFrame으로 변환
    df = pd.DataFrame(data)

    file_name = get_now_date()  # 파일 저장명

    df.to_excel(f"newsData/general/{file_name}.xlsx", index=False)

    print("일반 뉴스 수집 완료")

get_general()

