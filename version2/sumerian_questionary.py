import sys
from Crypto.Cipher import AES
import base64, zlib, pickle
import os
import questionary


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


with open(os.path.dirname(__file__) + "/sumerian_cipher_map.txt", "r", encoding="utf-8") as f:
    encoded = f.read().encode()

sumerian_cipher_map = pickle.loads(zlib.decompress(base64.b64decode(encoded)))


def encrypt_sumerian(text):
    """AES 암호화된 Base64를 수메르 문자로 변환 (Base64 패딩 유지)"""
    return "".join(sumerian_cipher_map.get(char, char) if char in sumerian_cipher_map else char for char in text)


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


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="비밀번호 암호화 및 복호화 도구 (AES-256 + CBC + 수메르어)")
    parser.add_argument("mode", nargs="?", choices=["encrypt", "decrypt", "test"], help="암호화 또는 복호화 모드")
    parser.add_argument("password", nargs="?", help="암호화/복호화할 비밀번호")
    parser.add_argument("--key", "-k", type=str, help="마스터 키")
    args = parser.parse_args()

    # 1. 모드 선택 (없으면 대화형)
    if not args.mode:
        args.mode = questionary.select("동작 모드를 선택하세요:", choices=["encrypt", "decrypt", "test"]).ask()

    # 2. 모드별 안내 메시지 분기, 하지만 입력은 항상 필수!
    if not args.password:
        password_label = {"encrypt": "암호화할 평문 비밀번호 입력:", "decrypt": "복호화할 암호문(암호화된 비밀번호) 입력:", "test": "테스트할 평문 비밀번호 입력:"}[args.mode]
        args.password = questionary.text(password_label, validate=lambda val: val.strip() != "" or "반드시 입력해야 합니다!").ask()

    # 3. 마스터 키 입력 (없으면 대화형, 가려서 입력)
    if not args.key:
        args.key = questionary.password("마스터 키 입력:").ask()

    # 예시 출력 (실전에서는 아래에 기존 로직 적용)
    print(f"선택된 모드: {args.mode}")
    print(f"입력한 비밀번호: {args.password}")
    print(f"입력한 키: {args.key}")

    if args.mode == "encrypt":
        encrypted = encrypt_password(args.password, args.key)
        print(f"암호화된 비밀번호: {encrypted}")
    elif args.mode == "decrypt":
        decrypted = decrypt_password(args.password, args.key)
        if decrypted:
            print(f"복호화된 비밀번호: {decrypted}")
        else:
            print("복호화 실패: 키가 잘못되었거나 암호화된 데이터가 손상되었습니다.")
    elif args.mode == "test":
        print("테스트 모드")
        encrypted = encrypt_password(args.password, args.key)
        print(f"암호화된 비밀번호: {encrypted}")
        # 테스트 목적으로 바로 복호화 검증
        print("\n암호화 검증:")
        decrypted = decrypt_password(encrypted, args.key)
        if decrypted == args.password:
            print(f"✅ 검증 성공: '{args.password}' → '{decrypted}'")
        else:
            print(f"❌ 검증 실패: '{args.password}' → '{decrypted}'")
    else:
        print("암호화 또는 복호화 모드를 지정해주세요.")
