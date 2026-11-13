from tkinter import filedialog


def Read_f():
    file_path = filedialog.askopenfilename(
        title="파일을 선택하세요",
        initialdir="/",
        filetypes=(
            ("단어장 파일", "*.csv;*.txt"),
            ("CSV 파일", "*.csv"),
            ("텍스트 파일", "*.txt"),

        ),
    )
    return file_path


def get_words(path):
    if not path:
        return []

    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        with open(path, "r", encoding="cp949") as f:
            lines = f.readlines()

    words = []
    for line in lines:
        # 1. 줄 맨 끝에 붙은 엔터(\n)와 앞뒤 공백만 제거
        line = line.strip()
        if not line:
            continue

        row = line.split(",", 2)
        if len(row) < 3:
            continue

        kanji = row[0].strip()
        furigana = row[1].strip()
        meaning = row[2].strip()

        # 첫 번째 제목 줄("한자,요미가나,뜻") 건너뛰기
        if kanji == "한자" and furigana == "요미가나":
            continue

        words.append((kanji, furigana, meaning))

    return words
