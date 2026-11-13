import tkinter as tk
import file
import learn

root = tk.Tk()
root.title("단어장 프로그램")
root.geometry("300x250")

saved_path = ""


def load_file():
    global saved_path
    path = file.Read_f()
    if path:
        saved_path = path
        file_name = path.split("/")[-1]
        label2.config(text=f"불러온 파일: {file_name}")


def go_learn():
    if saved_path:
        learn.open_learn(saved_path)
    else:
        label2.config(text="먼저 파일을 불러와 주세요!")


label = tk.Label(root, text="단어학습")
label.pack(pady=5)

label2 = tk.Label(root, text="파일불러오기")
label2.pack(pady=5)

f_Button = tk.Button(root, text="불러오기", command=load_file)
f_Button.pack(pady=5)

l_Button = tk.Button(root, text="학습", command=go_learn)
l_Button.pack(pady=5)

q_Button = tk.Button(root, text="퀴즈")
q_Button.pack(pady=5)

re_Button = tk.Button(root, text="오답")
re_Button.pack(pady=5)

root.mainloop()
