
import requests
from bs4 import BeautifulSoup
import csv

def Gethtmltext(url , header):
    try:
        txt = requests.get(url, headers=header)
        txt.raise_for_status()
        txt.encoding = txt.apparent_encoding

        return txt.text
    except:
        return ''

def PTinfo(lit, url, header):
    html = Gethtmltext(url, header)
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('div', attrs={'class':'novellist'})
    for item in items:
        urls = item.find_all('a')
        for i in urls:
            url_a = 'https:' + i['href']
            lit.append([url_a, i.string])




if __name__ == '__main__':
    header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
              }
    url = 'https://www.biquge5200.com/xiaoshuodaquan/'
    infolist = []
    PTinfo(infolist, url, header)
    with open("alltext.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for i,j in infolist:
            writer.writerow([i, j])


