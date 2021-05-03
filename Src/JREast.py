import os
from bs4 import BeautifulSoup
import requests
from urllib import request
# import pydrive

# filePath = '../Result/JREast.rss'
filePath = 'C:\inetpub\wwwroot\RSS\JREast.rss'
# filePath = 'https://drive.google.com/file/d/1TjuFaSd1iKe8nYG3sNMp_MVlsCDwajs0/view?usp=sharing'
url = 'https://www.jreast.co.jp/press/index.html/'
ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6)' \
     'AppleWebKit/605.1.15' \
     '(KHTML, like Gecko)' \
     'Version/14.0.1' \
     'Safari/605.1.15'
header = '<?xml version="1.0" encoding="UTF-8"?>\n'\
         '<rss version="2.0">\n' \
         '<channel>\n' \
         '<title>JR東日本：ホームページ</title>\n' \
         '<link>https://www.jreast.co.jp</link>\n' \
         '<description>JR東日本：ホームページ</description>\n' \
         '<language>ja</language>\n'
footer = '</channel>\n' \
         '</rss>'

response = requests.get(url, headers={"User-Agent": ua})
soup = BeautifulSoup(response.content, 'lxml')


newsTitle = soup.find_all('a', target='_blank')
newsDate = soup.find_all('p', class_='date')

f = open(filePath, 'w')
f.write(header)

for i in range(len(newsTitle)-3):
    mainWrite = '<item>\n' \
                '<title>'+str(newsTitle[i].string)+'</title>\n' \
                '<description>'+str(newsTitle[i].string)+'</description>\n' \
                '<link>' + str(newsTitle[i]['href']) + '</link>\n' \
                '</item>\n'
    # print(str(i) + ' of ' + str(len(newsTitle)-4))
    f.write(mainWrite)

# print(soup)
# print(newsTitle[0])
# print(newsTitle[0].string)
# print(newsTitle[0]['href'])

f.write(footer)
f.close()
