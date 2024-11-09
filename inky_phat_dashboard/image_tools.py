"""Image tools for the Inky pHat Dashboard."""

from abc import ABC

from PIL import Image, ImageDraw, ImageFont

from inky_phat_dashboard.const import (
    COLOR_PALETTE_TO_COLORS,
    INKY_HEIGHT,
    INKY_WIDTH,
    ColorMode,
    ColorPalette,
    VerticalAlign,
)


class ImageTools(ABC):
    """Image tools for the Inky pHat Dashboard."""

    @staticmethod
    def palette_from_color_palette(
        color_palette: ColorPalette,
    ) -> list[tuple[int, int, int, int]]:
        """Get the palette from the color palette."""

        colors = COLOR_PALETTE_TO_COLORS[color_palette]

        palette = [0] * 256 * 3

        for i, color in enumerate(colors):
            palette[i * 3 : i * 3 + 3] = color

        return palette

    @staticmethod
    def create_background(color_mode: ColorMode) -> Image.Image:
        """Create a background image."""

        return Image.new(
            "RGBA",
            (INKY_WIDTH, INKY_HEIGHT),
            (255, 255, 255, 255) if color_mode == ColorMode.LIGHT else (0, 0, 0, 255),
        )

    @staticmethod
    def recolor_non_transparent_pixels(
        image: Image.Image, new_color: tuple[int, int, int, int]
    ) -> Image.Image:
        """
        Changes all non-transparent pixels in an RGBA image to the specified color.

        Parameters:
        - image_path: Path to the input image
        - new_color: Tuple of RGBA values for the new color, e.g., (255, 255, 255, 255) for white

        Returns:
        - Image object with recolored non-transparent pixels
        """
        data = image.getdata()

        new_data: list[tuple[int, int, int, int]] = []
        for item in data:
            if item[3] != 0:
                new_data.append((new_color[0], new_color[1], new_color[2], item[3]))
            else:
                new_data.append(item)

        image.putdata(new_data)
        return image

    @staticmethod
    def merge_images(
        first: Image.Image, second: Image.Image, position: tuple[int, int]
    ) -> Image.Image:
        """Merge two images together."""

        first.paste(second, position, mask=second)
        return first

    @staticmethod
    def place_text_in_rectangle(
        image: Image.Image,
        font_path: str,
        rectangle: tuple[int, int, int, int],
        text: str,
        color: tuple[int, int, int, int],
        vertical_align: VerticalAlign,
    ):
        draw = ImageDraw.Draw(image)
        x, y, width, height = rectangle
        max_font_size = 100  # Start with a large font size

        # Try to find the maximum font size that fits within the rectangle
        font_size = max_font_size
        while font_size > 0:
            font = ImageFont.truetype(font_path, font_size)
            # Use textbbox to calculate the bounding box of the text
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            if text_width <= width and text_height <= height:
                break
            font_size -= 1

        # Calculate horizontal center alignment
        text_x = x + (width - text_width) // 2

        # Calculate vertical alignment with adjustment for precise centering
        if vertical_align == VerticalAlign.TOP:
            text_y = y
        elif vertical_align == VerticalAlign.CENTER:
            # Adjust to center within the rectangle
            text_y = y + (height - text_height) // 2 - text_bbox[1] // 2
        elif vertical_align == VerticalAlign.BOTTOM:
            text_y = y + height - text_height - text_bbox[1] // 2
        else:
            raise ValueError("Invalid vertical align mode")

        # Draw the text at the computed position
        draw.text((text_x, text_y), text, font=font, fill=color)

        return image
