"""Caption fitting: font size and outline width. No wrapping or shrinking."""


def initial_font_size(image_height: int) -> int:
    return max(14, image_height // 10)


def stroke_width(font_size: int) -> int:
    return max(1, font_size // 15)
