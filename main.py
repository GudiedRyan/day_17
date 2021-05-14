from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

try:
    word_bank = pandas.read_csv("data/words_to_learn.csv")
    to_learn = word_bank.to_dict(orient="records")
except FileNotFoundError:
    word_bank = pandas.read_csv("data/french_words.csv")
    to_learn = word_bank.to_dict(orient="records")
new_word = {}
#<-------------------------- Word Gen -------------------------->#

def next_card():
    global new_word, flip_timer
    window.after_cancel(flip_timer)
    new_word = random.choice(to_learn)
    canvas.itemconfig(card, image=card_front)
    canvas.itemconfig(language_label, text="French", fill="black")
    canvas.itemconfig(word_label, text=new_word["French"], fill="black")
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(card, image=card_back)
    canvas.itemconfig(language_label, text="English", fill="white")
    canvas.itemconfig(word_label, text=new_word["English"], fill="white")
    
def known_word():
    to_learn.remove(new_word)
    next_card()
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
#<-------------------------- UI -------------------------->#

window = Tk()
window.title("Flash Card Game")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card = canvas.create_image(400, 263, image=card_front)
language_label = canvas.create_text(400, 150, text="", fill="black", font=("Arial", 40, "italic"))
word_label = canvas.create_text(400, 263, text="", fill="black", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=known_word)
right_button.grid(row=1, column=1)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

next_card()

window.mainloop()