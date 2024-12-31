"""Image generator for Inky pHat Dashboard."""

from PIL import Image

from inky_phat_dashboard.const import (
    IMAGE_BORDER_PATH,
    POSITION_ICON_LARGE,
    POSITION_ICON_LOWER_LEFT,
    POSITION_ICON_LOWER_RIGHT,
    POSITION_ICON_UPPER_LEFT,
    POSITION_ICON_UPPER_RIGHT,
    RECTANGLE_TEXT_DASHBOARD_LOWER_LEFT,
    RECTANGLE_TEXT_DASHBOARD_LOWER_RIGHT,
    RECTANGLE_TEXT_DASHBOARD_UPPER_LEFT,
    RECTANGLE_TEXT_DASHBOARD_UPPER_RIGHT,
    RECTANGLE_TEXT_DETAILED_CENTER,
    RECTANGLE_TEXT_DETAILED_LOWER,
    RECTANGLE_TEXT_DETAILED_UPPER,
    ColorMode,
    ColorPalette,
    VerticalAlign,
)
from inky_phat_dashboard.image_tools import ImageTools
from inky_phat_dashboard.models import (
    Config,
    DashboardViewData,
    DetailedViewData,
    DetailedViewTwoLinesData,
)


class ImageGenerator:
    """Generates images for the Inky pHat Dashboard."""

    def __init__(self, config: Config):
        """Initialize the image generator."""

        self._config = config
        self._palette = ImageTools.palette_from_color_palette(config.color_palette)

    @property
    def primary_color(self) -> tuple[int, int, int, int]:
        """Get the primary color."""

        return (
            (0, 0, 0, 255)
            if self._config.color_mode == ColorMode.LIGHT
            else (255, 255, 255, 255)
        )

    @property
    def secondary_color(self) -> tuple[int, int, int, int]:
        """Get the secondary color."""

        return (
            (255, 255, 255, 255)
            if self._config.color_mode == ColorMode.LIGHT
            else (0, 0, 0, 255)
        )

    @property
    def alert_color(self) -> tuple[int, int, int, int]:
        """Get the alert color."""

        return (
            (255, 0, 0, 255)
            if self._config.color_palette == ColorPalette.RED
            else (255, 255, 0, 255)
        )

    def generate_detailed_view(
        self, detailed_view_data: DetailedViewData
    ) -> Image.Image:
        """Generate an image for the detailed view."""

        result = ImageTools.create_background(self._config.color_mode)
        border = Image.open(IMAGE_BORDER_PATH).convert("RGBA")
        icon = Image.open(detailed_view_data.icon_path).convert("RGBA")

        border = ImageTools.recolor_non_transparent_pixels(
            border,
            self.alert_color
            if detailed_view_data.is_border_alert
            else self.primary_color,
        )

        icon = ImageTools.recolor_non_transparent_pixels(
            icon,
            self.alert_color
            if detailed_view_data.is_icon_alert
            else self.primary_color,
        )

        result = ImageTools.merge_images(result, border, (0, 0))
        result = ImageTools.merge_images(result, icon, POSITION_ICON_LARGE)

        result = ImageTools.place_text_in_rectangle(
            result,
            self._config.font_path,
            RECTANGLE_TEXT_DETAILED_CENTER,
            detailed_view_data.text,
            self.alert_color
            if detailed_view_data.is_text_alert
            else self.primary_color,
            vertical_align=VerticalAlign.CENTER,
        )

        result = result.convert("P", palette=self._palette, colors=256)

        if self._config.flip_screen:
            result = result.rotate(180)

        return result

    def generate_detailed_view_two_lines(
        self, detailed_view_two_lines_data: DetailedViewTwoLinesData
    ) -> Image.Image:
        """Generate an image for the detailed view with two lines."""

        result = ImageTools.create_background(self._config.color_mode)
        border = Image.open(IMAGE_BORDER_PATH).convert("RGBA")
        icon = Image.open(detailed_view_two_lines_data.icon_path).convert("RGBA")

        border = ImageTools.recolor_non_transparent_pixels(
            border,
            self.alert_color
            if detailed_view_two_lines_data.is_border_alert
            else self.primary_color,
        )

        icon = ImageTools.recolor_non_transparent_pixels(
            icon,
            self.alert_color
            if detailed_view_two_lines_data.is_icon_alert
            else self.primary_color,
        )

        result = ImageTools.merge_images(result, border, (0, 0))
        result = ImageTools.merge_images(result, icon, POSITION_ICON_LARGE)

        result = ImageTools.place_text_in_rectangle(
            result,
            self._config.font_path,
            RECTANGLE_TEXT_DETAILED_UPPER,
            detailed_view_two_lines_data.upper_text,
            self.alert_color
            if detailed_view_two_lines_data.is_upper_text_alert
            else self.primary_color,
            vertical_align=VerticalAlign.BOTTOM,
        )

        result = ImageTools.place_text_in_rectangle(
            result,
            self._config.font_path,
            RECTANGLE_TEXT_DETAILED_LOWER,
            detailed_view_two_lines_data.lower_text,
            self.alert_color
            if detailed_view_two_lines_data.is_lower_text_alert
            else self.primary_color,
            vertical_align=VerticalAlign.TOP,
        )

        result = result.convert("P", palette=self._palette, colors=256)

        if self._config.flip_screen:
            result = result.rotate(180)

        return result

    def generate_dashboard_view(
        self, dashboard_view_data: DashboardViewData
    ) -> Image.Image:
        """Generate an image for the dashboard view."""

        if len(dashboard_view_data.elements) > 4:
            raise ValueError("Too many dashboard elements")

        result = ImageTools.create_background(self._config.color_mode)
        border = Image.open(IMAGE_BORDER_PATH).convert("RGBA")

        border = ImageTools.recolor_non_transparent_pixels(
            border,
            self.alert_color
            if dashboard_view_data.is_border_alert
            else self.primary_color,
        )

        result = ImageTools.merge_images(result, border, (0, 0))

        positions = [
            POSITION_ICON_UPPER_LEFT,
            POSITION_ICON_UPPER_RIGHT,
            POSITION_ICON_LOWER_LEFT,
            POSITION_ICON_LOWER_RIGHT,
        ]

        rectangles = [
            RECTANGLE_TEXT_DASHBOARD_UPPER_LEFT,
            RECTANGLE_TEXT_DASHBOARD_UPPER_RIGHT,
            RECTANGLE_TEXT_DASHBOARD_LOWER_LEFT,
            RECTANGLE_TEXT_DASHBOARD_LOWER_RIGHT,
        ]

        for i, dashboard_element_data in enumerate(dashboard_view_data.elements):
            icon = Image.open(dashboard_element_data.icon_path).convert("RGBA")
            position = positions[i]
            rectangle = rectangles[i]

            icon = ImageTools.recolor_non_transparent_pixels(
                icon,
                self.alert_color
                if dashboard_element_data.is_icon_alert
                else self.primary_color,
            )

            result = ImageTools.merge_images(result, icon, position)
            result = ImageTools.place_text_in_rectangle(
                result,
                self._config.font_path,
                rectangle,
                dashboard_element_data.text,
                self.alert_color
                if dashboard_element_data.is_text_alert
                else self.primary_color,
                vertical_align=VerticalAlign.CENTER,
            )

        result = result.convert("P", palette=self._palette, colors=256)

        if self._config.flip_screen:
            result = result.rotate(180)

        return result
