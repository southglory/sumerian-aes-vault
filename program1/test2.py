import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont


def render_sumerian_text():
    """Pillow로 수메르어 문자를 이미지로 렌더링"""
    img = Image.new("RGB", (400, 100), "white")
    draw = ImageDraw.Draw(img)

    font_path = "C:/Windows/Fonts/seguihis.ttf"  # Segoe UI Historic 폰트 경로

    try:
        font = ImageFont.truetype(font_path, 40)
        print("✅ Segoe UI Historic 폰트 로드 성공!")
    except IOError:
        print("❌ 폰트 로드 실패! 기본 폰트 사용")
        font = ImageFont.load_default()

    text = "𒀀𒁀𒍝𒁕𒂊𒆠"
    draw.text((10, 10), text, font=font, fill="black")

    return ImageTk.PhotoImage(img)


def update_canvas():
    """Canvas에 수메르어 텍스트 이미지 업데이트"""
    img = render_sumerian_text()
    canvas.create_image(0, 0, anchor="nw", image=img)
    canvas.image = img  # 이미지 참조 유지 (안 하면 사라짐)


root = tk.Tk()
root.title("AES-256 + 수메르어 변환 암호화 도구")
root.geometry("400x200")

canvas = tk.Canvas(root, width=400, height=100)
canvas.pack()

update_canvas()

root.mainloop()
