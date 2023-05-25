from tkinter import *
from tkinter import messagebox
from tkinter import font
from PIL import ImageTk, Image
from MovieQuery import *
from ChatGPT import *

class MovieQuiz:
    def show_screen(self, screen_num):  # 화면 전환을 처리하는 함수
        screens = [self.screen0_frame, self.screen1_frame, self.screen2_frame, self.screen3_frame, self.screen0_exp_frame]
        for i, screen in enumerate(screens):
            if i == screen_num:
                screen.pack()
                if i == 0:
                    self.setScreen0_frame()
                elif i == 4:
                    self.setScreen0_exp_frame()
            else:
                screen.pack_forget()

    def check_answer(self, choice):
        if choice == 0:
            print('정답입니다!!!')
            self.screen0_exp_frame.configure(bg='cyan')
        else:
            print('틀렸습니다ㅠ')
            self.screen0_exp_frame.configure(bg='indian red')
        self.show_screen(4);

    def check_info(self, choice):
        pass
        
    def setupDefaultImageButton(self):  # 이미지 버튼 생성 및 배치
        button_coordinates = [(20, 20), (20, 220), (20, 420), (20, 620)] # 좌측 프레임 내 버튼 4개
        for i, (x, y) in enumerate(button_coordinates):
            image_button = Button(self.left_frame, width=80, height=80, command=lambda num=i: self.show_screen(num))
            image_button.place(x=x, y=y)
            self.image_buttons.append(image_button)

    def setImageButton(self):   # 이미지 로드 및 버튼에 이미지 적용
        image_filenames = ["물음표.png", "별.png", "그래프.png", "영화관.png"]
        for i, filename in enumerate(image_filenames):
            image = Image.open(filename)
            image = image.resize((80, 80))
            photo = ImageTk.PhotoImage(image)
            self.image_buttons[i].config(image=photo)
            self.image_buttons[i].image = photo

    def setupDefaultLabel(self):
        label_texts = ["New 퀴즈", "즐겨찾기", "최근정답율", "상영 영화관"]
        label_coordinates = [(10, 120), (10, 320), (10, 520), (10, 720)]
        for text, (x, y) in zip(label_texts, label_coordinates):
            label = Label(self.left_frame, text=text, width=10, height=1, font=self.fontstyle1)
            label.place(x=x, y=y)

        self.Gpt_label = Label(self.screen0_exp_frame, 
                          text="", 
                          bg='white', font=self.fontstyle1)
        self.Gpt_label.place(x=10, y=10)

    def setupPosterButton_Quiz(self):  # 퀴즈 화면 포스터 버튼 생성 및 배치
        button_coordinates = [(40, 340), (240, 340), (40, 560), (240, 560)] # 퀴즈 화면 프레임 내 포스트 버튼 4개
        for i, (x, y) in enumerate(button_coordinates):
            poster_button = Button(self.screen0_frame, width=150, height=200, command=lambda choice=i: self.check_answer(choice))
            poster_button.place(x=x, y=y)
            self.poster_buttons.append(poster_button)

        button_coordinates = [(40, 90), (240, 90), (40, 460), (240, 460)] # 퀴즈 화면 프레임 내 포스트 버튼 4개
        for i, (x, y) in enumerate(button_coordinates):
            poster_button = Button(self.screen0_exp_frame, width=150, height=200, command=lambda choice=i: self.check_info(choice))
            poster_button.place(x=x, y=y)
            self.poster_buttons.append(poster_button)

    def setupPosterButton_Exp(self):  # 해설 화면 포스터 버튼 생성 및 배치
        button_coordinates = [(40, 90), (240, 90), (40, 460), (240, 460)] # 퀴즈 화면 프레임 내 포스트 버튼 4개
        for i, (x, y) in enumerate(button_coordinates):
            poster_button = Button(self.screen0_exp_frame, width=150, height=200, command=lambda choice=i: self.check_info(choice))
            poster_button.place(x=x, y=y)
            self.poster_buttons2.append(poster_button)

    def setPosterButton(self):  # 포스터 이미지 로드 및 버튼에 포스터 이미지 적용
        image_filenames = ["answer_poster.jpg", "poster0.jpg", "poster1.jpg", "poster2.jpg"]
        for i, filename in enumerate(image_filenames):
            image = Image.open(filename)
            image = image.resize((150, 200))
            photo = ImageTk.PhotoImage(image)
            self.poster_buttons[i].config(image=photo)
            self.poster_buttons[i].image = photo

    def set_MovieOverview(self, str): # 텍스트 박스에 검색 결과 기입
        self.text_box.insert(END, f"{str}\n\n")

    def setScreen0_frame(self):     # new퀴즈 화면 GUI 구현
        # 영화 정보 받기
        self.movie = MovieQuery()
        self.movie_query = self.movie.getRandomQuery()
        self.movie.PosterDownload(self.movie_query, -1) # -1은 정답은 영화 포스터
        self.movie.getMovieInfo(self.movie_query)
        self.answer_title = self.movie.getMovieTitle(self.movie_query)
        self.answer_overview = self.movie.getMovieOverview(self.movie_query)

        # screen0_frame에 텍스트 정보를 담는 박스와 스크롤바 생성
        self.text_box = Text(self.screen0_frame, width=60, height=15)

        # 텍스트 박스 상단에 배치
        self.text_box.place(x=20, y=20)
      
        self.text_box.delete('1.0', END)  # 기존 내용 삭제
        self.set_MovieOverview(self.answer_overview)
        self.similar_movies = self.movie.getSimilarGenreMovies(self.movie_query)
        if self.similar_movies:
            for i, movie in enumerate(self.similar_movies[:3]):
                self.movie.PosterDownload(movie, i)
     
        # 포스터 이미지 초기화
        self.setPosterButton()

        #self.setGptButton()

    def setScreen0_exp_frame(self): # 퀴즈해설 화면 GUI 구현
        self.Gpt_label.configure(text="정답은... '"+str(self.answer_title)+ "' 입니다!")
        # 포스터 이미지 초기화
        #self.setPosterButton()

    def setScreen1_frame(self):     # 즐겨찾기 화면 GUI 구현
        pass

    def setScreen2_frame(self):     # 최근 정답율 화면 GUI 구현
        pass

    def setScreen3_frame(self):     # 상영 영화관 화면 GUI 구현
        pass

    def __init__(self):
        # tkinter 윈도우 생성
        self.window = Tk()
        self.window.title("TEST_GUI")
        self.window.geometry("600x800")
        self.window.configure(bg='white')
        self.fontstyle1 = font.Font(self.window, size=14, weight='bold', family='Consolas')
        self.fontstyle2 = font.Font(self.window, size=10, weight='bold', family='Consolas')

        self.left_frame = Frame(self.window, width=130, height=800) # 좌측 프레임 생성
        self.left_frame.pack(side="left")

        self.screen0_frame = Frame(self.window, width=470, height=800, bg="white")  # new퀴즈 화면
        self.screen1_frame = Frame(self.window, width=470, height=800, bg="white")  # 즐겨찾기 화면
        self.screen2_frame = Frame(self.window, width=470, height=800, bg="white")  # 최근 정답율 화면
        self.screen3_frame = Frame(self.window, width=470, height=800, bg="white")  # 상영 영화관 화면
        self.screen0_exp_frame = Frame(self.window, width=470, height=800, bg="cyan") # 해설 화면

        self.image_buttons = []
        self.poster_buttons = []
        self.poster_buttons2 = []
        self.setupDefaultImageButton()
        self.setImageButton()
        self.setupDefaultLabel()
        self.setupPosterButton_Quiz()
        #self.setupPosterButton_Exp()
        
        # 초기 화면 설정
        self.show_screen(0)

        self.window.mainloop()

MovieQuiz()