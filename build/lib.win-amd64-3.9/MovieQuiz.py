import sys
import threading
import matplotlib.pyplot as plt
import spam
from tkinter import *
from tkinter import font
import tkinter.ttk as ttk
from PIL import ImageTk, Image
from cefpython3 import cefpython as cef
from MovieQuery import *
from ChatGPT import ChatGPT
from Map import Map
from teller import *

class MovieQuiz:
    def setup(self):
        # 브라우저를 위한 쓰레드 생성
        thread = threading.Thread(target=self.showMap, args=(self.screen3_frame,))
        thread.daemon = True
        thread.start()

    # cef모듈로 브라우저 실행
    def showMap(self, frame):
        global browser
        sys.excepthook = cef.ExceptHook
        window_info = cef.WindowInfo(frame.winfo_id())
        window_info.SetAsChild(frame.winfo_id(), [0, 0, 510, 800])
        cef.Initialize()
        browser = cef.CreateBrowserSync(window_info, url='file:///map.html')
        cef.MessageLoop()

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

        self.answer_label = Label(self.screen2_frame, text="맞춘 정답의 수: "+str(self.answer_count), 
                          bg='white', font=self.fontstyle1)
        self.answer_label.pack()

        self.wrong_label = Label(self.screen2_frame, text="틀린 오답의 수: "+str(self.wrong_count), 
                          bg='white', font=self.fontstyle1)
        self.wrong_label.pack()

        self.hint_label = Label(self.screen2_frame, text="힌트를 쓴 답의 수: "+str(self.hint_count), 
                          bg='white', font=self.fontstyle1)
        self.hint_label.pack()

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
        
        button_coordinates = [(20, 240), (240, 240), (20, 610), (240, 610)] # 해설 화면 프레임 내 포스트 버튼 4개
        for i, (x, y) in enumerate(button_coordinates):
            bookmark_button = Button(self.screen0_exp_frame, width=40, height=40, command=lambda choice=i: self.check_bookmarks(choice))
            bookmark_button.place(x=x, y=y)
            self.bookmarks_buttons.append(bookmark_button)
            self.bookmarks_buttons[i].config(image=photo)
            self.bookmarks_buttons[i].image = photo

    def get_movie_info(self): # 텔레그램 기능
        movie_title = self.entry.get().strip()
        # 만약 entry에 기입한 영화가 없다면 콤보박스 탐색
        if movie_title == '':
            movie_title = self.Bookmark_combobox.get()

        if not movie_title:
            print('영화명을 입력해주세요.')
            return

        movie_details = self.bot.get_movie_details(movie_title)
        if movie_details:
            movie_title = movie_details['title']
            movie_overview = movie_details['overview']
            movie_release_date = movie_details['release_date']
            movie_poster_path = movie_details['poster_path']

            movie_msg = f"Title: {movie_title}\nOverview: {movie_overview}\nRelease Date: {movie_release_date}\n"
            pprint(movie_msg)  # 세부 정보 출력 (테스트용)

            # 텔레그램 봇을 통해 세부 정보 전송
            # 포스터 이미지 전송
            if movie_poster_path:
                poster_url = self.bot.get_movie_poster_url(movie_poster_path)
                self.bot.send_photo(API_Key.telegram_my_id, poster_url)
                self.bot.send_message(API_Key.telegram_my_id, movie_msg)
                print('성공!', poster_url)
            else:
                self.bot.send_message(API_Key.telegram_my_id, movie_msg)
        else:
            print('해당 영화 정보를 찾을 수 없습니다.')

    def setupSubButton(self):
        def test():
            movie_list = self.movie.getBookmarksMovieTitle()
            print(movie_list)
            spam.save_movie_list(movie_list, "movie_list.txt") 

        self.entry = Entry(self.screen1_frame)
        self.entry.pack(side=TOP,anchor="e")

        # 즐겨찾기에 등록된 영화 검색을 위한 콤보박스 생성
        BookmarkMovies = self.movie.getBookmarksMovieTitle()
        self.Bookmark_combobox = ttk.Combobox(self.screen1_frame, values=BookmarkMovies, width=20)
        self.Bookmark_combobox.pack(side=TOP,anchor="e")

        image = Image.open("telegram.png")
        image = image.resize((40, 40))
        photo = ImageTk.PhotoImage(image)

        button = Button(self.screen1_frame, width=40, height=40, command=self.get_movie_info)
        button.pack(side=TOP, anchor="e")
        self.sub_buttons.append(button)
        self.sub_buttons[0].config(image=photo)
        self.sub_buttons[0].image = photo

        image = Image.open("note.png")
        image = image.resize((40, 40))
        photo = ImageTk.PhotoImage(image)

        button = Button(self.screen1_frame, width=40, height=40, command=test)
        button.pack(side= RIGHT, anchor="n")
        self.sub_buttons.append(button)
        self.sub_buttons[1].config(image=photo)
        self.sub_buttons[1].image = photo

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
        self.rand_movies = random.sample(self.prob_movies, len(self.prob_movies)) # 보기 영화 4개를 랜덤으로 섞음
        
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

            if prob_movie == self.movie_query:
                self.answer_position = i
                print(self.answer_position,' 가 현재 정답 위치입니다.')

    def setGptInstance(self):   # gpt 연동하기
        self.gpt = ChatGPT(self.movie_overview)
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
        
        # 2023.05.25
        # 토큰 사용량에 따라 비용을 내야하기 때문에 주의. 
        # 처음 api를 사용할 때 3개월동안 18달러까지는 무료로 사용할 수 있다. 
        
        # 2023.06.06 
        # gpt 오류 때문에 그냥 유료판 구매했다
        Gpt_button = Button(self.screen0_frame, width=40, height=40 , command=self.setGptInstance)
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

        self.movie.getMovieInfo(self.movie.getRandomQuery())
        self.movie_query = self.movie.getMovieQuery()         
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
        # 해설 화면 체크 라벨 생성 및 배치
        label_coordinates = [(20, 90), (240, 90), (20, 460), (240, 460)]
        for i, (x, y) in enumerate(label_coordinates):
            if self.answer_position == i:
                image = Image.open("o.png")
                image = image.resize((40, 40))
                photo = ImageTk.PhotoImage(image)
                # print('i는 ', i)
            else:
                image = Image.open("x.png")
                image = image.resize((40, 40))
                photo = ImageTk.PhotoImage(image)

            ox_label = Label(self.screen0_exp_frame, image=photo)
            ox_label.place(x=x, y=y)
            ox_label.config(image=photo)
            ox_label.image = photo

        # 정답 영화 제목 출력
        self.Prob_label.configure(text="정답은... '"+(self.movie_title)+ "' 입니다!")

        for text_box in self.prob_text_boxs:
            text_box.delete(1.0, END)  # 기존 텍스트 삭제

    def setScreen1_frame(self):
        self.bookmark_textboxes = []

        for i, movie in enumerate(self.movie.getBookmarks()):
            image = Image.open(f'bookmark_poster{i+1}.jpg')
            image = image.resize((150, 200))
            photo = ImageTk.PhotoImage(image)

            bookmark_poster = Label(self.frame, image=photo)
            bookmark_poster.grid(row=i, column=0, padx=10, pady=10)
            bookmark_poster.image = photo
            self.bookmark_posters.append(bookmark_poster)

            bookmark_textbox = Text(self.frame, width=36, height=20)
            bookmark_textbox.grid(row=i, column=1, padx=10, pady=10)
            self.bookmark_textboxes.append(bookmark_textbox)

            title = self.movie.getMovieTitle(movie)
            release_date = self.movie.getMovieRelease(movie)
            vote_average = self.movie.getMovieVote(movie)
            overview = self.movie.getMovieOverview(movie)

            info = f"영화 제목: {title}\n개봉 일자: {release_date}\n평점: {vote_average}\n개요: {overview}"

            # info를 화면에 출력하는 코드 추가
            self.bookmark_textboxes[i].insert(END, info)

        self.entry.delete(0, 'end')

        BookmarkMovies = self.movie.getBookmarksMovieTitle()
        BookmarkMovies.append("")  # 빈 정보를 추가
        self.Bookmark_combobox.configure(values=BookmarkMovies)


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

        self.answer_label.configure(text="맞춘 정답의 수: "+str(self.answer_count))

        self.wrong_label.configure(text="틀린 오답의 수: "+str(self.wrong_count))

        self.hint_label.configure(text="힌트를 쓴 답의 수: "+str(self.hint_count))

    def setScreen3_frame(self):  # 상영 영화관 화면 GUI 구현
        def parse_theater_info():
            selected_city = city_combobox.get()

            # 시군구 정보를 기반으로 영화관 정보를 가져옴
            self.map.get_theater_info(selected_city)

            # 브라우저 리로드
            browser.Reload()

        # 시군구 정보 입력을 위한 콤보박스 생성
        cities = self.map.get_city_list()
        city_combobox = ttk.Combobox(self.screen3_frame, values=cities, width=20)
        city_combobox.place(x=20, y=720)

        # 파싱 버튼 생성
        parse_button = Button(self.screen3_frame, text="파싱", command=parse_theater_info)
        parse_button.place(x=20, y=750)

    def __init__(self):
        # tkinter 윈도우 생성
        window = Tk()
        window.title("영화퀴즈_프로그램")
        window.geometry("680x800")
        window.configure(bg='white')
        self.fontstyle1 = font.Font(window, size=14, weight='bold', family='Consolas')
        self.fontstyle2 = font.Font(window, size=10, weight='bold', family='Consolas')

        self.left_frame = Frame(window, width=130, height=800) # 좌측 프레임 생성
        self.left_frame.pack(side="left")

        self.screen0_frame = Frame(window, width=510, height=800, bg="white")  # new퀴즈 화면
        self.screen1_frame = Frame(window, width=510, height=800, bg="white")  # 즐겨찾기 화면
        self.screen2_frame = Frame(window, width=510, height=800, bg="white")  # 최근 정답율 화면
        self.screen3_frame = Frame(window, width=510, height=800, bg="white")  # 상영 영화관 화면
        self.screen0_exp_frame = Frame(window, width=510, height=800, bg="cyan") # 해설 화면

        self.movie = MovieQuery()

        self.image_buttons = []
        self.poster_buttons = []
        self.poster_buttons2 = []
        self.OX_labels = []
        self.bookmarks_buttons = []
        self.sub_buttons = [] # 0번 원소는 telegram 기능, 1번 원소는 메모장 저장 기능
        self.prob_text_boxs = []
        self.prob_movies = []
        self.answer_count = 0
        self.wrong_count = 0
        self.hint_count = 0
        self.hint_use_check = False
        self.answer_position = 0 # 0,1,2,3

        self.setupDefaultImageButton()
        self.setImageButton()
        self.setupDefaultLabel()
        self.setupPosterButton()
        self.setupBookmarksButton()
        self.setupSubButton() # 즐겨찾기 화면에 들어가는 부가 버튼들 배치
        self.setupTextBox()

        self.bookmark_textboxes = []
        self.bookmark_posters = []
        self.canvas = None
        self.frame = None
  
        # 초기 화면 설정
        
        self.show_screen(0)

        # screen1_frame(즐겨찾기 화면)에 리스트 박스 생성
        self.canvas = Canvas(self.screen1_frame, width=460, height=700, bg="white")
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(self.screen1_frame, orient=VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.frame = Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.frame, anchor=NW)

        self.frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # 영화관 지도 기능
        self.map = Map()
        self.setup()

        # 텔레그램 챗봇
        self.bot = Tele()

        window.mainloop()

MovieQuiz()