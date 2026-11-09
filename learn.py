import tkinter as tk
import file as f


def next_page():

    for widget in root.winfo_children():
        widget.destroy()

        tk.Label(root, text="단어").pack(pady=20)
        tk.Label(root, text="뜻").pack(pady=20)
