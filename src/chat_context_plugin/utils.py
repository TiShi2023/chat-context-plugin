def get_color(name: str) -> str:
    # 根据名称生成颜色代码,确保同一名称总是生成相同的颜色
    hash_code = abs(hash(name))  # 获取名称的哈希值并取绝对值
    r = (hash_code & 0xFF0000) >> 16
    g = (hash_code & 0x00FF00) >> 8
    b = hash_code & 0x0000FF
    return f'#{r:02x}{g:02x}{b:02x}'

