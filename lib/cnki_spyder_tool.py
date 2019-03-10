"""
Eng:
Refer to README.md for this module's function.
It relies on python modules below:
1. requests
2. bs4
you can easily get them using tool like pip.

中文：
这个模块的用途见 /doc/README.md。
它依赖于以下的Python模块：
1.requests
2.bs4
你可以使用像pip这样的工具容易地获取它们。
"""


import requests
from bs4 import BeautifulSoup

# ensure that you have installed python modules as above

import csv
import math
import time
import re


def get_doc_list(author):
    """
    it needs support of function:
    def get_next_page_doc_url_set(author_name,page_num,unit_name):
    to deal with the demond of page turning
    
    Args:
        author: a dictionary, has key "uname" and "univ"
       
    Returns:
        return list of author's doc.
        each doc contains doc's information described in README.md
    """

    start_time = time.time()

    headers = {
        "Host": "yuanjian.cnki.com.cn",
        "Connection": "keep-alive",
        "Content-Length": "63",
        "Cache-Control": "max-age=0",
        "Origin": "http://yuanjian.cnki.com.cn",
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer": "http://yuanjian.cnki.com.cn/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }

    cookies = {
        "UM_distinctid": "168ae2b533519-0c21eda9d60a5f-57b143a-ea600-168ae2b533827",
        "KEYWORD": "%E5%BC%A0%E4%B9%85%E7%8F%8D%24%E7%89%9B%E4%B8%BD%E6%85%A7%24%E7%9F%AD%E5%B0%8F%E8%8A%BD%E5%AD%A2%E6%9D%86%E8%8F%8C%E8%A1%A8%E8%BE%BE%E7%B3%BB%E7%BB%9F%E7%9A%84%E4%BC%98%E5%8C%96%E7%A0%94%E7%A9%B6",
        "SID": "110105",
        "CNZZDATA1257838124": "249878561-1549106680-%7C1549701224",
    }

    base_url = "http://yuanjian.cnki.net/Search/Result"

    data = {
        "searchType": "MulityTermsSearch",
        "Author": author["uname"],
        "Unit": author["univ"],
    }

    r = requests.post(base_url, cookies=cookies, headers=headers, data=data)

    bs = BeautifulSoup(r.text, "html.parser")

    total_count = int(bs.find("input", {"id": "hidTotalCount"})["value"])
    count_per_page = 20
    page_count = math.ceil(total_count / count_per_page)

    stop_time = time.time()

    print(author["uname"], author["univ"], page_count, stop_time - start_time)

    doc_list = list()
    for i in range(1, page_count + 1):
        # turn page and add urls of each page to doc_url_set
        doc_list.extend(get_doc_list_per_page(author, i))

    return doc_list


def get_doc_list_per_page(author, page_num):
    """    
    Args:
        author: a dictionary, has key "uname" and "univ"
        page_num: page number
        
    Return:
        return list of author's doc of specified page.
        each doc contains doc's information described in README.md
    """

    headers = {
        "Host": "yuanjian.cnki.com.cn",
        "Connection": "keep-alive",
        "Content-Length": "473",
        "Accept": "text/html, */*; q=0.01",
        "Origin": "http://yuanjian.cnki.com.cn",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36",
        "DNT": "1",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": "http://yuanjian.cnki.com.cn/Search/Result",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }

    cookies = {
        "UM_distinctid": "168ae2b533519-0c21eda9d60a5f-57b143a-ea600-168ae2b533827",
        "KEYWORD": "%E5%BC%A0%E4%B9%85%E7%8F%8D%24%E7%89%9B%E4%B8%BD%E6%85%A7%24%E7%9F%AD%E5%B0%8F%E8%8A%BD%E5%AD%A2%E6%9D%86%E8%8F%8C%E8%A1%A8%E8%BE%BE%E7%B3%BB%E7%BB%9F%E7%9A%84%E4%BC%98%E5%8C%96%E7%A0%94%E7%A9%B6",
        "SID": "110105",
        "CNZZDATA1257838124": "249878561-1549106680-%7C1549701224",
    }

    base_url = "http://yuanjian.cnki.net/Search/Result"

    data = {
        "searchType": "MulityTermsSearch",
        "Author": author["uname"],
        "ParamIsNullOrEmpty": "true",
        "Islegal": "false",
        "Order": "1",
        "Page": page_num,
        "Unit": author["univ"],
    }

    r = requests.post(base_url, cookies=cookies, headers=headers, data=data)

    bs = BeautifulSoup(r.text, "html.parser")

    doc_list = []

    item_list = bs.find("div", attrs={"class": "lplist"}).find_all(
        "div", attrs={"class": "list-item"}
    )
    for item in item_list:
        doc = {}

        try:
            doc_title = item.find("p", attrs={"class": "tit clearfix"}).a["title"].strip()
        except:
            doc_title = ""

        try:
            doc_url = item.find("p", attrs={"class": "tit clearfix"}).a["href"].strip()
        except:
            doc_url = ""
        
        try:
            journal_name = item.select("p.source > a > span")[0]["title"].strip()
        except:
            journal_name = ""
        
        try:
            journal_url = item.select("p.source > a")[0]["href"].strip()
        except:
            journal_url = ""

        try:
            download_num = item.select("div.info > p.info_right.right > span.time1")[0].string
            download_num = re.search("[0-9]+", download_num).group()
        except:
            download_num = ""


        try:
            refer_num = item.select("div.info > p.info_right.right > span.time2")[0].string
            refer_num = re.search("[0-9]+", refer_num).group()
        except:
            refer_num = ""

        try:
            author_name = item.select("p.source > span")[0]["title"].split(";")
            author_name = [name.strip() for name in author_name]
            author_name = (",").join(author_name)
        except:
            author_name = ""
        
        try:
            author_url = item.select("p.source > span > a")[0]["href"]
            start_index = author_url.find("=") + 1
            end_index = author_url.find("&")
            author_id = author_url[start_index:end_index].split("%3b")[:-1]
            author_id = (",").join(author_id)
        except:
            author_url = ""
            author_id = ""
        

        doc["doc_title"] = doc_title
        doc["doc_url"] = doc_url
        doc["author_name"] = author_name
        doc["author_id"] = author_id
        doc["author_url"] = author_url
        doc["journal_name"] = journal_name
        doc["journal_url"] = journal_url
        doc["download_num"] = download_num
        doc["refer_num"] = refer_num
        doc["uid"] = author["uid"]

        doc_list.append(doc)

    return doc_list


if __name__ == "__main__":
    tmp = {}
    tmp["uname"] = "王军"
    tmp["univ"] = "北京大学"
    get_doc_list(tmp)
    # get_doc_list_per_page(tmp,1)

