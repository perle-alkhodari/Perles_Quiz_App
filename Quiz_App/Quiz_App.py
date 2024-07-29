from hmac import new
from operator import index
from tabnanny import check
from tempfile import TemporaryDirectory
from tkinter import *
from tkinter import font
from tkinter import messagebox
from turtle import bgcolor
import requests
from sqlalchemy.orm.session import DEACTIVE
from Quiz import Quizzer
from random import shuffle
from Color import Color
from Database import Database
import customtkinter
import ttkbootstrap as tb

#---------------------------------------- functions ----------------------------------------

def Disable_Buttons():
    a.config(state=DISABLED)
    b.config(state=DISABLED)
    c.config(state=DISABLED)
    d.config(state=DISABLED)

def Activate_Buttons():
    a.config(state=ACTIVE)
    b.config(state=ACTIVE)
    c.config(state=ACTIVE)
    d.config(state=ACTIVE)
    next_question.config(state=ACTIVE)
        
def Reset_Button_Colors():    
    a.config(foreground=color4, background=color2,)
    b.config(foreground=color4, background=color2,)
    c.config(foreground=color4, background=color2,)
    d.config(foreground=color4, background=color2,)
    
# Deserializing (Generating a color object from colors.txt)
def Make_Theme():
    
    with open("colors.txt") as file:
        random_colors = file.readlines()
        shuffle(random_colors)
        
    return Color(random_colors[0], "*")

# Start game   
def CheckAns():
    global i
    global position
    global score
    global correct_answer
    global all_answers
    global isRetry
    global username
    global started
    
    Reset_Button_Colors()
      
    if isRetry:
        next_question.config(
            text="Done",
            command=(CheckAns)
            )
        isRetry = False
        started = 0
        
    started += 1
    if started == 1:
        Activate_Buttons()
    
    if position <= len(quizzer.question) - 1:
        try:
            if all_answers[i] == correct_answer:
                score += 1
        except:
            pass
        
        score_label.config(text=f"Score: {score}")
        i = 10
        
        if position == 9:
            check_top_players()
            new_score = score
            old_score = Database().get_score(username)
            if new_score > old_score:
                Database().update_score(username, new_score)
                check_top_players()

            next_question.config(
                text="Retry",
                command=Reset,
                )
            Disable_Buttons()
    
    if position < len(quizzer.question) - 1:
        position += 1
        _question = quizzer.question[position]
        correct_answer = quizzer.correct_answer[position]
        wrong_answers = quizzer.wrong_answers[position]
        all_answers = wrong_answers
        all_answers.append(correct_answer)
    
        shuffle(all_answers)
    
        question.config(text=_question)
        a.config(text=all_answers[0])
        b.config(text=all_answers[1])
        c.config(text=all_answers[2])
        d.config(text=all_answers[3])
        
# Reseting game values and restarting
def Reset(difficulty="any difficulty", category=0 ):
    global i
    global position
    global score
    global correct_answer
    global all_answers
    global color
    global quizzer
    global isRetry
    global color
    global username
    
    isRetry = True
    quizzer = Quizzer(difficulty=difficulty, category=category)
    i = 10
    position = -1
    score = 0
    correct_answer = []
    all_answers = []
    color = Make_Theme()
    
    CheckAns()
    
# Save game
def save():
    global quizzer
    global username
    username = username_entry.get().title()
    if len(username) != 0:
        if len(username) < 20:
            if not Database().find_player(username):
                Database().create_player(username)
            category = categories_dictionary[choice.get()]
            difficulty = difficulty_choice.get().lower()
            check_top_players()
            Reset(difficulty=difficulty, category=category)
        else:
            messagebox.askokcancel("Username", "username too long (max 19 characters).")
    else:
        messagebox.askokcancel("Username", "Please enter your player name.")

# Leaderboard
def check_top_players():
    global row
    global first
    top_players = Database().get_top_players()
    row = 4
    
    if len(top_players) != 0:
        position = 0
        for key in top_players:
            position += 1
            label = Label(userFrame, font=("Fixedsys", 16, "bold"), text=str(position) + ". " + key + ": " + str(top_players[key]), background="#2b2b2b", foreground=color4)
            label.grid(row=row, column=0, columnspan=2, sticky="w")
            row += 1
        
    top_players = {}
    
def Reset_L():
    Database.reset_database()
    check_top_players()
       
# Button answers   
def aGuess():
    global i
    i = 0
    a.config(background=color4, foreground=color2)
    b.config(foreground=color4, background=color2,)
    c.config(foreground=color4, background=color2,)
    d.config(foreground=color4, background=color2,)

def bGuess():
    global i
    i = 1
    b.config(background=color4, foreground=color2)
    a.config(foreground=color4, background=color2,)
    c.config(foreground=color4, background=color2,)
    d.config(foreground=color4, background=color2,)

def cGuess():
    global i
    i = 2
    c.config(background=color4, foreground=color2)
    a.config(foreground=color4, background=color2,)
    b.config(foreground=color4, background=color2,)
    d.config(foreground=color4, background=color2,)

def dGuess():
    global i
    i = 3
    d.config(background=color4, foreground=color2)
    a.config(foreground=color4, background=color2,)
    b.config(foreground=color4, background=color2,)
    c.config(foreground=color4, background=color2,)

#---------------------------------------- Constants -------------------------------------------

color = Make_Theme()
color1 = color.c1
color2 = color.c2
color3 = color.c3
color4 = color.c4
color5 = color.c5
dark_color = "#2b2b2b"
FONT = ('Fixedsys', 18)
LITTLE_FONT = ('Fixedsys', 16)

#---------------------------------------- Initial Values ----------------------------------------

started = 0
i = 10
position = -1
score = 0
correct_answer = []
all_answers = []
isRetry = False
username = ""
quizzer = Quizzer()
       
#---------------------------------------- Window ------------------------------------------------

window = Tk()
window.title("Get Quizzed")
window.geometry("500x800")
window.resizable(False, False)
window.config(background=color1)
#window.wm_attributes('-transparentcolor','black') 

#---------------------------------------- Title ------------------------------------------------

label = Label(
            window,
            text="Get Quizzed",
            font=FONT,
            wraplength=500,
            bg=color1,
            foreground=color4
            )
label.grid(row=0, column=0, pady=20)

#---------------------------------------- Question ------------------------------------------------

question_frame = customtkinter.CTkScrollableFrame(window, width=350)
question_frame.grid(row=1, column=0, pady=10)

question = Label(
                question_frame,
                text="",
                wraplength=330,
                font=FONT,
                background=dark_color,
                foreground="White"
                )
question.pack()

#---------------------------------------- Answers ------------------------------------------------

div = Frame(
    window,
    background=color1,
    )
div.grid(row=2, column=0, pady=(0, 15))

a = Button(
            div,
            text="",
            font=LITTLE_FONT,
            width=45,
            command=aGuess,
            foreground=color4,
            background=color2,
            state=DISABLED
            )
a.grid(row=3, column=0)

b = Button(
            div,
            text="",
            font=LITTLE_FONT,
            width=45,
            command=bGuess,
            foreground=color4,
            background=color2,
            state=DISABLED
            )
b.grid(row=4, column=0, pady=20)

c = Button(
            div,
            text="",
            font=LITTLE_FONT,
            width=45,
            command=cGuess,
            foreground=color4,
            background=color2,
            state=DISABLED
            )
c.grid(row=5, column=0)

d = Button(
            div,
            text="",
            font=LITTLE_FONT,
            width=45,
            command=dGuess,
            foreground=color4,
            background=color2,
            state=DISABLED
            )
d.grid(row=6, column=0, pady=20)

#---------------------------------------- Next & Score ------------------------------------------------

next_question = Button(
            div,
            text="Done",
            font=LITTLE_FONT,
            width=10,
            command=CheckAns,
            foreground=color4,
            background=color2,
            state=DISABLED
            )
next_question.grid(row=7, column=0)

score = 0
score_label = Label(
         div,
         text="",
         font=(FONT),
         bg=color1,
         fg=color4,
         )
score_label.grid(row=8, column=0)

#---------------------------------------- Options ------------------------------------------------

userFrame = customtkinter.CTkScrollableFrame(window, width=350, height=200)
userFrame.grid(row=9, column=0, padx=60)

username_label = Label(
    userFrame,
    text="Name",
    font=LITTLE_FONT,
    background=dark_color,
    foreground=color4
    )
username_label.grid(row=0, column=0, sticky="w")

username_entry = Entry(
    userFrame,
    font=LITTLE_FONT,
    width=13
    )
username_entry.grid(row=1, column=0, sticky="w")
              
category_label = Label(
    userFrame,
    text="Category",
    font=LITTLE_FONT,
    background=dark_color,
    foreground=color4
    )
category_label.grid(row=0, column=1, sticky="w")

# Categories
categories_dictionary = {"Any Category": 0, "General Knowledge": 9 , "Video Games": 15, "Cartoons & Animations": 32,
                        "Mythology": 20, "Geography": 22, "Computers": 18}
choice = StringVar(userFrame)
choice.set("Any Category")
categories = OptionMenu(userFrame, choice,
                        "Any Category", "General Knowledge", "Video Games", "Cartoons & Animations",
                        "Mythology", "Geography", "Computers")
categories.config(background=dark_color, foreground=color4, activebackground=color3, activeforeground="White", borderwidth=0, highlightthickness=0)
categories.grid(row=1, column=1, padx=2, sticky="w")


difficulty_label = Label(
    userFrame,
    text="Difficulty",
    font=LITTLE_FONT,
    background=dark_color,
    foreground=color4
    )
difficulty_label.grid(row=0, column=2, sticky="w")

options = ["Any Difficulty", "Easy", "Medium", "Hard"]
difficulty_choice = StringVar(userFrame)
difficulty_choice.set(options[0])
difficulties = OptionMenu(userFrame, difficulty_choice,
                        *options)
difficulties.config(background=dark_color, foreground=color4, activebackground=color3, activeforeground="White", borderwidth=0, highlightthickness=0)
difficulties.grid(row=1, column=2, sticky="w")

save_changes = Button(
    userFrame,
    text="Save Changes & Retry",
    command=save,
    background="Black",
    foreground=color4
    )
save_changes.grid(row=2, column=0, columnspan=3, pady=10)

#---------------------------------------- Leaderboard ------------------------------------------------

top_3_players = Label(
    userFrame,
    text="Leaderboard",
    font=FONT,
    background=dark_color,
    foreground=color4,   
    )
top_3_players.grid(row=3, column=0, columnspan=3, pady=(30, 10))

row = 4
first = 0
check_top_players()


window.mainloop()
