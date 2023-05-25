import requests
import random

class MovieQuery:
    def __init__(self):
        params = {
            "api_key": "7dd451947ac9f89cc2c61f8dce323beb",
            "language": "ko",
            "page": "1",
            #"sort_by": "popularity.desc",  # �α������ ����
            "sort_by": "vote_average.desc",  # ���������� ����
            #"include_adult": "false"  # ���� ��ȭ ����
            "vote_count.gte": "200",  # �ּ� ��ǥ �� ����
        }

        url = 'https://api.themoviedb.org/3/discover/movie'  # ������ ��û�� �ּ�
        resp = requests.get(url, params=params)
        self.data = resp.json()['results']

        self.bookmarks = []  # ���ã�� ������ ����Ʈ

    def getRandomQuery(self):
        if self.data:
            query = random.choice(self.data)  # ��ȭ ��Ͽ��� �����ϰ� ��ȭ ����
            return query
        else:
            print("data�� �޾ƿ��� ���߽��ϴ�.")
            return None 

    def getMovieInfo(self, query): # ��ȭ ������ �޽��ϴ�.
        # ��ȭ ���� ���
        print("��ȭ ����:", query['title'])
        print("���� ����:", query['release_date'])
        print("����:", query['vote_average'])

        if 'overview' in query and query['overview']:
            print("����:", query['overview'])
        else:
            print("���� ������ �����ϴ�. �ٸ� ������ ��ȭ ������ ��ȸ�մϴ�.")
            new_query = self.getRandomQuery()  # �ٸ� ������ ������
            self.getMovieInfo(new_query)  # �ٸ� ������ ��������� ȣ��

    def PosterDownload(self, query, num): # ��ȭ ������ �̹����� �޽��ϴ�
        if query['poster_path']:
            poster_path = query['poster_path']
            poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"

            response = requests.get(poster_url)

            if response.status_code == 200:
                if num == -1:
                    with open('answer_poster.jpg', 'wb') as f:
                        f.write(response.content)
                elif num == 0:
                    with open('poster0.jpg', 'wb') as f:
                        f.write(response.content)
                elif num == 1:
                    with open('poster1.jpg', 'wb') as f:
                        f.write(response.content)
                elif num == 2:
                    with open('poster2.jpg', 'wb') as f:
                        f.write(response.content)
                print("������ �̹��� �ٿ�ε� �Ϸ�")
            else:
                print("������ �̹��� �ٿ�ε� ����")

    def getMovieTitle(self, query):
        return query['title']

    def getMovieRelease(self, query):
        return query['release_date']

    def getMovieVote(self, query):
        return str(query['vote_average'])

    def getMovieOverview(self, query):
        return query['overview']

    def getSimilarGenreMovies(self, query):
        genre_id = query['genre_ids'][0] if 'genre_ids' in query else None

        if genre_id:
            similar_movies = []
            for movie in self.data:
                if 'genre_ids' in movie and genre_id in movie['genre_ids']:
                    similar_movies.append(movie)
            
            return similar_movies
        else:
            print("��ȭ�� �帣 ������ �����ϴ�.")
            return None

    def addBookmark(self, query):
        self.bookmarks.append(query)

    def removeBookmark(self, query):
        if query in self.bookmarks:
            self.bookmarks.remove(query)

    def getBookmarks(self):
        return self.bookmarks
        