from tkinter import *
from tkinter import messagebox
from tkinter import font
from PIL import ImageTk, Image
from MovieQuery import *

class MovieQuiz:
    def show_screen(self, screen_num):  # ȭ�� ��ȯ�� ó���ϴ� �Լ�
        screens = [self.screen0_frame, self.screen1_frame, self.screen2_frame, self.screen3_frame]
        for i, screen in enumerate(screens):
            if i == screen_num:
                screen.pack()
            else:
                screen.pack_forget()

    def setupImageButton(self):  # �̹��� ��ư ���� �� ��ġ
        button_coordinates = [(20, 20), (20, 220), (20, 420), (20, 620)] # ���� ������ �� ��ư 4��
        for i, (x, y) in enumerate(button_coordinates):
            image_button = Button(self.left_frame, width=80, height=80, command=lambda num=i: self.show_screen(num))
            image_button.place(x=x, y=y)
            self.image_buttons.append(image_button)

    def setupPosterButton(self):  # ������ ��ư ���� �� ��ġ
        button_coordinates = [(40, 340), (240, 340), (40, 560), (240, 560)] # ���� ȭ�� ������ �� ����Ʈ ��ư 4��
        for i, (x, y) in enumerate(button_coordinates):
            poster_button = Button(self.screen0_frame, width=150, height=200)
            poster_button.place(x=x, y=y)
            self.poster_buttons.append(poster_button)

    def setImageButton(self):   # �̹��� �ε� �� ��ư�� �̹��� ����
        image_filenames = ["����ǥ.png", "��.png", "�׷���.png", "��ȭ��.png"]
        for i, filename in enumerate(image_filenames):
            image = Image.open(filename)
            image = image.resize((80, 80))
            photo = ImageTk.PhotoImage(image)
            self.image_buttons[i].config(image=photo)
            self.image_buttons[i].image = photo

    def setPosterButton(self):  # ������ �̹��� �ε� �� ��ư�� ������ �̹��� ����
        image_filenames = ["answer_poster.jpg", "poster0.jpg", "poster1.jpg", "poster2.jpg"]
        for i, filename in enumerate(image_filenames):
            image = Image.open(filename)
            image = image.resize((150, 200))
            photo = ImageTk.PhotoImage(image)
            self.poster_buttons[i].config(image=photo)
            self.poster_buttons[i].image = photo

    def setupLabel(self):
        label_texts = ["New ����", "���ã��", "�ֱ�������", "�� ��ȭ��"]
        label_coordinates = [(10, 120), (10, 320), (10, 520), (10, 720)]
        for text, (x, y) in zip(label_texts, label_coordinates):
            label = Label(self.left_frame, text=text, width=10, height=1, font=self.fontstyle)
            label.place(x=x, y=y)

    def __init__(self):
        # tkinter ������ ����
        self.window = Tk()
        self.window.title("TEST_GUI")
        self.window.geometry("600x800")
        self.window.configure(bg='white')
        self.fontstyle = font.Font(self.window, size=8, weight='bold', family='Consolas')
        self.fontstyle = font.Font(self.window, size=14, weight='bold', family='Consolas')

        self.left_frame = Frame(self.window, width=130, height=800) # ���� ������ ����
        self.left_frame.pack(side="left")

        self.screen0_frame = Frame(self.window, width=470, height=800, bg="cyan")  # new���� ȭ��
        self.screen1_frame = Frame(self.window, width=470, height=800, bg="white")  # ���ã�� ȭ��
        self.screen2_frame = Frame(self.window, width=470, height=800, bg="white")  # �ֱ� ������ ȭ��
        self.screen3_frame = Frame(self.window, width=470, height=800, bg="white")  # �� ��ȭ�� ȭ��

        self.image_buttons = []
        self.poster_buttons = []
        self.setupImageButton()
        self.setImageButton()
        self.setupLabel()

        self.movie = MovieQuery()
        self.movie_query = self.movie.getRandomQuery()
        self.movie.PosterDownload(self.movie_query, -1) # -1�� ������ ��ȭ ������
        self.movie.getMovieInfo(self.movie_query)

        # �ʱ� ȭ�� ����
        self.show_screen(0)
        
        # screen0_frame�� �ؽ�Ʈ ������ ��� �ڽ��� ��ũ�ѹ� ����
        self.text_box = Text(self.screen0_frame, width=60, height=15)
        '''
        self.scrollbar = Scrollbar(self.screen0_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # �ؽ�Ʈ �ڽ��� ��ũ�ѹ� ����
        self.text_box.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_box.yview)
        '''

        # �ؽ�Ʈ �ڽ� ��ܿ� ��ġ
        self.text_box.place(x=20, y=20)
      
        self.set_MovieOverview()
        similar_movies = self.movie.getSimilarGenreMovies(self.movie_query)
        if similar_movies:
            for i, movie in enumerate(similar_movies[:3]):
                self.movie.PosterDownload(movie, i)
     
        # ������ �̹��� ��ư ����
        self.setupPosterButton()
        self.setPosterButton()

        self.window.mainloop()

    def set_MovieOverview(self): # �ؽ�Ʈ �ڽ��� �˻� ��� ����
        
        self.text_box.delete('1.0', END)  # ���� ���� ����

        overview = self.movie.getMovieOverview(self.movie_query)
        info = f"{overview}\n\n"
        self.text_box.insert(END, info)

MovieQuiz()