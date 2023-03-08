import time
import requests
from multiprocessing import Pool
from multiprocessing import freeze_support
from bs4 import BeautifulSoup
from langconv import*


def get_link(link='https://www.69shu.com/37481/'):
    url = requests.get(link)
    # print(url.encoding) 輸出編碼
    url = url.text
    url = url.encode("ISO-8859-1")

    soup = BeautifulSoup(url, "html.parser")
    temp = soup.find("div", {"id": "catalog"})

    content_list_temp = temp.find_all("a")
    # print(temp)
    content_list = []
    for i in range(0, len(content_list_temp)):
        content_list.append(content_list_temp[i].get("href"))
    return content_list


def get_content(article_link='https://www.69shu.com/txt/35934/25197207'):

    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }

        url = requests.get(article_link, headers=headers)
        soup = BeautifulSoup(url.content, "html.parser")

        temp = soup.find('div', {"class": "txtnav"})

        temp.find("div", {"class": "txtinfo hide720"}).decompose()
        temp = temp.getText()
        temp = Converter('zh-hant').convert(temp)
        temp = temp.replace("\u2003", "")
        temp = temp.replace("\r", "")
        temp = temp.replace("                ", "")
        temp = temp.replace("(本章完)", "")
        temp = temp.replace("纔", "才").replace("羣", "群").replace("麪", "麵").replace("中文網\n", "\n").replace("茍","苟").replace("莪", "我").replace("模闆", "模板")
        temp_list = temp.split("\n")[6:]
        article = ""
        tempI = temp_list[0]
        for i in range(0, len(temp_list)):
            if temp_list[i] != "":
                article += temp_list[i] + "\n"

        time.sleep(0.1)

        article = article.split(tempI)[1]  # 避免章節重複
        article = tempI + "\n" + article

        return article

    except:{print(article_link)}



if __name__ == '__main__':

    freeze_support()
    menu_link = input("請輸入目錄網址:")

    article_link_list = get_link(menu_link)
    # print(article_link_list)

    name = input("請輸入書名：")
    output_file = open(r"%s.txt" % (name), mode='w', encoding='utf-8')

    pool = Pool(48)
    result = pool.map(get_content, article_link_list)
    pool.close()
    pool.join()

    for i in range(0, len(result)):
        print(result[i], file=output_file)

    output_file.close()































