import tkinter as tk
import file

root = tk.Tk()

label = tk.Label(root, text="단어학습")
label.pack()

label2 = tk.Label(root, text="파일불러오기")
label2.pack()

f_Button = tk.Button(root, text="불러오기", command=file.Read_f)
f_Button.pack()

l_Button = tk.Button(root, text="학습")
l_Button.pack()

q_Button = tk.Button(root, text="퀴즈")
q_Button.pack()

re_Button = tk.Button(root, text="오답")
re_Button.pack()

root.mainloop()
