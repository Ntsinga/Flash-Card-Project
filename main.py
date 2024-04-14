"""Project 31: Flash Card App"""
from tkinter import *
import pandas
import csv, random

BACKGROUND_COLOR = "#B1DDC6"
french_word = None


# Function to generate random French words from french list
def generate_word():
    random_word = random.choice(french_words)
    return random_word


# Function for correct button
def correct_answer():
    global french_word, french_words
    global dictionary
    french_words.remove(french_word)
    del dictionary[french_word]

    # Write remaining words to csv file
    data = {"French": dictionary.keys(), "English": dictionary.values()}
    df = pandas.DataFrame(data)
    df.to_csv("data/words_to_learn.csv", index=False)

    # Flip card
    front_flip()


# Flip card to the front to show new French word
def front_flip():
    global french_word, flip_timer
    window.after_cancel(flip_timer)
    french_word = generate_word()
    canvas.itemconfig(word, text=french_word, fill="black")
    canvas.itemconfig(language, text="French", fill="black")
    canvas.itemconfig(card_image, image=card_front)
    # Start 3-second countdown to flip card to the back to show English translation
    flip_timer = window.after(3000, back_flip)


# Flip the card to the back to show English translation
def back_flip():
    # Translate to English
    global dictionary
    english_word = dictionary[french_word]
    canvas.itemconfig(card_image, image=card_back)
    canvas.itemconfig(language, text="English", fill="white")
    canvas.itemconfig(word, text=english_word, fill="white")


# Window setup
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Read csv
try:
    words = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    words = pandas.read_csv("data/french_words.csv")


# Create dictionary to store French words and their English equivalents
dictionary = {row.French: row.English for (index, row) in words.iterrows()}

# ______________OR________________________
# words.to_dict(orient="records") to create list of dictionaries

# Create a list for French words
french_words = list(words.French)
# Generate initial French word
french_word = generate_word()

# Canvas
canvas = Canvas(height=526, width=800, highlightthickness=0, bg=BACKGROUND_COLOR)
# Images for front and back
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
card_image = canvas.create_image(400, 263, image=card_front)

language = canvas.create_text(400, 150, text="French", fill="black", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text=french_word, fill="black", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# Wrong Button
wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image, command=front_flip)
wrong_button.grid(column=0, row=1)

# Right Button
correct_image = PhotoImage(file="./images/right.png")
correct_button = Button(image=correct_image, command=correct_answer)
correct_button.grid(column=1, row=1)

# 3 seconds till card is flipped to the back
flip_timer = window.after(3000, back_flip)
window.mainloop()
