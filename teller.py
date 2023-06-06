
import tkinter as tk
import requests
from tkinter import messagebox
from pprint import pprint
import API_Key

class TelegramBot:
    def __init__(self):
        self.token = API_Key.tellegram_key
        self.base_url = f'https://api.telegram.org/bot{self.token}/'
        self.key = API_Key.Tmdb_api_key

    def get_movie_details(self, movie_title, language='ko-KR'):
        url = f'https://api.themoviedb.org/3/search/movie?api_key={self.key}&query=\
        {movie_title}&language={language}'
        response = requests.get(url)
        data = response.json()
        results = data['results']
        if results:
            movie_details = results[0]  # Get the first movie in the search results
            return movie_details
        else:
            return None

    def send_message(self, chat_id, message):
        url = f'{self.base_url}sendMessage'
        params = {
            'chat_id': chat_id,
            'text': message
        }
        response = requests.post(url, params=params)
        return response.json()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('영화 정보 조회')
        self.geometry('400x200')
        self.resizable(False, False)

        self.bot = TelegramBot()

        self.label = tk.Label(self, text='영화명:')
        self.label.pack()

        self.entry = tk.Entry(self)
        self.entry.pack()

        self.button = tk.Button(self, text='영화 정보 조회', command=self.get_movie_info)
        self.button.pack()

    def get_movie_info(self):
        movie_title = self.entry.get().strip()
        if not movie_title:
            messagebox.showerror('오류', '영화명을 입력해주세요.')
            return

        movie_details = self.bot.get_movie_details(movie_title)
        if movie_details:
            movie_title = movie_details['title']
            movie_overview = movie_details['overview']
            movie_release_date = movie_details['release_date']
            movie_msg = f"Title: {movie_title}\nOverview: {movie_overview}\nRelease Date: {movie_release_date}\n"
            pprint(movie_msg)  # 세부 정보 출력 (테스트용)
            # 텔레그램 봇을 통해 세부 정보 전송
            self.bot.send_message(API_Key.tellegram_my_id, movie_msg)
        else:
            messagebox.showinfo('알림', '해당 영화 정보를 찾을 수 없습니다.')

if __name__ == '__main__':
    app = App()
    app.mainloop()

