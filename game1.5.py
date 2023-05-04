import random
import time
from tkinter import *

screen_1 = Tk()
screen_1.title('Ball')
screen_1.resizable(False, False)
screen_1.wm_attributes('-topmost', 1)

canvas = Canvas(
    screen_1,
    width=500,
    height=600,
)

canvas.pack()
screen_1.update()


class Ball:
    def __init__(self, canvas, color, platform, score):
        self.score = score
        self.canvas = canvas
        self.platform = platform
        self.id = self.canvas.create_oval(0, 0,
                                          30, 30, fill=color)
        self.canvas.move(self.id, 250, 250)
        start = [-3, -2, -1, 1, 2, 3]
        self.x = random.choice(start)
        self.y = -1
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 1
        elif pos[3] >= self.canvas_height:
            self.hit_bottom = True
            self.canvas.create_text(250, 200, text='ВЫ ПРОИГРАЛИ', fill='black', font=('Helvetica', 30))
        elif pos[2] >= self.canvas_width:
            self.x = -1
        elif pos[0] <= 0:
            self.x = 1
        if self.hit_platform(pos):
            self.y = -1

    def hit_platform(self, pos):
        platform_pos = self.canvas.coords(self.platform.id_2)
        if pos[2] >= platform_pos[0] and pos[0] <= platform_pos[2]:
            if platform_pos[1] <= pos[3] <= platform_pos[3]:
                self.score.hit()
                return True
        return False


class Platform:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id_2 = self.canvas.create_rectangle(200, 440,
                                                 300, 460, fill=color)
        self.x = 0
        self.canvas.bind_all('<KeyPress-Left>', self.left)
        self.canvas.bind_all('<KeyPress-Right>', self.right)
        self.canvas_width = self.canvas.winfo_width()

    def draw(self):
        self.canvas.move(self.id_2, self.x, 0)
        pos = self.canvas.coords(self.id_2)
        if pos[2] >= self.canvas_width:
            self.x = 0
        elif pos[0] <= 0:
            self.x = 0

    def left(self, event):
        self.x = -1.5

    def right(self, event):
        self.x = 1.5


class Score:
    def __init__(self, canvas):
        self.canvas = canvas
        self.score = 0
        self.text = self.canvas.create_text(450, 40, text=self.score, fill='black', font=('Helvetica', 30))

    def hit(self):
        self.score += 1
        self.canvas.itemconfig(self.text, text=self.score)


score = Score(canvas)
platform = Platform(canvas, 'blue')
ball = Ball(canvas, 'red', platform, score=score)


while True:
    if not ball.hit_bottom:
        ball.draw()
        platform.draw()
    else:
        time.sleep(2)
        break
    screen_1.update_idletasks()
    screen_1.update()
    time.sleep(.01)
