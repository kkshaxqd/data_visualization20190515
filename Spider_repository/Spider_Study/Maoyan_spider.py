#https://github.com/Germey/MaoYan/blob/master/spider.py
import json
from multiprocessing import Pool
import requests
from requests.exceptions import RequestException
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36',
}
###原来不能爬取是,headers=headers没有加这个，就不能识别网页
def get_one_page(url):
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == requests.codes.ok:
            return response.text
        else:
            return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(\d+)</i>'
        '.*?<img data-src="(.*?)"'
        '.*?class="name"><a.*?>(.*?)</a>'
        '.*?class="star">(.*?)</p>'
        '.*?class="releasetime">(.*?)</p>'
        '.*?class="score"><i class="integer">(.*?)</i><i class="fraction">(.*?)</i>'
        '.*?</dd>', re.S)
    patterraw = re.compile(
        '<dd>.*?board-index.*?>(\d+)</i>'
        '.*?data-src="(.*?)"'
        '.*?name"><a.*?>(.*?)</a>'
        '.*?star">(.*?)</p>'
        '.*?releasetime">(.*?)</p>'
        '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>'
        '.*?</dd>', re.S)
    items = re.findall(patterraw, html)
    print(items)
    for item in items:
        ## yield 类似return，不过返回的是生成器
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5]+item[6]
        }

def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n') #ensure_ascii=False为了输出中文，json.dumps转化成json格式
        f.close()

def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i*10 for i in range(10)])
    pool.close()
    pool.join()