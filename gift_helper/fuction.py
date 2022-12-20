# -*- coding: UTF-8 -*-
import json
import random
from spider import PchomeSpider


def generate_title_file():
    gift_list = [{"name": "temp", "age": ["0:20歲以下", "1:20-40歲", "2:40歲以上"], "gender": ["0:男生", "1:女生"], "festival": ["0:父親節", "1:聖誕節", "2:母親節", "3:情人節", "4:紀念日"], "money": ["0:500以下", "1:500-1000", "2:1000-2000", "3:2000以上"]}]
    with open("gift_list.json", "w", encoding="utf8") as outfile:
        json.dump(gift_list, outfile, ensure_ascii=False)
    return "finish"


def read_gift_list():
    with open('gift_list.json', 'r', encoding="utf8") as openfile:
        # Reading from json file
        json_object = json.load(openfile)
    print(json_object)
    print(type(json_object))


def search_gift_list(age, gender, festival, money):
    available_gift = []
    with open('gift_list.json', 'r', encoding="utf8") as openfile:
        # Reading from json file
        data = json.load(openfile)
        for gift in data:
            if age in gift['age']:
                if gender in gift['gender']:
                    if festival in gift['festival']:
                        if money in gift['money']:
                            available_gift.append(gift['name'])
    gift = pick_available_gift(available_gift)
    return gift


def pick_available_gift(gift_list):
    amount = len(gift_list)
    pick = random.randint(1, amount)
    gift = gift_list[pick]
    return gift


def random_pick():
    age = random.randint(0, 2)
    gender = random.randint(0, 1)
    festival = random.randint(0, 4)
    money = random.randint(0, 2)
    random_gift = search_gift_list(age, gender, festival, money)
    return random_gift


def search_product(name):
    pchome_spider = PchomeSpider()
    all_product = pchome_spider.search_products(keyword=name)
    length = len(all_product)
    text_head = "幫你搜尋到%d項結果\n" % length
    text_body = ""
    for product in all_product:
        text_body += "名稱:%s" % product['name'] + " 價格:%d\n" % product['price']
    text = text_head +  text_body
    print(text)
    return text


if __name__ == "__main__":
    search_product('手機')
    # search_gift_list(0, 1, 1, 1)
    # read_gift_list()
    # generate_title_file()
