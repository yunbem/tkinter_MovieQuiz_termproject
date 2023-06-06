#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
import requests
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback

import noti


def replyAptData(date_param, user, loc_param='11710'):
    print(user, date_param, loc_param)
    res_list = noti.getData( loc_param, date_param )
    msg = ''
    for r in res_list:
        print( str(datetime.now()).split('.')[0], r )
        if len(r+msg)+1>noti.MAX_MSG_LENGTH:
            noti.sendMessage( user, msg )
            msg = r+'\n'
        else:
            msg += r+'\n'
    if msg:
        noti.sendMessage( user, msg )
    else:
        noti.sendMessage( user, '%s 기간에 해당하는 데이터가 없습니다.'%date_param )

def save( user, loc_param ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    try:
        cursor.execute('INSERT INTO users(user, location) VALUES ("%s", "%s")' % (user, loc_param))
    except sqlite3.IntegrityError:
        noti.sendMessage( user, '이미 해당 정보가 저장되어 있습니다.' )
        return
    else:
        noti.sendMessage( user, '저장되었습니다.' )
        conn.commit()

def check( user ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    cursor.execute('SELECT * from users WHERE user="%s"' % user)
    for data in cursor.fetchall():
        row = 'id:' + str(data[0]) + ', location:' + data[1]
        noti.sendMessage( user, row )

def getMovieDetails(movie_title):
    url = f'https://api.themoviedb.org/3/search/movie?api_key={noti.key}&query={movie_title}'
    response = requests.get(url)
    data = response.json()
    results = data['results']
    if results:
        movie_details = results[0]  # Get the first movie in the search results
        return movie_details
    else:
        return None

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('거래') and len(args)>1:
        print('try to 거래', args[1])
        replyAptData( args[1], chat_id, args[2] )
    elif text.startswith('지역') and len(args)>1:
        print('try to 지역', args[1])
        replyAptData( '201705', chat_id, args[1] )
    elif text.startswith('저장')  and len(args)>1:
        print('try to 저장', args[1])
        save( chat_id, args[1] )
    elif text.startswith('확인'):
        print('try to 확인')
        check( chat_id )
    elif text.startswith('영화') and len(args) > 1:
        print('try to 영화', args[1])
        movie_title = ' '.join(args[1:])
        movie_details = getMovieDetails(movie_title)
        if movie_details:
            movie_title = movie_details['title']
            movie_overview = movie_details['overview']
            movie_release_date = movie_details['release_date']
            movie_msg = f"Title: {movie_title}\nOverview: {movie_overview}\nRelease Date: {movie_release_date}\n"
            noti.sendMessage(chat_id, movie_msg)
        else:
            noti.sendMessage(chat_id, f"'{movie_title}'에 대한 영화 정보를 찾을 수 없습니다.")
    else:
        noti.sendMessage(chat_id, "모르는 명령어입니다.\n")

today = date.today()
current_month = today.strftime('%Y%m')

print( '[',today,']received token :', noti.TOKEN )

bot = telepot.Bot(noti.TOKEN)
pprint( bot.getMe() )

bot.message_loop(handle)

print('Listening...')

while 1:
  time.sleep(10)

# 영화 세부 정보, 포스터를 출력하도록 인자로 영화 제목을 받는 것으로 수정