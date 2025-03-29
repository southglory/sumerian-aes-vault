import tkinter as tk
from tkinter import messagebox
from Crypto.Cipher import AES
import base64
import os


def pad(s):
    """AES 블록 크기(16바이트)에 맞게 패딩 추가"""
    return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)


def unpad(s):
    """AES 패딩 제거"""
    return s[: -ord(s[-1])]


def encrypt_aes(password, key):
    key = key.ljust(32)[:32].encode()
    iv = os.urandom(16)  # 🔹 랜덤 IV 생성 (CBC 모드)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(password).encode())  # 🔹 PKCS7 패딩 적용
    return base64.b64encode(iv + encrypted).decode()  # 🔹 Base64 변환


def decrypt_aes(encrypted_password, key):
    key = key.ljust(32)[:32].encode()

    try:
        print(f"[DEBUG] 복호화 전 Base64 문자열: {encrypted_password}")  # Base64 복호화 전 확인
        encrypted_password = base64.b64decode(encrypted_password)  # Base64 디코딩
    except Exception as e:
        print(f"[ERROR] Base64 디코딩 실패: {e}")
        return None

    iv = encrypted_password[:16]  # CBC 모드에서 IV 추출
    encrypted_text = encrypted_password[16:]  # 실제 암호문

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_bytes = cipher.decrypt(encrypted_text)  # AES 복호화

    print(f"[DEBUG] AES 복호화된 바이트 데이터: {decrypted_bytes}")  # 🔹 복호화 후 데이터 확인

    try:
        decrypted_text = unpad(decrypted_bytes.decode())  # UTF-8 디코딩 및 패딩 제거
    except UnicodeDecodeError as e:
        print(f"[ERROR] 복호화된 데이터 UTF-8 디코딩 실패: {e}")
        return None

    print(f"[DEBUG] 최종 복호화된 텍스트: {decrypted_text}")  # 최종 결과 확인
    return decrypted_text


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


def encrypt_sumerian(text):
    """AES 암호화된 Base64를 수메르 문자로 변환 (Base64 패딩 유지)"""
    return "".join(sumerian_cipher_map.get(char.lower(), char) if char in sumerian_cipher_map else char for char in text)


def decrypt_sumerian(text):
    """수메르 문자에서 원래 Base64로 복원"""
    reverse_map = {v: k for k, v in sumerian_cipher_map.items()}
    return "".join(reverse_map.get(char, char) for char in text)


def encrypt_password(password, key):
    """AES-256 + CBC로 암호화 후 수메르어 변환"""
    encrypted_aes = encrypt_aes(password, key)
    return encrypt_sumerian(encrypted_aes)


def decrypt_password(encrypted_password, key):
    """수메르어 복호화 후 AES-256 + CBC 복호화"""
    decrypted_sumerian = decrypt_sumerian(encrypted_password)
    return decrypt_aes(decrypted_sumerian, key)


def process():
    text = input_text.get("1.0", tk.END).strip()
    key = key_entry.get().strip()
    if not text or not key:
        messagebox.showwarning("입력 오류", "텍스트와 키를 입력하세요!")
        return
    if mode_var.get() == "encrypt":
        result = encrypt_password(text, key)
    else:
        result = decrypt_password(text, key)
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)
    output_text.config(state=tk.DISABLED)


def exit_app():
    root.destroy()


root = tk.Tk()
root.title("AES-256 + 수메르어 변환 암호화 도구")
root.geometry("400x500")

custom_font = ("Segoe UI Historic", 12)

mode_var = tk.StringVar(value="encrypt")
tk.Label(root, text="암호화 / 복호화 선택", font=custom_font).pack()
mode_switch = tk.OptionMenu(root, mode_var, "encrypt", "decrypt")
mode_switch.pack()

tk.Label(root, text="텍스트 입력", font=custom_font).pack()
input_text = tk.Text(root, height=4, width=50, font=custom_font)
input_text.pack()

tk.Label(root, text="암호화 키 입력", font=custom_font).pack()
key_entry = tk.Entry(root, show="*", width=40, font=custom_font)
key_entry.pack()

tk.Label(root, text="출력 결과", font=custom_font).pack()
output_text = tk.Text(root, height=4, width=50, state=tk.DISABLED, font=custom_font)
output_text.pack()

tk.Button(root, text="실행", font=custom_font, command=process).pack()
tk.Button(root, text="종료", font=custom_font, command=exit_app).pack()

root.mainloop()
