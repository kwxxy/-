import re
import requests


headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'}

def Gethttptxt(url):
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def Save_page(info, html):
    try:
        plt = re.findall(r'"view_price":"[\d\.]*"', html)
        tlt = re.findall(r'"raw_title":".*?"', html)
        for i in range(len(plt)):
            pirce = eval(plt[i].split(':')[1])
            title = eval(tlt[i].split(':')[1])
            info.append([pirce,title])
    except:
        print("")

def Printcc(info):
    tip = '{:4}\t{:8}\t{:16}'
    print(tip.format('序号', '价格', '商品名称'))
    count = 0
    for til in info:
        count += 1
        print(tip.format(count, til[0], til[1]))

if __name__ == '__main__':
    title = '书包'
    page = 2
    start_url = 'https://s.taobao.com/search?q='+ title
    infolist = []
    for i in range(page):
        try:
            url = start_url + '&s=' + str(page)
            html = Gethttptxt(url)
            Save_page(infolist, html)
        except:
            continue
        Printcc(infolist)



