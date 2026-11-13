from tkinter import filedialog


def Read_f():
    file_path = filedialog.askopenfilename(
        title="파일을 선택하세요",
        initialdir="/",
        filetypes=(
            ("텍스트 파일", "*.txt"),
            ("CSV 파일", "*.csv"),
            ("모든 파일", "*.*"),
        ),
    )
    return file_path


def get_content(path):
    if not path:
        return ""
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(path, "r", encoding="cp949") as f:
            return f.read()
