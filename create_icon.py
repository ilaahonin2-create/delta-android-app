"""
Создать иконку для приложения Дельты
"""
from PIL import Image, ImageDraw, ImageFont

# Создаём иконку 512x512 (стандарт для Android)
size = 512
img = Image.new('RGB', (size, size), color='#8a2be2')  # Фиолетовый фон

# Рисуем круг
draw = ImageDraw.Draw(img)

# Внешний круг (светлее)
draw.ellipse([50, 50, 462, 462], fill='#9370db', outline='#ffffff', width=8)

# Внутренний круг (темнее)
draw.ellipse([100, 100, 412, 412], fill='#8a2be2')

# Рисуем букву Δ (Дельта)
try:
    # Пытаемся использовать системный шрифт
    font = ImageFont.truetype("arial.ttf", 280)
except:
    # Если не получилось - используем стандартный
    font = ImageFont.load_default()

# Текст Δ
text = "Δ"
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
text_x = (size - text_width) // 2
text_y = (size - text_height) // 2 - 20

draw.text((text_x, text_y), text, fill='#ffffff', font=font)

# Сохраняем
img.save('delta_icon.png')
print("✅ Иконка создана: delta_icon.png")
