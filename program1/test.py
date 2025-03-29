from PIL import Image, ImageDraw, ImageFont

# Windows에서 Segoe UI Historic 폰트 경로 (메모장에서 자동 사용된 폰트)
font_path = "C:/Windows/Fonts/seguihis.ttf"

# 이미지 크기 설정
img = Image.new("RGB", (400, 100), "white")
draw = ImageDraw.Draw(img)

try:
    font = ImageFont.truetype(font_path, 40)
    print("✅ Segoe UI Historic 폰트 로드 성공!")
except IOError:
    print("❌ 폰트 로드 실패! 기본 폰트 사용")
    font = ImageFont.load_default()

# 수메르어 텍스트
text = "𒀀𒁀𒍝𒁕𒂊𒆠"

# 이미지에 텍스트 그리기
draw.text((10, 10), text, font=font, fill="black")

# 이미지 저장 및 보기
img.show()
img.save("sumerian_text.png")
