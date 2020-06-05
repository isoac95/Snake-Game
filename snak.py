import tkinter as tk
from tkinter import *
from tkinter import messagebox
import time
import random

class Snak:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Snake game by Ante Culo")
        self.root.configure(bg="SpringGreen2")
        self.score = 0
        self.high_score = 0
        self.label = tk.Label(self.root, text="Use arrow keys for\nsnake movement!", fg="white", bg="SpringGreen2", font=("Arial", 15))
        self.label.pack()
        self.frame = tk.Frame(self.root, bg="dark goldenrod")
        self.frame.pack()
        self.width = 500
        self.height = 500
        self.canvas = tk.Canvas(self.frame, width=self.width, height=self.height, relief="flat", bd=0, highlightthickness=0) #padx=10, pady=10, highlightcolor="red", relief="groove", bd=0
        self.canvas.focus_set()
        self.canvas.pack(padx=5, pady=5)
        self.rows = 20
        self.columns = 20
        self.canvas.bind("<Configure>", self.create_field)
        self.last_command = ""
        self.move = StringVar()
        self.move.set("Stand still")
        self.move.trace("w", self.callback)
        self.canvas.bind('<Left>', lambda event: self.move.set("Left"))
        self.canvas.bind('<Right>', lambda event: self.move.set("Right"))
        self.canvas.bind('<Up>', lambda event: self.move.set("Up"))
        self.canvas.bind('<Down>', lambda event: self.move.set("Down"))
        self.canvas.after(0, self.animate)
        self.root.mainloop()

    def create_field(self, event=None):
        cellwidth = int(self.canvas.winfo_width()/self.columns)
        cellheight = int(self.canvas.winfo_height()/self.rows)
        for i in range(self.columns):
            for j in range(self.rows):
                x1 = j * cellwidth
                y1 = i * cellheight
                x2 = x1 + cellwidth
                y2 = y1 + cellheight
                if (i + j) % 2 == 0:
                    cell = self.canvas.create_rectangle(x1,y1,x2,y2, fill="SpringGreen2", tags="rect", outline="")
                else:
                    cell = self.canvas.create_rectangle(x1,y1,x2,y2, fill="SpringGreen3", tags="rect", outline="")
        self.pos = (random.randint(0,19), random.randint(0,19))
        self.food = self.canvas.create_oval(self.pos[0]*25, self.pos[1]*25, self.pos[0]*25+25, self.pos[1]*25+25, fill="OrangeRed2", outline="")
        self.head = self.canvas.create_oval(250, 250, 275, 275, fill="RoyalBlue3", outline="")
        self.lst = [[self.head, [250, 250, 275, 275]],
        [self.canvas.create_oval(225, 250, 250, 275, fill="RoyalBlue2", outline=""),[225, 250, 250, 275]],
        [self.canvas.create_oval(200, 250, 225, 275, fill="RoyalBlue2", outline=""), [200, 250, 225, 275]],
        [self.canvas.create_oval(175, 250, 200, 275, fill="RoyalBlue2", outline=""), [175, 250, 200, 275]]]

    def animate(self):
        self.canvas.update()
        if self.last_command == self.move.get():
            self.move_direction(self.move.get())
        else:
            self.move_direction(self.last_command)
        position = self.canvas.coords(self.head)
        lst_of_pos = list()
        for index in range(1, len(self.lst)):
            lst_of_pos.append(self.lst[index][1])
        if position[0] < 0 or position[2] > self.width or position[1] < 0 or position[3] > self.height or position in lst_of_pos:
            self.move.set("Stand still")
            answer = messagebox.askretrycancel("Game over!", "Better luck next time :P")
            if answer:
                self.reset()
            else:
                exit()
        if position == self.canvas.coords(self.food):
            self.score += 1
            self.label.configure(text="High score: {}\nCurrent score: {}".format(self.high_score, self.score))
            print(self.score)
            self.create_food(lst_of_pos)
            self.lst.append([self.canvas.create_oval(1000, 1000, 1025, 1025, fill="RoyalBlue2", outline=""), [175, 250, 200, 275]])
        self.canvas.after(100, self.animate)

    def move_direction(self, direction):
        if direction == "Stand still":
            self.canvas.move(self.head, 0, 0)
        elif direction == "Left":
            if len(self.lst) == 4 and self.canvas.coords(self.head) == [250, 250, 275, 275] and self.lst[1][1] == [225, 250, 250, 275]:
                self.move.set("Stand still")
                self.last_command = ""
                self.canvas.move(self.head, 0, 0)
            else:
                self.canvas.move(self.head, -25, 0)
        elif direction == "Up":
            self.canvas.move(self.head, 0, -25)
        elif direction == "Down":
            self.canvas.move(self.head, 0, 25)
        elif direction == "Right":
            self.canvas.move(self.head, 25, 0)
        if self.move.get() != "Stand still":
            temp_coord = self.lst[0][1]
            for index in range(1, len(self.lst)):
                value = self.lst[index][1]
                self.canvas.coords(self.lst[index][0], temp_coord)
                self.lst[index][1] = temp_coord
                temp_coord = value
            self.lst[0][1] = self.canvas.coords(self.head)

    def reset(self):
        self.canvas.delete(self.food)
        for item in self.lst:
            self.canvas.delete(item[0])
        if self.score > self.high_score:
            self.high_score = self.score
        self.score = 0
        self.label.configure(text="High score: {}\nCurrent score: {}".format(self.high_score, self.score))
        self.pos = (random.randint(0,19), random.randint(0,19))
        self.food = self.canvas.create_oval(self.pos[0]*25, self.pos[1]*25, self.pos[0]*25+25, self.pos[1]*25+25, fill="OrangeRed2", outline="")
        self.head = self.canvas.create_oval(250, 250, 275, 275, fill="RoyalBlue3", outline="")
        self.lst = [[self.head, [250, 250, 275, 275]],
        [self.canvas.create_oval(225, 250, 250, 275, fill="RoyalBlue2", outline=""),[225, 250, 250, 275]],
        [self.canvas.create_oval(200, 250, 225, 275, fill="RoyalBlue2", outline=""), [200, 250, 225, 275]],
        [self.canvas.create_oval(175, 250, 200, 275, fill="RoyalBlue2", outline=""), [175, 250, 200, 275]]]
        self.last_command = ""

    def create_food(self, snake_position):
        self.canvas.delete(self.food)
        self.pos = (random.randint(0,19), random.randint(0,19))
        if [self.pos[0]*25, self.pos[1]*25, self.pos[0]*25+25, self.pos[1]*25+25] not in snake_position:
            self.food = self.canvas.create_oval(self.pos[0]*25, self.pos[1]*25, self.pos[0]*25+25, self.pos[1]*25+25, fill="OrangeRed2", outline="")
        else:
            self.create_food(snake_position)

    def callback(self, *args):
        #print("Current command: {}, previos command: {}".format(self.move.get(), self.last_command))
        if self.last_command == "":
            self.last_command = self.move.get()
        elif self.last_command == "Left" and self.move.get() != "Right":
            self.last_command = self.move.get()
        elif self.last_command == "Right" and self.move.get() != "Left":
            self.last_command = self.move.get()
        elif self.last_command == "Up" and self.move.get() != "Down":
            self.last_command = self.move.get()
        elif self.last_command == "Down" and self.move.get() != "Up":
            self.last_command = self.move.get()

Snak()
