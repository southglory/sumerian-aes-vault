# VERSION 2 (Sumerian AES Encryption)

## Overview

This version implements an encryption/decryption system using Sumerian Unicode characters. It combines AES-256 (CBC) encryption with a mapping that converts ciphertext into Sumerian characters for enhanced readability and security. The mapping table is managed using pickle serialization, zlib compression, and base64 encoding.

---

## Main Files

- **make_sumerian_secret_map.py** :
  - Generates a random 1:1 mapping between characters (alphabets, numbers, special symbols, etc.) and Sumerian Unicode characters, and saves it as `sumerian_map.json`.
- **encode_sumerian_map.py** :
  - Encodes `sumerian_map.json` using pickle+zlib+base64 and saves it as `sumerian_cipher_map.txt`.
- **sumerian.py** :
  - Encrypts/decrypts passwords using AES-256 (CBC), and converts ciphertext to/from Sumerian characters.
  - Provides a CLI for encryption, decryption, and testing.

---

## Generating and Encoding the Mapping Table

1. **Generate Sumerian Mapping**

```bash
python make_sumerian_secret_map.py
# → Creates version2/sumerian_map.json
```

2. **Encode the Mapping Table**

```bash
python encode_sumerian_map.py
# → Creates version2/sumerian_cipher_map.txt
```

---

## How to Use Encryption/Decryption (sumerian.py)

### Encryption

```bash
python sumerian.py encrypt <password> <master_key>
# Example:
python sumerian.py encrypt mySecret123 qwerty1234
```

### Decryption

```bash
python sumerian.py decrypt <encrypted_password> <master_key>
# Example:
python sumerian.py decrypt 𒁷𒇶𒍉... qwerty1234
```

### Test

```bash
python sumerian.py test <password> <master_key>
# Encrypts and immediately verifies decryption
```

### Run without arguments for default test

```bash
python sumerian.py
# Runs encryption/decryption test with default values (HelloWorld123, Qwerty1234)
```

---

## Example Structure of Mapping Files

- **sumerian_map.json** : `{ "a": "𒊕", ... }` (character → Sumerian)
- **sumerian_cipher_map.txt** : Base64-encoded binary string (serialized + compressed)

---

## Example: Loading the Mapping Table in Python

```python
import base64, zlib, pickle
with open("sumerian_cipher_map.txt", "r", encoding="utf-8") as f:
    encoded = f.read().encode()
sumerian_cipher_map = pickle.loads(zlib.decompress(base64.b64decode(encoded)))
```

---

## Notes

- Only printable Sumerian Unicode block characters (CUNEIFORM, U+12000~U+1247F) are used.
- If you regenerate the mapping table, encryption/decryption results will change. (Decryption will fail if the mapping does not match)
- Encrypted passwords consist only of Sumerian characters.

---

## License

MIT License
