import tkinter as tk
from tkinter import messagebox
from Crypto.Cipher import AES
import base64
import os


def pad(s):
    """Add padding to match AES block size (16 bytes)"""
    return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)


def unpad(s):
    """Remove AES padding"""
    return s[: -ord(s[-1])]


def encrypt_aes(password, key):
    key = key.ljust(32)[:32].encode()
    iv = os.urandom(16)  # 🔹 Generate random IV (CBC mode)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(password).encode())  # 🔹 Apply PKCS7 padding
    return base64.b64encode(iv + encrypted).decode()  # 🔹 Convert to Base64


def decrypt_aes(encrypted_password, key):
    key = key.ljust(32)[:32].encode()

    try:
        print(f"[DEBUG] Base64 string before decryption: {encrypted_password}")  # Check Base64 before decryption
        encrypted_password = base64.b64decode(encrypted_password)  # Base64 decoding
    except Exception as e:
        print(f"[ERROR] Base64 decoding failed: {e}")
        return None

    iv = encrypted_password[:16]  # Extract IV for CBC mode
    encrypted_text = encrypted_password[16:]  # Actual ciphertext

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_bytes = cipher.decrypt(encrypted_text)  # AES decryption

    print(f"[DEBUG] AES decrypted byte data: {decrypted_bytes}")  # 🔹 Check data after decryption

    try:
        decrypted_text = unpad(decrypted_bytes.decode())  # UTF-8 decoding and padding removal
    except UnicodeDecodeError as e:
        print(f"[ERROR] UTF-8 decoding of decrypted data failed: {e}")
        return None

    print(f"[DEBUG] Final decrypted text: {decrypted_text}")  # Check final result
    return decrypted_text


# Sumerian conversion mapping (alphabet + numbers + special characters → Sumerian)
sumerian_cipher_map = {
    # Lowercase letters
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
    # Numbers
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
    # Base64 special characters
    "+": "𒃻",
    "/": "𒁺",
    "=": "𒈦",
    # Space and additional special characters
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
    """Convert AES encrypted Base64 to Sumerian characters (maintain Base64 padding)"""
    return "".join(sumerian_cipher_map.get(char.lower(), char) if char in sumerian_cipher_map else char for char in text)


def decrypt_sumerian(text):
    """Restore original Base64 from Sumerian characters"""
    reverse_map = {v: k for k, v in sumerian_cipher_map.items()}
    return "".join(reverse_map.get(char, char) for char in text)


def encrypt_password(password, key):
    """Encrypt with AES-256 + CBC then convert to Sumerian"""
    encrypted_aes = encrypt_aes(password, key)
    return encrypt_sumerian(encrypted_aes)


def decrypt_password(encrypted_password, key):
    """Decrypt from Sumerian then AES-256 + CBC"""
    decrypted_sumerian = decrypt_sumerian(encrypted_password)
    return decrypt_aes(decrypted_sumerian, key)


def process():
    text = input_text.get("1.0", tk.END).strip()
    key = key_entry.get().strip()
    if not text or not key:
        messagebox.showwarning("Input Error", "Please enter both text and key!")
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
root.title("AES-256 + Sumerian Character Conversion Tool")
root.geometry("400x500")

custom_font = ("Segoe UI Historic", 12)

mode_var = tk.StringVar(value="encrypt")
tk.Label(root, text="Select Mode", font=custom_font).pack()
mode_switch = tk.OptionMenu(root, mode_var, "encrypt", "decrypt")
mode_switch.pack()

tk.Label(root, text="Enter Text", font=custom_font).pack()
input_text = tk.Text(root, height=4, width=50, font=custom_font)
input_text.pack()

tk.Label(root, text="Enter Encryption Key", font=custom_font).pack()
key_entry = tk.Entry(root, show="*", width=40, font=custom_font)
key_entry.pack()

tk.Label(root, text="Output Result", font=custom_font).pack()
output_text = tk.Text(root, height=4, width=50, state=tk.DISABLED, font=custom_font)
output_text.pack()

tk.Button(root, text="Execute", font=custom_font, command=process).pack()
tk.Button(root, text="Exit", font=custom_font, command=exit_app).pack()

root.mainloop()
