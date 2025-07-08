# VERSION 2 (수메르어 AES 암호화)

## 개요

이 버전은 수메르어 유니코드 문자를 활용한 암호화/복호화 시스템입니다. AES-256(CBC) 암호화와 함께, 암호문을 수메르어 문자로 변환하여 가독성과 보안성을 높였습니다. 매핑 테이블은 pickle 직렬화, zlib 압축, base64 인코딩을 통해 관리합니다.

---

## 주요 파일 설명

- **make_sumerian_secret_map.py** :
  - 암호화에 사용할 문자(알파벳, 숫자, 특수문자 등)와 수메르어 유니코드 문자를 1:1로 랜덤 매핑하여 `sumerian_map.json`을 생성합니다.
- **encode_sumerian_map.py** :
  - `sumerian_map.json`을 pickle+zlib+base64로 인코딩하여 `sumerian_cipher_map.txt`로 저장합니다.
- **sumerian.py** :
  - AES-256(CBC)로 비밀번호를 암호화/복호화하고, 암호문을 수메르어 문자로 변환/복원합니다.
  - CLI(명령행)에서 암호화/복호화/테스트를 실행할 수 있습니다.

---

## 매핑 테이블 생성 및 인코딩

1. **수메르 매핑 생성**

```bash
python make_sumerian_secret_map.py
# → version2/sumerian_map.json 생성
```

2. **매핑 테이블 인코딩**

```bash
python encode_sumerian_map.py
# → version2/sumerian_cipher_map.txt 생성
```

---

## 암호화/복호화 사용법 (sumerian.py)

### 암호화

```bash
python sumerian.py encrypt <비밀번호> <마스터키>
# 예시:
python sumerian.py encrypt mySecret123 qwerty1234
```

### 복호화

```bash
python sumerian.py decrypt <암호화된_비밀번호> <마스터키>
# 예시:
python sumerian.py decrypt 𒁷𒇶𒍉... qwerty1234
```

### 테스트

```bash
python sumerian.py test <비밀번호> <마스터키>
# 암호화 후 바로 복호화 검증
```

### 인자 없이 실행 시 기본 테스트 동작

```bash
python sumerian.py
# 기본값(HelloWorld123, Qwerty1234)으로 암호화/복호화 테스트
```

---

## 매핑 파일 구조 예시

- **sumerian_map.json** : `{ "a": "𒊕", ... }` (문자→수메르어)
- **sumerian_cipher_map.txt** : base64로 인코딩된 바이너리 문자열 (직렬화+압축)

---

## 매핑 테이블 로딩 예시 (파이썬)

```python
import base64, zlib, pickle
with open("sumerian_cipher_map.txt", "r", encoding="utf-8") as f:
    encoded = f.read().encode()
sumerian_cipher_map = pickle.loads(zlib.decompress(base64.b64decode(encoded)))
```

---

## 참고/기타

- 수메르어 유니코드 블록(CUNEIFORM, U+12000~U+1247F) 내에서 실제 출력 가능한 문자만 사용합니다.
- 매핑 테이블을 새로 만들면 암호화/복호화 결과가 달라집니다. (매핑 불일치 시 복호화 불가)
- 암호화된 비밀번호는 수메르어 문자로만 구성되어 있습니다.

---

## 라이선스

MIT License
