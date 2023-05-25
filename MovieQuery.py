import requests
import random

class MovieQuery:
    def __init__(self):
        self.params = {
            "api_key": "API_KEY",
            "language": "ko",
            "page": "2",
            #"sort_by": "popularity.desc",  # 인기순으로 정렬
            "sort_by": "vote_average.desc",  # 평점순으로 정렬
            #"include_adult": "false"  # 성인 영화 제외
            "vote_count.gte": "200",  # 최소 투표 수 조건
        }

        self.data = []  # 영화 데이터를 저장할 리스트
        self.bookmarks = []  # 즐겨찾기 저장할 리스트
        self.fetchMovieData()  # 영화 데이터를 가져옴

    def fetchMovieData(self):
        page = 1
        for _ in range(5):
            self.params["page"] = str(page)
            url = 'https://api.themoviedb.org/3/discover/movie'  # 정보를 요청할 주소
            resp = requests.get(url, params=self.params)
            page_data = resp.json()["results"]

            if not page_data:
                break  # 페이지 데이터가 없으면 종료

            self.data.extend(page_data)  # 페이지 데이터를 전체 데이터에 추가
            page += 1

    def getRandomQuery(self):
        if self.data:
            query = random.choice(self.data)  # 영화 목록에서 랜덤하게 영화 선택
            return query
        else:
            print("data를 받아오지 못했습니다.")
            return None 

    def getMovieInfo(self, query): # 영화 정보를 받습니다.
        # 영화 정보 출력
        print("영화 제목:", query['title'])
        print("개봉 일자:", query['release_date'])
        print("평점:", query['vote_average'])

        if 'overview' in query and query['overview']:
            print("개요:", query['overview'])
            self.moviequery = query
        else:
            print("개요 정보가 없습니다. 다른 쿼리로 영화 정보를 조회합니다.")
            new_query = self.getRandomQuery()  # 다른 쿼리를 가져옴
            self.getMovieInfo(new_query)  # 다른 쿼리로 재귀적으로 호출

    def getMovieQuery(self):
        return self.moviequery

    def PosterDownload(self, query, num): # 영화 포스터 이미지를 받습니다
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
                print("포스터 이미지 다운로드 완료")
            else:
                print("포스터 이미지 다운로드 실패")

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
            print("영화의 장르 정보가 없습니다.")
            return None

    def addBookmark(self, query):
        self.bookmarks.append(query)

    def removeBookmark(self, query):
        if query in self.bookmarks:
            self.bookmarks.remove(query)

    def getBookmarks(self):
        return self.bookmarks
        