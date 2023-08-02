import os
from tkinter import *
from random import choice
import pandas

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Ariel"

# ---------------------------- GET DATA FROM CSV ------------------------------- #
file_path = "data/words_to_learn.csv"
if os.path.exists(file_path):
    data = pandas.read_csv(file_path)
    if os.path.getsize(file_path) < 5:
        os.remove(file_path)
        data = pandas.read_csv("data/french_words.csv")
else:
    data = pandas.read_csv("data/french_words.csv")

to_learn = data.to_dict(orient="records")
current_card = {}


def remove_word():
    global current_card, to_learn
    to_learn.remove(current_card)
    pandas.DataFrame(to_learn).to_csv(file_path, index=False)
    if not to_learn:
        window.destroy()
        return
    pick_random_word()


def pick_random_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(to_learn)
    canvas.itemconfig(canvas_image, image=front_image)
    canvas.itemconfig(flash_card_language, text="French", fill="black")
    canvas.itemconfig(flash_card_text, text=current_card["French"], fill="black")
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(canvas_image, image=back_image)
    canvas.itemconfig(flash_card_language, text="English", fill="white")
    canvas.itemconfig(flash_card_text, text=current_card["English"], fill="white")


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=front_image)
canvas.grid(row=0, column=0, columnspan=2)
flash_card_language = canvas.create_text(400, 150, text="", font=(FONT_NAME, 40, "italic"))
flash_card_text = canvas.create_text(400, 263, text="", font=(FONT_NAME, 60, "italic"))

unknown_card_image = PhotoImage(file="images/wrong.png")
button_unknown = Button(image=unknown_card_image, highlightthickness=0, command=pick_random_word)
button_unknown.grid(row=1, column=0)
known_card_image = PhotoImage(file="images/right.png")
known_button = Button(image=known_card_image, highlightthickness=0, command=remove_word)
known_button.grid(row=1, column=1)

pick_random_word()

window.mainloop()
