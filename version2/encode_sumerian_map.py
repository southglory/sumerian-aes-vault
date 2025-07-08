import json
import pickle, zlib, base64

# 수메르 매핑 파일 읽기
with open("./utils/sumerian_map.json", "r", encoding="utf-8") as f:
    sumerian_map = json.load(f)

# 직렬화(pickle), 압축(zlib), 인코딩(base64)
encoded = base64.b64encode(zlib.compress(pickle.dumps(sumerian_map)))
print(encoded.decode())  # 복사해서 코드에 붙이면 됨

# encoded를 텍스트에 생성
with open("./version2/sumerian_cipher_map.txt", "w", encoding="utf-8") as f:
    f.write(encoded.decode())


# 복원 함수
def load_mapping():
    return pickle.loads(zlib.decompress(base64.b64decode(encoded)))


if __name__ == "__main__":
    print(load_mapping())
