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

key = '7dd451947ac9f89cc2c61f8dce323beb'
TOKEN = '6071626513:AAFf_TqmbyMwO9NwWqAzRNuh7l3c5krhWC4'
MAX_MSG_LENGTH = 300
baseurl = 'https://api.themoviedb.org/3/discover/movie'+key
bot = telepot.Bot(TOKEN)

def getData(loc_param, date_param):
    res_list = []
    url = baseurl+'&LAWD_CD='+loc_param+'&DEAL_YMD='+date_param
    print(url)
    res_body = urlopen(url).read()
    print(res_body)
    soup = BeautifulSoup(res_body, 'html.parser')
    items = soup.findAll('item')
    for item in items:
        item = re.sub('<.*?>', '|', item.text)
        parsed = item.split('|')
        try:
            row = parsed[3]+'/'+parsed[6]+'/'+parsed[7]+', '+parsed[4]+' '+parsed[5]+', '+parsed[8]+'m², '+parsed[11]+'F, '+parsed[1].strip()+'만원\n'
        except IndexError:
            row = item.replace('|', ',')

        if row:
            res_list.append(row.strip())
    return res_list

def getMovieDetails(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={key}'
    response = requests.get(url)
    data = response.json()
    return data

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def extractMovieId(row):
    match = re.search(r'Movie ID: (\d+)', row)
    if match:
        movie_id = match.group(1)
        return movie_id
    return None


def run(date_param, param='11710'):
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
    conn.commit()

    user_cursor = sqlite3.connect('users.db').cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    user_cursor.execute('SELECT * from users')

    for data in user_cursor.fetchall():
        user, param = data[0], data[1]
        print(user, date_param, param)
        res_list = getData( param, date_param )
        msg = ''
        for r in res_list:
            try:
                cursor.execute('INSERT INTO logs (user,log) VALUES ("%s", "%s")'%(user,r))
            except sqlite3.IntegrityError:
                # 이미 해당 데이터가 있다는 것을 의미합니다.
                pass
            else:
                print( str(datetime.now()).split('.')[0], r )
                
                # 영화 ID 추출
                movie_id = extractMovieId(r)

                if movie_id:
                    # 영화 세부정보 가져오기
                    movie_details = getMovieDetails(movie_id)

                    # 세부정보 활용하여 메시지 작성
                    movie_title = movie_details['title']
                    movie_overview = movie_details['overview']
                    movie_release_date = movie_details['release_date']
                    movie_msg = f"Title: {movie_title}\nOverview: {movie_overview}\nRelease Date: {movie_release_date}\n"

                    if len(movie_msg + msg) + 1 > MAX_MSG_LENGTH:
                        sendMessage(user, msg)
                        msg = movie_msg + '\n'
                    else:
                        msg += movie_msg + '\n'
        if msg:
            sendMessage( user, msg )
    conn.commit()

if __name__=='__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print( '[',today,']received token :', TOKEN )

    pprint( bot.getMe() )

    run(current_month)
