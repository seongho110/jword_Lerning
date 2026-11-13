import random
import tkinter as tk
import wrong as re


def open_quiz1(words, parent_win=None):
    if not words:
        return

    if parent_win:
        parent_win.withdraw()

    win = tk.Toplevel()
    win.title("일본어 → 한국어 퀴즈")
    win.geometry("460x430")

    quiz_words = list(words)
    random.shuffle(quiz_words)

    questions = []
    for word in quiz_words:
        kanji, furigana, meaning = word
        q_text = f"{kanji} ({furigana})"
        correct_text = meaning
        wrong_candidates = list({w[2] for w in words if w[2] != correct_text})

        distractors = random.sample(
            wrong_candidates, min(3, len(wrong_candidates)))
        options = distractors + [correct_text]
        random.shuffle(options)

        questions.append({
            "word": word,
            "q_text": q_text,
            "correct": correct_text,
            "options": options,
            "selected": None,
            "is_correct": None,
        })

    state = {"index": 0}

    count_label = tk.Label(win, text="", font=("맑은 고딕", 10), fg="gray")
    count_label.pack(pady=(12, 4))

    question_label = tk.Label(win, text="", font=(
        "맑은 고딕", 20, "bold"), wraplength=420)
    question_label.pack(pady=12)

    result_label = tk.Label(win, text="", font=("맑은 고딕", 12, "bold"))
    result_label.pack(pady=6)

    opt_frame = tk.Frame(win)
    opt_frame.pack(pady=8)

    opt_buttons = []
    for i in range(4):
        btn = tk.Button(
            opt_frame,
            text="",
            width=32,
            font=("맑은 고딕", 11),
            command=lambda idx=i: check_answer(idx),
        )
        btn.pack(pady=4)
        opt_buttons.append(btn)

    def render_question():
        q = questions[state["index"]]
        count_label.config(text=f"{state['index'] + 1} / {len(questions)}")
        question_label.config(text=q["q_text"])

        for i, btn in enumerate(opt_buttons):
            if i < len(q["options"]):
                btn.config(text=q["options"][i], bg="SystemButtonFace")
            else:
                btn.config(text="", bg="SystemButtonFace")

        if q["selected"] is None:
            result_label.config(text="알맞은 뜻을 선택하세요.", fg="gray")
        else:
            for btn in opt_buttons:
                if btn.cget("text") == q["correct"]:
                    btn.config(bg="#d9ead3")
                elif btn.cget("text") == q["selected"] and not q["is_correct"]:
                    btn.config(bg="#f4cccc")

            if q["is_correct"]:
                result_label.config(text="정답입니다!", fg="green")
            else:
                result_label.config(
                    text=f"틀렸습니다! 정답: {q['correct']}", fg="red")

    def check_answer(btn_idx):
        q = questions[state["index"]]
        if q["selected"] is not None or btn_idx >= len(q["options"]):
            return

        chosen = q["options"][btn_idx]
        q["selected"] = chosen

        if chosen == q["correct"]:
            q["is_correct"] = True
        else:
            q["is_correct"] = False
            k, fu, m = q["word"]
            re.save_wrong(k, fu, m)

        render_question()

    def prev_q():
        state["index"] = (state["index"] - 1) % len(questions)
        render_question()

    def next_q():
        state["index"] = (state["index"] + 1) % len(questions)
        render_question()

    def exit_quiz():
        win.destroy()
        if parent_win:
            parent_win.deiconify()

    win.protocol("WM_DELETE_WINDOW", exit_quiz)

    nav_frame = tk.Frame(win)
    nav_frame.pack(pady=14)

    tk.Button(nav_frame, text="이전", width=9, command=prev_q).grid(
        row=0, column=0, padx=6)
    tk.Button(nav_frame, text="다음", width=9, command=next_q).grid(
        row=0, column=1, padx=6)
    tk.Button(nav_frame, text="나가기", width=9,
              command=exit_quiz).grid(row=0, column=2, padx=6)

    render_question()
