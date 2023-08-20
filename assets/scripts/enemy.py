from assets.scripts.core_funcs import *
class Enemy:
    def __init__(self, type_, pos):
        self.pos = pos
        self.type = type_
        init_color = [92, 105, 159]
        