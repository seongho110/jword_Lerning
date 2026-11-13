import tkinter as tk
import file


def open_learn(path):
    learn_win = tk.Toplevel()
    learn_win.title("단어 학습")
    learn_win.geometry("400x300")

    label = tk.Label(learn_win, text="")
    label.pack(pady=20)

    content = file.get_content(path)
    label.config(text=content)
