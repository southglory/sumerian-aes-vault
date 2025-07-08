import json
import random
import string
import unicodedata

print(string.ascii_uppercase)  # ABCDEFGHIJKLMNOPQRSTUVWXYZ
print(string.ascii_lowercase)  # abcdefghijklmnopqrstuvwxyz
print(string.digits)  # 0123456789
print(string.punctuation)  # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
print(string.whitespace)  # \t\n\r\x0c\x0b\x0a\x0d\x09\x0b\x0c
print(string.printable)  # 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~


# 모든 후보 문자를 한 번에 모으기
all_chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation + string.whitespace + string.printable

# 순서를 유지하면서 중복 제거
unique_chars = []
seen = set()
for ch in all_chars:
    if ch not in seen:
        unique_chars.append(ch)
        seen.add(ch)

print("Total characters:", len(unique_chars))
print(unique_chars)


def is_printable_sumerian(ch):
    try:
        name = unicodedata.name(ch)
        # 수메르 유니코드 블록이면서 실제 이름이 있다면 OK
        return "CUNEIFORM" in name
    except ValueError:
        # 이름이 없는 문자는 대개 출력 불가/미지원
        return False


# 매핑에 쓸 정상적인 수메르 문자만 추출
sumerian_chars = [chr(cp) for cp in range(0x12000, 0x12400) if is_printable_sumerian(chr(cp))]
print("Sumerian characters:", len(sumerian_chars))

# 문자 개수와 수메르 문자 개수 확인
print("문자 개수:", len(unique_chars))
print("수메르 문자 개수:", len(sumerian_chars))

# 수메르 문자가 더 많을 때만 매핑!
assert len(unique_chars) <= len(sumerian_chars), "수메르 문자가 부족합니다!"

# 랜덤 셔플
random.shuffle(sumerian_chars)

# 1:1 매핑
mapping = dict(zip(unique_chars, sumerian_chars))

# 예시 출력
print(mapping)

# 매핑 파일 json으로 저장
with open("./utils/sumerian_map.json", "w", encoding="utf-8") as f:
    json.dump(mapping, f, ensure_ascii=False, indent=4)
