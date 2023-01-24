# course: Web Scraping 101 with Python3 using REQUESTS, LXML & SPLASH - Section 7: API
import json
from pprint import pp
from urllib.parse import urljoin

import requests
from fake_useragent import UserAgent

ua = UserAgent()
extracted_product = []


def scraper(page_number=0):
    url = "https://www.walgreens.com/retailsearch/search/tier3"
    payload = json.dumps({
        "p": page_number,
        "s": 24,
        "view": "allView",
        "geoTargetEnabled": False,
        "deviceType": "mobile",
        "id": [
            "350006"
        ],
        "requestType": "tier3",
        "user_token": "zmnrkjc81cgrchzc3n3ht1pb",
        "sort": "Top Sellers",
        "storeId": "15196"
    })
    headers = {
        'content-type': 'application/json',
        'User-Agent': ua.random
    }

    response = requests.post(url, headers=headers, data=payload)

    data = response.json()

    try:
        products = data['products']

        for prod_info in products:
            prod = {
                'img': prod_info['productInfo']['imageUrl'],
                'price': prod_info['productInfo']['priceInfo']['regularPrice'],
                'id': prod_info['productInfo']['prodId'],
                'name': prod_info['productInfo']['productDisplayName'],
                'size': prod_info['productInfo']['productSize'],
                'url': urljoin(base='https://www.walgreens.com/', url=prod_info['productInfo']['productURL'])
            }
            extracted_product.append(prod)
        page_number += 1
        print(page_number)
        scraper(page_number=page_number)
    except KeyError:
        return


def write_to_json(filename, data):
    f = open(filename, 'w')
    f.write(json.dumps(data))
    f.close()

scraper()
pp(extracted_product)
write_to_json('../ext_product.json', extracted_product)
