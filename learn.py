import tkinter as tk
import file


def open_learn(path, root=None):
    words = file.get_words(path)
    if not words:
        return

    # 메인 창 숨기기
    if root:
        root.withdraw()

    learn_win = tk.Toplevel()
    learn_win.title("단어 학습")
    learn_win.geometry("420x300")

    # 상태 관리 변수
    state = {
        "index": 0,
        "is_auto": False,
        "timer_id": None,
    }

    # 화면 위젯 구성
    count_label = tk.Label(learn_win, text="", font=("맑은 고딕", 10), fg="gray")
    count_label.pack(pady=(15, 5))

    word_label = tk.Label(learn_win, text="", font=("맑은 고딕", 22, "bold"))
    word_label.pack(pady=15)

    meaning_label = tk.Label(learn_win, text="", font=("맑은 고딕", 15))
    meaning_label.pack(pady=10)

    mode_label = tk.Label(learn_win, text="현재 모드: 수동",
                          font=("맑은 고딕", 9), fg="blue")
    mode_label.pack(pady=5)

    # 현재 순서의 단어를 화면에 표시하는 함수
    def show_word():
        idx = state["index"]
        kanji, furigana, meaning = words[idx]
        count_label.config(text=f"{idx + 1} / {len(words)}")
        word_label.config(text=f"{kanji} ({furigana})")  # 후리가나 괄호 처리
        meaning_label.config(text=meaning)

    # 이전 버튼 기능
    def prev_word():
        state["index"] = (state["index"] - 1) % len(words)
        show_word()

    # 다음 버튼 기능
    def next_word():
        state["index"] = (state["index"] + 1) % len(words)
        show_word()

    # 자동 넘김 반복 실행 함수 (2000ms = 2초 간격)
    def auto_loop():
        if state["is_auto"]:
            next_word()
            state["timer_id"] = learn_win.after(2000, auto_loop)

    # 자동 / 수동 전환 버튼 기능
    def toggle_auto():
        state["is_auto"] = not state["is_auto"]
        if state["is_auto"]:
            auto_btn.config(text="자동 중지", bg="#ffd966")
            mode_label.config(text="현재 모드: 자동 (2초마다 이동)", fg="red")
            state["timer_id"] = learn_win.after(2000, auto_loop)
        else:
            auto_btn.config(text="자동", bg="SystemButtonFace")
            mode_label.config(text="현재 모드: 수동", fg="blue")
            if state["timer_id"]:
                learn_win.after_cancel(state["timer_id"])
                state["timer_id"] = None

    def exit_learn():
        if state["timer_id"]:
            learn_win.after_cancel(state["timer_id"])
        learn_win.destroy()
        if root:
            root.deiconify()

    learn_win.protocol("WM_DELETE_WINDOW", exit_learn)

    btn_frame = tk.Frame(learn_win)
    btn_frame.pack(pady=20)

    prev_btn = tk.Button(btn_frame, text="이전", width=8, command=prev_word)
    prev_btn.grid(row=0, column=0, padx=5)

    next_btn = tk.Button(btn_frame, text="다음", width=8, command=next_word)
    next_btn.grid(row=0, column=1, padx=5)

    auto_btn = tk.Button(btn_frame, text="자동", width=8, command=toggle_auto)
    auto_btn.grid(row=0, column=2, padx=5)

    exit_btn = tk.Button(btn_frame, text="나가기", width=8, command=exit_learn)
    exit_btn.grid(row=0, column=3, padx=5)

    # 첫 번째 단어 표시
    show_word()
