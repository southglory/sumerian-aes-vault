import pickle, zlib, base64

# 수메르어 변환 매핑 (알파벳 + 숫자 + 특수문자 → 수메르어)
sumerian_cipher_map = {
    # 알파벳 소문자
    "a": "𒀀",
    "b": "𒁀",
    "c": "𒍝",
    "d": "𒁕",
    "e": "𒂊",
    "f": "𒆠",
    "g": "𒂅",
    "h": "𒄭",
    "i": "𒄿",
    "j": "𒋡",
    "k": "𒆪",
    "l": "𒇷",
    "m": "𒈬",
    "n": "𒉈",
    "o": "𒌷",
    "p": "𒉿",
    "q": "𒍪",
    "r": "𒊏",
    "s": "𒊭",
    "t": "𒋾",
    "u": "𒌋",
    "v": "𒅈",
    "w": "𒂗",
    "x": "𒐊",
    "y": "𒅆",
    "z": "𒍣",
    # 숫자
    "0": "𒀹",
    "1": "𒁹",
    "2": "𒀻",
    "3": "𒀼",
    "4": "𒌝",
    "5": "𒉽",
    "6": "𒐖",
    "7": "𒐗",
    "8": "𒐘",
    "9": "𒐙",
    # Base64 특수문자
    "+": "𒃻",
    "/": "𒁺",
    "=": "𒈦",
    # 공백 및 추가 특수문자
    " ": "𒌃",
    ".": "𒁇",
    ",": "𒄑",
    "!": "𒄠",
    "?": "𒅎",
    "@": "𒀭",
    "#": "𒂔",
    "$": "𒌨",
    "%": "𒊬",
    "^": "𒅖",
    "&": "𒀝",
    "*": "𒀯",
    "(": "𒐏",
    ")": "𒐐",
    "-": "𒁲",
    "_": "𒀞",
    "[": "𒌍",
    "]": "𒌌",
    "{": "𒍢",
    "}": "𒍤",
    "|": "𒌒",
    "\\": "𒍦",
    ":": "𒌓",
    ";": "𒌇",
    '"': "𒋰",
    "'": "𒋫",
    "<": "𒉺",
    ">": "𒊒",
    "`": "𒋛",
    "~": "𒀊",
}

# 직렬화(pickle), 압축(zlib), 인코딩(base64)
encoded = base64.b64encode(zlib.compress(pickle.dumps(sumerian_cipher_map)))
print(encoded.decode())  # 복사해서 코드에 붙이면 됨

# encoded를 텍스트에 생성
with open("./version2/sumerian_cipher_map.txt", "w", encoding="utf-8") as f:
    f.write(encoded.decode())


# 복원 함수
def load_mapping():
    return pickle.loads(zlib.decompress(base64.b64decode(encoded)))


if __name__ == "__main__":
    print(load_mapping())
