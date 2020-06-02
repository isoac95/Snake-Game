import tkinter as tk
from tkinter import *
from tkinter import messagebox
import time
import random

class Snak:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Snake game")
        self.root.configure(bg="dark goldenrod")
        self.width = 500
        self.height = 500
        self.score = 0
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, relief="flat", bd=0, highlightthickness=0) #padx=10, pady=10, highlightcolor="red", relief="groove", bd=0
        self.canvas.focus_set()
        self.canvas.grid(padx=5, pady=5)  #pack
        self.rows = 20
        self.columns = 20
        self.cells = dict()
        self.canvas.bind("<Configure>", self.create_field)
        self.move = StringVar()
        self.move.set(("Stand still",))
        self.move.trace("w", self.callback)
        self.canvas.bind('<Left>', lambda event: self.move.set(("Left", self.move.get()[0])))
        self.canvas.bind('<Right>', lambda event: self.move.set(("Right", self.move.get()[0])))
        self.canvas.bind('<Up>', lambda event: self.move.set(("Up", self.move.get()[0])))
        self.canvas.bind('<Down>', lambda event: self.move.set(("Down", self.move.get()[0])))
        self.canvas.after(0, self.animate)
        self.root.mainloop()

    def create_field(self, event=None):
        #self.canvas.delete("rect")
        cellwidth = int(self.canvas.winfo_width()/self.columns)
        cellheight = int(self.canvas.winfo_height()/self.columns)
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
                self.cells["i" + str(i) + "j" + str(j)] = cell
                self.canvas.tag_bind(cell, "<1>", lambda event, row=i, column=j: self.clicked(row, column))
                print("created field:", i, j)
        self.pos = (random.randint(0,19), random.randint(0,19))
        self.food = self.canvas.create_oval(self.pos[0]*25, self.pos[1]*25, self.pos[0]*25+25, self.pos[1]*25+25, fill="OrangeRed2", outline="")
        self.head = self.canvas.create_oval(250, 250, 275, 275, fill="RoyalBlue2", outline="")

    def clicked(self, row, column):
        print("clicked on:", row, column)

    def animate(self):
        self.canvas.update()
        self.move_direction(self.move.get())
        position = self.canvas.coords(self.head)
        if position[0] < 0 or position[2] > self.width or position[1] < 0 or position[3] > self.height:
            self.move.set("Stand still")
            answer = messagebox.askretrycancel("Game over!", "Better luck next time :P")
            if answer:
                self.reset()
            else:
                exit()
        if position == self.canvas.coords(self.food):
            self.score += 1
            print(self.score)
            self.canvas.delete(self.food)
            self.pos = (random.randint(0,19), random.randint(0,19))
            self.food = self.canvas.create_oval(self.pos[0]*25, self.pos[1]*25, self.pos[0]*25+25, self.pos[1]*25+25, fill="OrangeRed2", outline="")
        self.canvas.after(100, self.animate) #12

    def move_direction(self, direction):
        if direction[0] == "Stand still":
            self.canvas.move(self.head, 0, 0)
        elif direction[0] == "Left" and direction[1] != "Right":
            self.canvas.move(self.head, -25, 0)
        elif direction[0] == "Up" and direction[1] != "Down":
            self.canvas.move(self.head, 0, -25)
        elif direction[0] == "Down" and direction[1] != "Up":
            self.canvas.move(self.head, 0, 25)
        elif direction[0] == "Right" and direction[1] != "Left":
            self.canvas.move(self.head, 25, 0)

    def reset(self):
        self.canvas.delete(self.head)
        self.canvas.delete(self.food)
        self.score = 0
        self.pos = (random.randint(0,19), random.randint(0,19))
        self.food = self.canvas.create_oval(self.pos[0]*25, self.pos[1]*25, self.pos[0]*25+25, self.pos[1]*25+25, fill="OrangeRed2", outline="")
        self.head = self.canvas.create_oval(250, 250, 275, 275, fill="RoyalBlue2", outline="")

    def callback(self, *args):
        print(self.move.get())

Snak()
