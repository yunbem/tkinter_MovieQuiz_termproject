from tkinter import *
from tkinter import font
from PIL import ImageTk, Image
from MovieQuery import *
from ChatGPT import *
import matplotlib.pyplot as plt

class MovieQuiz:
    def show_screen(self, screen_num): # 화면 전환을 처리하는 함수
        screens = [self.screen0_frame, self.screen1_frame, self.screen2_frame, self.screen3_frame, self.screen0_exp_frame]
        screen = screens[screen_num]
        screen.pack()
    
        if screen_num == 0:
            self.setScreen0_frame()
        elif screen_num == 1:
            self.setScreen1_frame()
        elif screen_num == 2:
            self.setScreen2_frame()
        elif screen_num == 3:
            self.setScreen3_frame()
        elif screen_num == 4:
            self.setScreen0_exp_frame()
    
        for i, other_screen in enumerate(screens):
            if i != screen_num:
                other_screen.pack_forget()

    def check_answer(self, choice):
        if self.rand_movies[choice] == self.movie_query:
            print('정답입니다!!!')
            if self.hint_use_check == False:
                self.answer_count += 1
            self.screen0_exp_frame.configure(bg='cyan')
        else:
            print('틀렸습니다ㅠ')
            if self.hint_use_check == False:
                self.wrong_count += 1
            self.screen0_exp_frame.configure(bg='indian red')
        self.prob_count += 1
        self.show_screen(4);

    def check_info(self, choice):
        movie = self.rand_movies[choice]
    
        title = self.movie.getMovieTitle(movie)
        release_date = self.movie.getMovieRelease(movie)
        vote_average = self.movie.getMovieVote(movie)
        overview = self.movie.getMovieOverview(movie)

        info = f"영화 제목: {title}\n개봉 일자: {release_date}\n평점: {vote_average}\n개요: {overview}"

        # info를 화면에 출력하는 코드 추가
        self.prob_text_boxs[choice].insert(END, info)

    def check_bookmarks(self, choice):
        movie = self.rand_movies[choice]
        self.movie.addBookmark(movie)
        print("즐겨찾기에 등록되었습니다!")

        if movie['poster_path']:
            poster_path = movie['poster_path']
            poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"

            response = requests.get(poster_url)

            if response.status_code == 200:
                with open(f'bookmark_poster{len(self.movie.getBookmarks())}.jpg', 'wb') as f:
                    f.write(response.content)
                print(f"즐겨찾기 포스터 {len(self.movie.getBookmarks())} 이미지 다운로드 완료")
            else:
                print(f"즐겨찾기 포스터 {len(self.movie.getBookmarks())} 이미지 다운로드 실패")
        
    def setupDefaultImageButton(self):  # 이미지 버튼 생성 및 배치
        button_coordinates = [(20, 20), (20, 220), (20, 420), (20, 620)] # 좌측 프레임 내 버튼 4개
        for i, (x, y) in enumerate(button_coordinates):
            image_button = Button(self.left_frame, width=80, height=80, command=lambda num=i: self.show_screen(num))
            image_button.place(x=x, y=y)
            self.image_buttons.append(image_button)

    def setupDefaultLabel(self):
        # left_frame
        label_texts = ["New 퀴즈", "즐겨찾기", "최근정답율", "상영 영화관"]
        label_coordinates = [(10, 120), (10, 320), (10, 520), (10, 720)]
        for text, (x, y) in zip(label_texts, label_coordinates):
            label = Label(self.left_frame, text=text, width=10, height=1, font=self.fontstyle1)
            label.place(x=x, y=y)

        # screen0_exp_frame
        self.Prob_label = Label(self.screen0_exp_frame, 
                          text="", bg='white', font=self.fontstyle1)
        self.Prob_label.place(x=10, y=10)

        # screen2_frame
        self.chart_image_label = Label(self.screen2_frame)
        self.chart_image_label.pack()

    def setupPosterButton(self):
        # 퀴즈 화면 포스터 버튼 생성 및 배치
        button_coordinates = [(50, 340), (270, 340), (50, 560), (270, 560)] # 퀴즈 화면 프레임 내 포스트 버튼 4개
        for i, (x, y) in enumerate(button_coordinates):
            poster_button = Button(self.screen0_frame, width=150, height=200, command=lambda choice=i: self.check_answer(choice))
            poster_button.place(x=x, y=y)
            self.poster_buttons.append(poster_button)

        # 해설 화면 포스터 버튼 생성 및 배치
        button_coordinates = [(50, 90), (270, 90), (50, 460), (270, 460)] # 해설 화면 프레임 내 포스트 버튼 4개
        for i, (x, y) in enumerate(button_coordinates):
            poster_button = Button(self.screen0_exp_frame, width=150, height=200, command=lambda choice=i: self.check_info(choice))
            poster_button.place(x=x, y=y)
            self.poster_buttons2.append(poster_button)

    def setupBookmarksButton(self):
        # 해설 화면 즐겨찾기 버튼 생성 및 배치, 이미지 적용
        image = Image.open("별.png")
        image = image.resize((40, 40))
        photo = ImageTk.PhotoImage(image)
        
        button_coordinates = [(20, 90), (240, 90), (20, 460), (240, 460)] # 해설 화면 프레임 내 포스트 버튼 4개
        for i, (x, y) in enumerate(button_coordinates):
            bookmark_button = Button(self.screen0_exp_frame, width=40, height=40, command=lambda choice=i: self.check_bookmarks(choice))
            bookmark_button.place(x=x, y=y)
            self.bookmarks_buttons.append(bookmark_button)
            self.bookmarks_buttons[i].config(image=photo)
            self.bookmarks_buttons[i].image = photo

    def setupTextBox(self):
        # screen0_exp_frame(해설 화면)에 텍스트 정보를 담는 박스 4개 생성
        text_box_coordinates = [(25, 300), (245, 300), (25, 670), (245, 670)] # 퀴즈 화면 프레임 내 포스트 버튼 4개
        for (x, y) in (text_box_coordinates):
            prob_text_box = Text(self.screen0_exp_frame, width=25, height=9)
            prob_text_box.place(x=x, y=y)
            self.prob_text_boxs.append(prob_text_box)
    
    def setImageButton(self):   # 이미지 로드 및 버튼에 이미지 적용
        image_filenames = ["물음표.png", "별.png", "그래프.png", "영화관.png"]
        for i, filename in enumerate(image_filenames):
            image = Image.open(filename)
            image = image.resize((80, 80))
            photo = ImageTk.PhotoImage(image)
            self.image_buttons[i].config(image=photo)
            self.image_buttons[i].image = photo

    def setPosterButton(self):  # 포스터 이미지 로드 및 버튼에 포스터 이미지 적용
        image_filenames = ["poster0.jpg", "poster1.jpg", "poster2.jpg", "poster3.jpg"]
        for i, filename in enumerate(image_filenames):
            image = Image.open(filename)
            image = image.resize((150, 200))
            photo = ImageTk.PhotoImage(image)
            self.poster_buttons[i].config(image=photo)
            self.poster_buttons[i].image = photo
            self.poster_buttons2[i].config(image=photo)
            self.poster_buttons2[i].image = photo

    def random_movies_PosterDownload(self):
        self.rand_movies = random.sample(self.prob_movies, len(self.prob_movies))
        for i, prob_movie in enumerate(self.rand_movies):
            poster_path = prob_movie['poster_path']
            poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        
            response = requests.get(poster_url)

            if response.status_code == 200:
                with open(f'poster{i}.jpg', 'wb') as f:
                    f.write(response.content)
                print(f"포스터 {i} 이미지 다운로드 완료")
            else:
                print(f"포스터 {i} 이미지 다운로드 실패")

    def setGptInstance(self):   # gpt 연동하기
        self.gpt = ChatGPT(self.movie_title)
        self.set_MovieStr(self.gpt.getPrompt()) # 텍스트 박스에 gpt 대답 기입하기
        if self.hint_use_check == False:
            self.hint_count += 1
            self.hint_use_check = True

    def setGptButton(self):     # GPT 버튼, 라벨 생성 및 배치
        Gpt_label = Label(self.screen0_frame, text="(버튼을 눌러서 GPT 해설을 볼 수 있어요)", 
                          bg='white', font=self.fontstyle2)
        Gpt_label.place(x=80, y=240)
        Gpt_label2 = Label(self.screen0_frame, text="(다만 조금 시간이 걸릴 수 있어요)", 
                          bg='white', font=self.fontstyle2)
        Gpt_label2.place(x=80, y=260)
        
        # 토큰 사용량에 따라 비용을 내야하기 때문에 주의. 
        # 처음 api를 사용할 때 3개월동안 18달러까지는 무료로 사용할 수 있다. 
        Gpt_button = Button(self.screen0_frame, width=40, height=40 , command=self.setGptInstance)
        #Gpt_button = Button(self.screen0_frame, width=40, height=40)
        Gpt_button.place(x=20, y=240)
        image = Image.open("ChatGPT.png")
        image = image.resize((40, 40))
        photo = ImageTk.PhotoImage(image)
        Gpt_button.config(image=photo)
        Gpt_button.image = photo

    def set_MovieStr(self, str): # 텍스트 박스에 검색 결과 기입
        self.text_box.insert(END, f"{str}\n\n")

    def create_chart(self):
        # 데이터
        labels = ['Correct', 'Incorrect', 'Hint']
        sizes = [self.answer_count, self.wrong_count, self.hint_count]
        colors = ['#66BB6A', '#EF5350', '#8fd9b6']
        explode = [0, 0.10, 0]

        # 차트 생성
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, colors=colors, autopct='%.1f%%', startangle=0, 
               explode=explode, shadow=True, labeldistance= 0.8)
        ax.legend(labels)
        ax.axis('equal')  # 원형 모양 유지

        # 차트를 이미지로 저장
        fig.savefig('chart_image.png')

        # 이미지를 Tkinter 캔버스에 삽입
        self.chart_image = ImageTk.PhotoImage(Image.open('chart_image.png'))
        self.chart_image_label.config(image=self.chart_image)
        self.chart_image_label.image = self.chart_image

    def setScreen0_frame(self): # new퀴즈 화면 GUI 구현
        # 문제 영화 정보 받기
        #self.movie_query = self.movie.getRandomQuery()
        #self.movie.getMovieInfo(self.movie_query)
        self.movie.getMovieInfo(self.movie.getRandomQuery())
        self.movie_query = self.movie.getMovieQuery()           # 진짜 거지같은 코드다
        self.movie_title = self.movie.getMovieTitle(self.movie_query)       # 문제 영화 제목
        self.movie_overview = self.movie.getMovieOverview(self.movie_query) # 문제 영화 줄거리

        self.prob_movies = []
        self.prob_movies.append(self.movie_query)  # 보기에 문제 영화 넣기

        # screen0_frame에 텍스트 정보를 담는 박스 생성
        self.text_box = Text(self.screen0_frame, width=60, height=15)
        self.text_box.place(x=20, y=20)         # 텍스트 박스 상단에 배치
        self.text_box.delete('1.0', END)        # 텍스트 박스 기존 내용 삭제
        self.set_MovieStr(self.movie_overview)  # 텍스트 박스에 문제 영화의 줄거리 기입

        # 유사한 영화들 정보 받기
        self.similar_movies = self.movie.getSimilarGenreMovies(self.movie_query)
        if self.similar_movies:
            for movie in self.similar_movies[:3]:
                self.prob_movies.append(movie)
     
        # gpt 버튼 생성 및 배치
        self.hint_use_check = False
        self.setGptButton()

        # 유사한 영화 포스터들 다운받기 
        self.random_movies_PosterDownload()

        # 포스터 이미지 초기화
        self.setPosterButton()

    def setScreen0_exp_frame(self): # 퀴즈해설 화면 GUI 구현
        self.Prob_label.configure(text="정답은... '"+str(self.movie_title)+ "' 입니다!")

        for text_box in self.prob_text_boxs:
            text_box.delete(1.0, END)  # 기존 텍스트 삭제

    def setScreen1_frame(self):     # 즐겨찾기 화면 GUI 구현

        # screen1_frame(즐겨찾기 화면)에 텍스트 박스 생성
        self.bookmark_text_boxs = []

        for i in range(1, len(self.movie.getBookmarks()) + 1):
            bookmark_text_box = Text(self.screen1_frame, width=36, height=20)
            bookmark_text_box.place(x=200, y=20+(i-1)*220)
            self.bookmark_text_boxs.append(bookmark_text_box)
            image = Image.open(f'bookmark_poster{i}.jpg')
            image = image.resize((150, 200))
            photo = ImageTk.PhotoImage(image)
            bookmark_poster = Label(self.screen1_frame, image=photo)
            bookmark_poster.place(x=20, y=20+(i-1)*220)
            bookmark_poster.image = photo

        for i, movie in enumerate(self.movie.getBookmarks()):
            title = self.movie.getMovieTitle(movie)
            release_date = self.movie.getMovieRelease(movie)
            vote_average = self.movie.getMovieVote(movie)
            overview = self.movie.getMovieOverview(movie)

            info = f"영화 제목: {title}\n개봉 일자: {release_date}\n평점: {vote_average}\n개요: {overview}"

            # info를 화면에 출력하는 코드 추가
            self.bookmark_text_boxs[i].insert(END, info)

    def setScreen2_frame(self):     # 최근 정답율 화면 GUI 구현
        # 파이 차트 생성 및 표시
        if not self.answer_count == self.wrong_count == self.hint_count == 0:
            self.create_chart()
        else:
            image = Image.open("null.png")
            image = image.resize((400, 400))
            photo = ImageTk.PhotoImage(image)
            self.chart_image_label.config(image=photo)
            self.chart_image_label.image = photo

    def setScreen3_frame(self):     # 상영 영화관 화면 GUI 구현
        pass

    def __init__(self):
        # tkinter 윈도우 생성
        self.window = Tk()
        self.window.title("영화퀴즈_프로그램")
        self.window.geometry("640x800")
        self.window.configure(bg='white')
        self.fontstyle1 = font.Font(self.window, size=14, weight='bold', family='Consolas')
        self.fontstyle2 = font.Font(self.window, size=10, weight='bold', family='Consolas')

        self.left_frame = Frame(self.window, width=130, height=800) # 좌측 프레임 생성
        self.left_frame.pack(side="left")

        self.screen0_frame = Frame(self.window, width=510, height=800, bg="white")  # new퀴즈 화면
        self.screen1_frame = Frame(self.window, width=510, height=800, bg="white")  # 즐겨찾기 화면
        self.screen2_frame = Frame(self.window, width=510, height=800, bg="white")  # 최근 정답율 화면
        self.screen3_frame = Frame(self.window, width=510, height=800, bg="white")  # 상영 영화관 화면
        self.screen0_exp_frame = Frame(self.window, width=510, height=800, bg="cyan") # 해설 화면

        self.image_buttons = []
        self.poster_buttons = []
        self.poster_buttons2 = []
        self.bookmarks_buttons = []
        self.prob_text_boxs = []
        self.bookmark_text_boxs = []
        self.prob_movies = []
        self.answer_count = 0
        self.wrong_count = 0
        self.hint_count = 0
        self.hint_use_check = False
        self.prob_count = 0

        self.setupDefaultImageButton()
        self.setImageButton()
        self.setupDefaultLabel()
        self.setupPosterButton()
        self.setupBookmarksButton()
        self.setupTextBox()
        
        # 초기 화면 설정
        self.movie = MovieQuery()
        self.show_screen(0)

        self.window.mainloop()

MovieQuiz()