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

    return ImageTk.PhotoImage(img), text  # 이미지와 원본 텍스트 반환


def update_canvas():
    """Canvas에 수메르어 텍스트 이미지 업데이트"""
    img, text = render_sumerian_text()
    canvas.create_image(0, 0, anchor="nw", image=img)
    canvas.image = img  # 이미지 참조 유지 (안 하면 사라짐)

    # 텍스트 위젯에 원본 텍스트 추가 (복사 가능)
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, text)
    output_text.config(state=tk.DISABLED)


root = tk.Tk()
root.title("AES-256 + 수메르어 변환 암호화 도구")
root.geometry("400x300")

canvas = tk.Canvas(root, width=400, height=100)
canvas.pack()

# 복사 가능하게 텍스트 위젯 추가
output_text = tk.Text(root, height=4, width=50)
output_text.pack()

update_canvas()

root.mainloop()
