import requests
from urllib.parse import urlencode
from requests import codes
import os,re
from hashlib import md5
from multiprocessing.pool import Pool
from configtoutiao import *

def get_page(offset,keyword):
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
        'from': 'search_tab'
    }
    base_url = 'https://www.toutiao.com/search_content/?'
    url = base_url + urlencode(params)
    try:
        resp = requests.get(url)
        if codes.ok == resp.status_code:
            return resp.json()
    except requests.ConnectionError:
        return None

def get_images_urls(json):
    if json.get('data'):
        data = json.get('data')
        for item in data:
            if item.get('cell_type') is not None:
                continue
            title = item.get('title')
            images = item.get('image_list')
            for image in images:
                image = image.get('url')
                image_pattern = re.compile('(.*?)pstatp.com/list/pgc-image/(\S+)')
                large_url = image_pattern.sub(r"\1pstatp.com/large/pgc-image/\2",image)
                #print(large_url)
                #https://p1.pstatp.com/large/pgc-image
                if large_url:
                    yield  {
                        'image':'https:'+large_url,
                        'title':title
                    }
##  这种爬取对于image_list里没有地址的图片就没法爬到了。

def save_image(url):
    img_path = KEYWORD + os.path.sep + url.get('title')
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    try:
        resp = requests.get(url.get('image'))
        if codes.ok == resp.status_code:
            file_path = img_path + os.path.sep + '{file_name}.{file_suffix}'.format(
                file_name=md5(resp.content).hexdigest(),
                file_suffix='jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(resp.content)
                print('Downloaded image path is %s' % file_path)
            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image，item %s' % url)



def main(offset):
    json = get_page(offset,KEYWORD)
    urls = get_images_urls(json)
    for url in urls:
        if '/list/' not in url.get('image'):
            print(r'我要看的', url)
            save_image(url)


GROUP_START = 0
GROUP_END = 20

if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()