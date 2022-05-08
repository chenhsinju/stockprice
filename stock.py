class Stock():
    # 個股包含以下屬性
    # 個股代號、名稱
    def __init__(self, code, name, is_tw):
        self.code = code
        self.name = name
        self.is_tw = is_tw
