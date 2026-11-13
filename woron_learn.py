import time
import tkinter as tk
import wrong as re
import sound

# 소리 OFF일 때 자동 넘김 간격 (밀리초 단위: 2500 = 2.5초)
AUTO_DELAY = 2500


def open_wrong_learn(parent_win=None, status_label=None):
    words = re.get_wrong_words()
    if not words:
        if status_label:
            status_label.config(text="저장된 오답 단어가 없습니다!", fg="red")
        return

    if parent_win:
        parent_win.withdraw()

    learn_win = tk.Toplevel()
    learn_win.title("오답 단어 학습")
    learn_win.geometry("450x350")

    state = {
        "index": 0,
        "is_auto": False,
        "timer_id": None,
        "sound_on": False,
    }

    jp_var = tk.BooleanVar(value=True)
    ko_var = tk.BooleanVar(value=False)

    def cancel_timer():
        if state["timer_id"]:
            learn_win.after_cancel(state["timer_id"])
            state["timer_id"] = None

    def speak_current():
        if not state["sound_on"]:
            sound.stop()
            return
        kanji, furigana, meaning = words[state["index"]]
        sound.speak(kanji, furigana, meaning, jp_var.get(), ko_var.get())

    def schedule_next():
        cancel_timer()
        if not state["is_auto"]:
            return

        if state["sound_on"] and (jp_var.get() or ko_var.get()):
            start_time = time.time()
            state["timer_id"] = learn_win.after(
                150, lambda: wait_sound_end(start_time))
        else:
            state["timer_id"] = learn_win.after(AUTO_DELAY, next_word)

    def wait_sound_end(start_time):
        if not state["is_auto"]:
            return
        if sound.is_speaking() and (time.time() - start_time < 8.0):
            state["timer_id"] = learn_win.after(
                150, lambda: wait_sound_end(start_time))
        else:
            state["timer_id"] = learn_win.after(600, next_word)

    def update_mode_label():
        if not state["is_auto"]:
            mode_label.config(text="현재 모드: 수동", fg="blue")
        elif state["sound_on"]:
            mode_label.config(text="현재 모드: 자동 (소리 끝나면 이동)", fg="red")
        else:
            sec = AUTO_DELAY / 1000
            mode_label.config(text=f"현재 모드: 자동 ({sec:g}초마다 이동)", fg="red")

    def toggle_sound():
        state["sound_on"] = not state["sound_on"]
        if state["sound_on"]:
            sound_btn.config(text="🔊 소리 ON", bg="#d9ead3")
            speak_current()
        else:
            sound_btn.config(text="🔇 소리 OFF", bg="SystemButtonFace")
            sound.stop()
        update_mode_label()
        schedule_next()

    def on_check_change():
        if state["sound_on"]:
            speak_current()
            schedule_next()

    # --- [우측 상단] 소리 버튼 + 체크박스 ---
    top_bar = tk.Frame(learn_win)
    top_bar.pack(fill="x", padx=12, pady=(10, 0))

    sound_box = tk.Frame(top_bar, relief="groove", bd=2, padx=6, pady=4)
    sound_box.pack(side="right")

    sound_btn = tk.Button(sound_box, text="🔇 소리 OFF",
                          width=13, command=toggle_sound)
    sound_btn.pack()

    chk_frame = tk.Frame(sound_box)
    chk_frame.pack(pady=(3, 0))

    jp_chk = tk.Checkbutton(chk_frame, text="일본어",
                            variable=jp_var, command=on_check_change)
    jp_chk.pack(side="left")

    ko_chk = tk.Checkbutton(chk_frame, text="한국어",
                            variable=ko_var, command=on_check_change)
    ko_chk.pack(side="left")

    # --- 단어 표시 영역 ---
    count_label = tk.Label(learn_win, text="", font=("맑은 고딕", 10), fg="gray")
    count_label.pack(pady=(5, 5))

    word_label = tk.Label(learn_win, text="", font=("맑은 고딕", 22, "bold"))
    word_label.pack(pady=12)

    meaning_label = tk.Label(learn_win, text="", font=("맑은 고딕", 15))
    meaning_label.pack(pady=8)

    mode_label = tk.Label(learn_win, text="현재 모드: 수동",
                          font=("맑은 고딕", 9), fg="blue")
    mode_label.pack(pady=5)

    def show_word():
        cancel_timer()
        idx = state["index"]
        kanji, furigana, meaning = words[idx]
        count_label.config(text=f"오답 {idx + 1} / {len(words)}")
        word_label.config(text=f"{kanji} ({furigana})")
        meaning_label.config(text=meaning)
        speak_current()
        schedule_next()

    def prev_word():
        state["index"] = (state["index"] - 1) % len(words)
        show_word()

    def next_word():
        state["index"] = (state["index"] + 1) % len(words)
        show_word()

    def toggle_auto():
        state["is_auto"] = not state["is_auto"]
        if state["is_auto"]:
            auto_btn.config(text="자동 중지", bg="#ffd966")
        else:
            auto_btn.config(text="자동", bg="SystemButtonFace")
            cancel_timer()
        update_mode_label()
        schedule_next()

    def exit_learn():
        sound.stop()
        cancel_timer()
        learn_win.destroy()
        if parent_win:
            parent_win.deiconify()

    learn_win.protocol("WM_DELETE_WINDOW", exit_learn)

    # --- 하단 버튼 영역 ---
    btn_frame = tk.Frame(learn_win)
    btn_frame.pack(pady=15)

    prev_btn = tk.Button(btn_frame, text="이전", width=8, command=prev_word)
    prev_btn.grid(row=0, column=0, padx=5)

    next_btn = tk.Button(btn_frame, text="다음", width=8, command=next_word)
    next_btn.grid(row=0, column=1, padx=5)

    auto_btn = tk.Button(btn_frame, text="자동", width=8, command=toggle_auto)
    auto_btn.grid(row=0, column=2, padx=5)

    exit_btn = tk.Button(btn_frame, text="나가기", width=8, command=exit_learn)
    exit_btn.grid(row=0, column=3, padx=5)

    show_word()
