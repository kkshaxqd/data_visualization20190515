import json
import os
import re
from urllib.parse import urlencode
import pymongo
import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
from requests import codes
from multiprocessing import Pool
from hashlib import md5
from configtoutiao import *

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36',
}

path = "E:\haxqd\python\data_visualization\Spider_repository\Spider_Study" + "\\" + KEYWORD
def dirpathcheck():
    if os.path.exists(path):
        os.chdir(path)
    else:
        os.mkdir(path)



client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]


def get_page_index(offset, keyword):
    data = {
        'autoload': 'true',
        'from':'search_tab',
        'count': 20,
        'cur_tab': 1,
        'format': 'json',
        'keyword': keyword,
        'offset': offset,
    }
    params = urlencode(data)
    base = 'http://www.toutiao.com/search_content/'
    url = base + '?' + params
    try:
        response = requests.get(url)
        if codes.ok == response.status_code:
            return response.json()
    except ConnectionError:
        print('Error occurred')
        return None

def parse_page_index(json):
    if json.get('data'):
        data = json.get('data')
        for item in data:
            if item.get('cell_teype') is not None:
                continue
            title = item.get('title')
            images = item.get('image_list')
            for image in images:
                yield {
                    'image': 'https:'+image.get('url'),
                    'title': title
                }



def save_image(content):
    #md5.hexdigest() 返回内容的16进制md5码，用来判断内容是否重复，重复应该会被覆盖掉，这样保证结果内容是唯一的。
    file_path = '{0}/{1}.{2}'.format(path, md5(content).hexdigest(), 'jpg')
    print(file_path)
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()

def download_image(url):
    print('Downloading', url)
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except ConnectionError:
        return None

def get_page_detail(url):
    print(url)
    try:
        response = requests.get(url,headers=headers)
        print(response)
        if response.status_code == 200:
            return response.text
        return None
    except:
        print('Error get_page_detail')
        return None

def parse_page_detail(html, url):
    try:
        soup = BeautifulSoup(html, 'lxml')
    except TypeError:
        return None
    #寻找标题
    result = soup.select('title')
    title = result[0].get_text() if result else "title not exist"
    # 寻找图片内容
    images_pattern = re.compile('gallery: JSON.parse\("(.*)"\)', re.S)
    result = re.search(images_pattern, html)
    if result:
        data = json.loads(result.group(1).replace('\\', ''))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for image in images: download_image(image)
            return {
                'title': title,
                'url': url,
                'images': images
            }



def save_to_mongo(result):
    if db[MONGO_TABLE].update(result,upsert=True):
        print('Successfully Saved to Mongo', result)
        return True
    else:
        return False


def main(offset):
    dirpathcheck()
    json = get_page_index(offset, KEYWORD)
    urls = parse_page_index(json)
    for url in urls.get('image'):
        html = get_page_detail(url)
        result = parse_page_detail(html, url)
        if result: save_to_mongo(result)


if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()








