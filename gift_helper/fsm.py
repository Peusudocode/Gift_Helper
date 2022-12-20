# -*- coding: UTF-8 -*-
from transitions.extensions import GraphMachine
from utils import send_text_message, send_carousel_message, send_button_message, send_image_message
import requests
from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction
from fuction import search_gift_list, random_pick, search_product
# global variable
start = 0
# 0:20歲以下, 1:20-40歲, 2:40歲以上
age = 0
# 0:男生, 1:女生
gender = 0
# 0:父親節, 1:聖誕節, 2:母親節, 3:情人節, 4:紀念日
festival = 0
# 0:500以下, 1:500-1000, 2:1000-2000, 3:2000以上
money = 0


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_introduction(self, event):
        text = event.message.text
        return text.lower() == "介紹"

    def on_enter_introduction(self, event):
        print("on_enter\n")
        text = '歡迎使用禮物挑選小幫手。\n輸入『開始挑選』就會問你問題，給你禮物建議。' \
               '\n輸入『重新開始』就能重新開始\n輸入『查詢__』就可以自動幫你搜尋物品名稱與價格。\n輸入『隨機挑選』就可以隨機給你禮物建議。'
        send_text_message(event.reply_token, text)
        self.go_back()

    def is_going_to_start_query(self, event):
        text = event.message.text
        return text.lower() == "開始挑選"

    def on_enter_start_query(self, event):
        title = '請先提供您的基本資訊'
        text = '請問你要送禮對象得年齡範圍'
        btn = [
            MessageTemplateAction(
                label='20歲以下',
                text='20歲以下'
            ),
            MessageTemplateAction(
                label='20-40歲',
                text='20-40歲'
            ),
            MessageTemplateAction(
                label='40歲以上',
                text='40歲以上'
            ),
        ]
        url = 'https://i.imgur.com/kDBm8JP.png'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_input_age(self, event):
        global age
        text = event.message.text
        if text == '20歲以下' or text == '0':
            age = 0
            return True
        elif text == '20-40歲' or text == '1':
            age = 1
            return True
        elif text == '40歲以上' or text == '2':
            age = 2
            return True
        elif text == '重新開始' or text == '-1':
            self.go_back(event)
        else:
            return False

    def on_enter_input_age(self, event):
        title = '請先提供您的基本資訊'
        text = '請問你要送禮對象的性別'
        btn = [
            MessageTemplateAction(
                label='男',
                text='男'
            ),
            MessageTemplateAction(
                label='女',
                text='女'
            ),
        ]
        url = 'https://i.imgur.com/TlNLMtX.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_input_gender(self, event):
        global gender
        text = event.message.text
        if text == '男' or text == '0':
            gender = 0
            return True
        elif text == '女' or text == '1':
            gender = 1
            return True
        elif text == '重新開始' or text == '-1':
            self.go_back(event)
        else:
            return False

    def on_enter_input_gender(self, event):
        text = '請輸入你要送禮的日子\n父親節\n母親節\n聖誕節\n情人節\n紀念日'
        send_text_message(event.reply_token, text)

    def is_going_to_input_festival(self, event):
        global festival
        text = event.message.text
        if text == '紀念日' or text == '4':
            festival = 4
            return True
        elif text == '情人節' or text == '3':
            festival = 3
            return True
        elif text == '母親節' or text == '2':
            festival = 2
            return True
        elif text == '聖誕節' or text == '1':
            festival = 1
            return True
        elif text == '父親節' or text == '0':
            festival = 0
            return True
        elif text == '重新開始' or text == '-1':
            self.go_back(event)
        else:
            return False

    def on_enter_input_festival(self, event):
        title = '請先提供您的基本資訊'
        text = '請問你的禮物價格範圍'
        btn = [
            MessageTemplateAction(
                label='500以下',
                text='500以下'
            ),
            MessageTemplateAction(
                label='500-1000',
                text='500-1000'
            ),
            MessageTemplateAction(
                label='1000-2000',
                text='1000-2000'
            ),
            MessageTemplateAction(
                label='2000以上',
                text='2000以上'
            ),
        ]
        url = 'https://i.imgur.com/Hdpol7S.png'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_input_money(self, event):
        global money
        text = event.message.text
        if text == '500以下' or text == '0':
            money = 0
            return True
        elif text == '500-1000' or text == '1':
            money = 1
            return True
        elif text == '1000-2000' or text == '2':
            money = 2
            return True
        elif text == '2000以上' or text == '3':
            money = 3
            return True
        elif text == 'restart' or text == '-1':
            self.go_back()
        else:
            return False

    def on_enter_input_money(self, event):
        text = '產生結果中\n請輸入:結果'
        send_text_message(event.reply_token, text)

    def is_going_to_give_advise(self, event):
        text = event.message.text
        return text == "結果"

    def on_enter_give_advise(self, event):
        text = search_gift_list(age, gender, festival, money)
        send_text_message(event.reply_token, text)
        self.go_back(event)

    def is_going_to_random_pick(self, event):
        text = event.message.text
        return text.lower() == "隨機挑選"

    def on_enter_random_pick(self, event):
        text = random_pick()
        send_text_message(event.reply_token, text)
        self.go_back(event)

    def is_going_to_search_merchandise(self, event):
        text = event.message.text
        return text == "查詢"

    def on_enter_search_merchandise(self, event):
        text = '請輸入商品名稱'
        send_text_message(event.reply_token, text)

    def is_going_to_show_merchandise(self, event):
        product_name = event.message.text
        text = search_product(product_name)
        send_text_message(event.reply_token, text)
        self.go_back(event)
