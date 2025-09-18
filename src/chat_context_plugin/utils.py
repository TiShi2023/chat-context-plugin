def get_color(name: str) -> tuple[str, str]:
    # 根据名称生成背景颜色代码和字体颜色代码,确保同一名称总是生成相同的颜色。确保两种颜色对比强烈
    hash_code = abs(hash(name))  # 获取名称的哈希值并取绝对值
    r = (hash_code & 0xFF0000) >> 16
    g = (hash_code & 0x00FF00) >> 8
    b = hash_code & 0x0000FF
    back_color = f'#{r:02x}{g:02x}{b:02x}'
    font_color = '#000000' if (r * 0.299 + g * 0.587 + b * 0.114) > 186 else '#FFFFFF'
    return back_color, font_color
