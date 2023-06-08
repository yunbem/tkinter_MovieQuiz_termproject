import requests
from pprint import pprint
import API_Key

class Tele:
    def __init__(self):
        self.token = API_Key.telegram_key
        self.base_url = f'https://api.telegram.org/bot{self.token}/'
        self.key = API_Key.Tmdb_api_key
        self.poster_base_url = 'https://image.tmdb.org/t/p/'

    def get_movie_details(self, movie_title, language='ko-KR'):
        url = f'https://api.themoviedb.org/3/search/movie?api_key={self.key}&query=\
        {movie_title}&language={language}'

        response = requests.get(url)
        data = response.json()
        results = data['results']
        if results:
            movie_details = results[0]
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

    def send_photo(self, chat_id, photo_url):
        url = f'{self.base_url}sendPhoto'
        files = {'photo': requests.get(photo_url).content}
        params = {
            'chat_id': chat_id,
        }
        response = requests.post(url, params=params, files=files)
        return response.json()


    def get_movie_poster_url(self, poster_path, size='w500'):
        return f'{self.poster_base_url}{size}/{poster_path}'
