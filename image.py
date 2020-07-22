from color import Color

class Image:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.pixels = [[Color().raw() for _ in range(width)] for _ in range(height)]

    def set_pixel(self, x: int, y: int, color: list):
        self.pixels[y][x] = color

    def get_pixels(self) -> list:
        return self.pixels