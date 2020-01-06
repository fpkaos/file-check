#!/usr/bin/env python3

import requests
import json
from sys import argv
import telebot
from telebot import types
from telebot.types import InputMediaPhoto
from bs4 import BeautifulSoup as bs

token = ''
channel = '@'
logfile = argv[1]
bot = telebot.TeleBot(token)

class Post():
    def __init__(self, post):
        '''
        text (str): message.text
        link (str): link to the original post -> btn
        pics (list): list of links for attached images
        '''
        self.post = post[0]
        self.header = post [1]
        self.text = None
        self.link = None
        self.pics = list()

    def parse_images(self, pic):
        js = pic.get('onclick')
        if 'showPhoto' in js:
            pic_url = js.split(',')[2].split(':')
            self.pics.append(InputMediaPhoto(json.loads(':'.join(pic_url[2:4]))))

    def parse_text(self):
        div_str = str(self.post.find(class_='wall_post_text')).replace('<br/>', '\r\n')
        parts = bs(div_str, 'html.parser').getText().split('Показать полностью…')
        self.text = ''.join(parts)

    def parse(self):
        self.parse_text()
        
        new_markup = self.post.find_all('a', class_='image_cover')
        old_markup = self.post.find_all('a', class_='page_post_thumb_unsized')
        markup = new_markup + old_markup
        if markup:
            for pic in markup:
                self.parse_images(pic)

        self.link = self.header.find_all('a', class_='post_link')[0]['href']
        return self
    
    def upload(self):
        try:
            if self.text and self.text != 'None':
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text='Пост VK', url=f'https://vk.com{self.link}'))
                if len(self.text) > 4096:
                    long_text = list()
                    for x in range(0, len(self.text), 4096):
                        long_text.append(self.text[x:x+4096])
                    for sm_text in long_text[:-1]:
                        bot.send_message(channel, sm_text)
                    self.text = long_text[-1]
                bot.send_message(channel, self.text, reply_markup=markup)
            if self.pics:    
                bot.send_media_group(channel, self.pics)
        except Exception as e:
            print(e)

def get_state():
    with open(logfile, 'r') as log:
        state = int(log.readlines()[-1]) - 20
        if state < 20: exit()
    return state

def save_sate(offset):
    with open(logfile, 'a') as log:
        log.write(str(offset) + '\n')

def get_posts(target_uri):
    raw_page = requests.get(target_uri, headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'})
    if raw_page.ok:
        page = bs(raw_page.text, 'html.parser')
        posts = page.find_all('div', class_='wall_text')
        headers = page.find_all('div', class_='post_header')
        return list(zip(posts, headers))[::-1]

def get_pages(lastet_offset, newest_offset=20):
    for offset in range(lastet_offset, newest_offset, -20): #8120-2100
        save_sate(offset)
        posts = get_posts(f'https://vk.com/wall-?offset={offset}&own=1')
        for post in posts:
            Post(post).parse().upload()

if __name__ == '__main__':
    try:
        get_pages(int(argv[2]), int(argv[3]))
    except IndexError:
        get_pages(get_state())
