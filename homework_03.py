import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

# body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.number
# body-content > div.newest-list > div > table > tbody > tr:nth-child(3) > td.info > a.albumtitle.ellipsis
# body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis

songs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

# 지니뮤직의 1~50위 곡의 정보를 스크래핑 >> 스크래핑한 결과를 mongoDB 에 저장해보세요.
for song in songs:
    rank = song.select_one('td.number').text
    title = song.select_one('td.info > a.albumtitle.ellipsis').text
    artist = song.select_one('td.info > a.artist.ellipsis').text
    doc = {
        'rank': rank[0:2].rstrip(),'title' : title, 'artist' : artist
    }
    db.genie_chart.insert_one(doc)