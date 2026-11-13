import os

WRONG_FILE = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "wrong_words.txt")


def get_wrong_words():
    """wrong_words.txt에서 틀린 단어 목록을 읽어옴"""
    if not os.path.exists(WRONG_FILE):
        return []

    words = []
    with open(WRONG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.replace("\ufeff", "").strip()
            if not line:
                continue
            row = line.split(",", 2)
            if len(row) == 3:
                words.append((row[0].strip(), row[1].strip(), row[2].strip()))
    return words


def save_wrong(kanji, furigana, meaning):
    """틀린 단어를 중복 없이 텍스트 파일에 추가 저장"""
    current = get_wrong_words()
    target = (kanji.strip(), furigana.strip(), meaning.strip())
    if target not in current:
        with open(WRONG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{target[0]},{target[1]},{target[2]}\n")


def remove_wrong(kanji, furigana, meaning):
    """오답 퀴즈에서 맞힌 단어를 텍스트 파일에서 삭제"""
    current = get_wrong_words()
    target = (kanji.strip(), furigana.strip(), meaning.strip())
    updated = [w for w in current if w != target]

    with open(WRONG_FILE, "w", encoding="utf-8") as f:
        for k, fu, m in updated:
            f.write(f"{k},{fu},{m}\n")
