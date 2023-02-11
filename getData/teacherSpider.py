# coding: utf-8
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse


if __name__ == '__main__':
    # colleges = readJson()
    url = 'https://cyber.seu.edu.cn/18201/list.htm'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/51.0.2704.63 Safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)
    res = urllib.request.urlopen(req)
    html = res.read()
    soup = BeautifulSoup(html, 'html.parser')
    class_a_tags = soup.select('.tc-ul')
    for tag in class_a_tags:
        link_tags = tag.select('a')
        for link_tag in link_tags:
            print(link_tag)
    pass