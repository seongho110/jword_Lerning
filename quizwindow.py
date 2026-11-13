import tkinter as tk
import file
import quiz1
import quiz2
import randomquiz
import wrong as re
import wrong_quize


def open_quiz_window(path, root=None):
    words = file.get_words(path) if path else []

    if root:
        root.withdraw()

    quiz_win = tk.Toplevel()
    quiz_win.title("퀴즈 모드 선택")
    quiz_win.geometry("340x330")

    title_label = tk.Label(quiz_win, text="퀴즈 모드를 선택하세요",
                           font=("맑은 고딕", 14, "bold"))
    title_label.pack(pady=(18, 8))

    info_label = tk.Label(quiz_win, text="", font=("맑은 고딕", 9), fg="blue")
    info_label.pack(pady=(0, 8))

    def start_quiz1():
        if not words:
            info_label.config(text="단어장 파일을 먼저 불러와 주세요!", fg="red")
            return
        info_label.config(text="")
        quiz1.open_quiz1(words, quiz_win)

    def start_quiz2():
        if not words:
            info_label.config(text="단어장 파일을 먼저 불러와 주세요!", fg="red")
            return
        info_label.config(text="")
        quiz2.open_quiz2(words, quiz_win)

    def start_random():
        if not words:
            info_label.config(text="단어장 파일을 먼저 불러와 주세요!", fg="red")
            return
        info_label.config(text="")
        randomquiz.open_random_quiz(words, quiz_win)

    def start_wrong():
        if not re.get_wrong_words():
            info_label.config(text="저장된 오답 단어가 없습니다!", fg="red")
            return
        info_label.config(text="")
        wrong_quize.open_wrong_quiz(quiz_win, words, info_label)

    def exit_quiz_window():
        quiz_win.destroy()
        if root:
            root.deiconify()

    quiz_win.protocol("WM_DELETE_WINDOW", exit_quiz_window)

    tk.Button(quiz_win, text="일본어 -> 한국어", width=22,
              command=start_quiz1).pack(pady=5)
    tk.Button(quiz_win, text="한국어 -> 일본어", width=22,
              command=start_quiz2).pack(pady=5)
    tk.Button(quiz_win, text="랜덤", width=22, command=start_random).pack(pady=5)
    tk.Button(quiz_win, text="오답문제 퀴즈", width=22,
              command=start_wrong).pack(pady=5)
    tk.Button(quiz_win, text="나가기", width=22,
              command=exit_quiz_window).pack(pady=(12, 5))
