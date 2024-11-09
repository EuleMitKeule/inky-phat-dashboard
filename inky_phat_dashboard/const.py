"""Constants for the inky_phat_dashboard package."""

from enum import Enum, StrEnum


class ColorInPalette(Enum):
    """Color in palette enumeration."""

    WHITE = 0
    ALERT = 1
    BLACK = 2


class Color(Enum):
    """Color enumeration."""

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)


class ColorMode(StrEnum):
    """Color mode enumeration."""

    LIGHT = "light"
    DARK = "dark"


class ColorPalette(StrEnum):
    """Color palette enumeration."""

    RED = ("red",)
    YELLOW = ("yellow",)


class VerticalAlign(Enum):
    TOP = "top"
    CENTER = "center"
    BOTTOM = "bottom"


ENV_CONFIG_FILE_PATH = "CONFIG_FILE_PATH"
ENV_LOG_FILE_PATH = "LOG_FILE_PATH"

DEFAULT_CONFIG_FILE_PATH = "config.yml"
DEFAULT_LOG_PATH = "inky_phat_dashboard.log"
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_FMT = "%(asctime)s %(levelname)s %(message)s"
DEFAULT_LOG_DATEFMT = "%Y-%m-%d %H:%M:%S"
DEFAULT_LOG_FILEMODE = "a"
DEFAULT_DATA_TIMEOUT_SECONDS = 10
DEFAULT_VIEW_CHANGE_SECONDS = 5
DEFAULT_FONT_PATH = "fonts/MinecraftRegular.otf"
DEFAULT_COLOR_MODE = ColorMode.LIGHT
DEFAULT_WASTE_ALERT_DAYS = 1
DEFAULT_WASTE_DETAILED_DAYS = 3
DEFAULT_ENABLE_INKY = True

RESTART_DELAY_SECONDS = 5

INKY_WIDTH = 250
INKY_HEIGHT = 122

IMAGE_BACKGROUND_PATH = "media/general/background.png"
IMAGE_BORDER_PATH = "media/general/border.png"

POSITION_ICON_LARGE = (16, 16)
POSITION_ICON_UPPER_LEFT = (16, 15)
POSITION_ICON_UPPER_RIGHT = (125, 15)
POSITION_ICON_LOWER_LEFT = (16, 65)
POSITION_ICON_LOWER_RIGHT = (125, 65)

RECTANGLE_TEXT_DETAILED_CENTER = (106, 16, 128, 90)
RECTANGLE_TEXT_DETAILED_UPPER = (106, 16, 128, 42)
RECTANGLE_TEXT_DETAILED_LOWER = (106, 64, 128, 42)
RECTANGLE_TEXT_DASHBOARD_UPPER_LEFT = (57, 15, 68, 42)
RECTANGLE_TEXT_DASHBOARD_UPPER_RIGHT = (167, 15, 68, 42)
RECTANGLE_TEXT_DASHBOARD_LOWER_LEFT = (57, 65, 68, 42)
RECTANGLE_TEXT_DASHBOARD_LOWER_RIGHT = (167, 65, 68, 42)

COLOR_PALETTE_TO_COLORS = {
    ColorPalette.RED: [
        Color.WHITE.value,
        Color.RED.value,
        Color.BLACK.value,
    ],
    ColorPalette.YELLOW: [
        Color.WHITE.value,
        Color.YELLOW.value,
        Color.BLACK.value,
    ],
}
