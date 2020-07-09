import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import json

""" create folder if not create yet """
def create_folder(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def get_beautytifulsoup(web_url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=web_url, headers=headers)
    html = urllib.request.urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')
    return bs


""" for get popular hashtag in instagram """
def crawler(bs, rank_dict):

    i_rows = bs.find('ul', 'i-group').find_all('li')
    for row in i_rows:
        rank_num = row.find_all('div', 'i-num')
        hashtag_txt = row.find_all('a')
        print(rank_num[0].text, hashtag_txt[0].text)
        rank_dict[rank_num[0].text] = hashtag_txt[0].text
    return rank_dict


def main(target_number):
    assert target_number>99 and target_number%100 ==0
    # get all page urls.
    main_page = "https://top-hashtags.com/instagram/"

    print("\
        This crawler will download the rank of instagram hashtag, \
        we choose 'https://top-hashtags.com/instagram/' as our data source. , \
         ")

    urls_list = [main_page]
    for i in range(1, target_number//100):
        urls_list.append(main_page+"{}01/".format(i))

    print("\nStart crawling...")
    rank_dict = {}
    for i, web_url in enumerate(urls_list):
        bs = get_beautytifulsoup(web_url)
        rank_dict = crawler(bs, rank_dict)
        print("finish rank {}~{}.".format(i*100, i*100+99))

    with open("instagram_rank.json", "w") as fjson:
        fjson.write(json.dumps(rank_dict, indent=2))

if __name__ == "__main__":
    main(3000)


