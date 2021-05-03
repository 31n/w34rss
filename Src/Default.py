import os
from bs4 import BeautifulSoup
import requests
from urllib import request
# import pydrive
import re
import json

log = True
# True/False
# True: Print log to Command line
# False: NOT print anything to Command line
mode = 'D'
# Debug/Release
# D: Debug mode(set variable from ".py")
# R: Release mode(set variable from ".json")
env = 'M'
# Environment mode
# W: Windows & export IIS folder
# M: macOS & Relative path


def main():
    if (log):
        extention = 'txt'
    else:
        extention = 'rss'
    if mode == 'D':
        if (log): print('DEBUG mode')
        company = 'ANA'
        newsUrl = 'https://jr-central.co.jp/news/'
        title = '全日本空輸株式会社'
        mainLink = 'https://www.ana.co.jp'
        linkSearch = '/news/release/'
        rssc(extention, company, newsUrl, title, mainLink, linkSearch)
    elif mode == 'R':
        if(log): print('RELEASE mode')
        jsonFile = open('Setting.json', 'r')
        jsonLoad = json.load(jsonFile)
        for site in jsonLoad.values():
            company = site['company']
            newsUrl = site['newsUrl']
            title = site['title']
            mainLink = site['mainLink']
            linkSearch = site['linkSearch']
            rssc(extention, company, newsUrl, title, mainLink, linkSearch)
    else:
        print('ERROR!!!')


def rssc(extention, company, newsUrl, title, mainLink, linkSearch):
    if(log): print('Now Processing ' + company + '...')
    if env == 'M':
        if(log): print('macOS mode')
        filePath = '../Result/' + company + '.' + extention
    elif env == 'W':
        if(log): print('Windows mode')
        filePath = 'C:\\inetpub\\wwwroot\\RSS\\' + company + '.' + extention

    ua = 'Mozilla/5.0 (X11; Linux x86_64) ' \
         'AppleWebKit/537.36 (KHTML, like Gecko) ' \
         'Chrome/51.0.2704.103 ' \
         'Safari/537.36'
    header = '<?xml version="1.0" encoding="UTF-8"?>\n' \
             '<rss version="2.0">\n' \
             '<channel>\n' \
             '<title>' + title + '</title>\n' \
                                 '<link>' + mainLink + '</link>\n' \
                                                       '<description>' + title + '</description>\n' \
                                                                                 '<language>ja</language>\n'
    footer = '</channel>\n' \
             '</rss>'

    response = requests.get(newsUrl, headers={"User-Agent": ua})
    soup = BeautifulSoup(response.content, 'lxml')

    newsTitle = soup.find_all(href=re.compile(linkSearch))
    # print(newsTitle)
    # newsDate = soup.find_all('p', class_='date')

    f = open(filePath, 'w')
    f.write(header)

    for i in range(len(newsTitle)):
        if (newsTitle[i].contents[0]):
            info = newsTitle[i].contents[0]
        else:
            info = newsTitle[i].string

        mainWrite = '<item>\n' \
                    '<title>' + info + '</title>\n' \
                                       '<description>' + info + '</description>\n' \
                                                                '<link>' + str(newsTitle[i]['href']) + '</link>\n' \
                                                                                                       '</item>\n'
        # print(str(i) + ' of ' + str(len(newsTitle)-4))
        f.write(mainWrite)

    # print(soup)
    # print(newsTitle[0])
    # print(newsTitle[0]).string
    # print(newsTitle[0]['href'])

    f.write(footer)
    f.close()


if __name__ == "__main__":
    main()
