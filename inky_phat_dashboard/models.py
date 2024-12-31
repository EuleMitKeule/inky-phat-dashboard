"""Models for the Inky pHat Dashboard."""

import datetime
from abc import ABC
from dataclasses import dataclass, field
from pathlib import Path

import marshmallow_dataclass
import tzlocal
import yaml

from inky_phat_dashboard.const import (
    DEFAULT_COLOR_MODE,
    DEFAULT_DATA_TIMEOUT_SECONDS,
    DEFAULT_ENABLE_INKY,
    DEFAULT_FLIP_SCREEN,
    DEFAULT_FONT_PATH,
    DEFAULT_LOG_DATEFMT,
    DEFAULT_LOG_FILEMODE,
    DEFAULT_LOG_FMT,
    DEFAULT_LOG_LEVEL,
    DEFAULT_VIEW_CHANGE_SECONDS,
    DEFAULT_WASTE_ALERT_DAYS,
    DEFAULT_WASTE_DETAILED_DAYS,
    ColorMode,
    ColorPalette,
)


@dataclass
class ViewData(ABC):
    """Data for a view."""


@dataclass
class DashboardElementData:
    """Data for a dashboard element."""

    icon_path: str
    text: str
    is_icon_alert: bool = False
    is_text_alert: bool = False


@dataclass
class DashboardViewData(ViewData):
    """Data for the dashboard view."""

    elements: list[DashboardElementData]
    is_border_alert: bool = False


@dataclass
class DetailedViewData(ViewData):
    """Data for the detailed view."""

    icon_path: str
    text: str
    is_border_alert: bool = False
    is_icon_alert: bool = False
    is_text_alert: bool = False


@dataclass
class DetailedViewTwoLinesData(ViewData):
    """Data for the detailed view with two lines."""

    icon_path: str
    upper_text: str
    lower_text: str
    is_border_alert: bool = False
    is_icon_alert: bool = False
    is_upper_text_alert: bool = False
    is_lower_text_alert: bool = False


@dataclass
class StateInformation:
    """Information about the state of a sensor."""

    is_available: bool
    due_date: datetime.datetime | None = None

    @property
    def remaining_days(self) -> int | None:
        """Get the remaining days until the due date."""

        if not self.is_available:
            return None

        return (
            self.due_date.date() - datetime.datetime.now(tzlocal.get_localzone()).date()
        ).days


@dataclass
class LoggingConfig:
    """Configuration for logging."""

    path: str | None = None
    level: str = DEFAULT_LOG_LEVEL
    fmt: str = DEFAULT_LOG_FMT
    datefmt: str = DEFAULT_LOG_DATEFMT
    filemode: str = DEFAULT_LOG_FILEMODE


@dataclass
class SensorConfig:
    """Configuration for a sensor."""

    name: str
    friendly_name: str
    entity_id: str
    icon_path_small: str
    icon_path_large: str

    def __hash__(self):
        return hash(self.name)


@dataclass
class HomeAssistantConfig:
    """Configuration for Home Assistant."""

    url: str
    token: str
    sensor_configs: list[SensorConfig] = field(
        default_factory=list, metadata=dict(data_key="sensors")
    )


@dataclass
class Config:
    """Configuration for the Inky pHat Dashboard."""

    color_palette: ColorPalette
    home_assistant_config: HomeAssistantConfig = field(
        metadata=dict(data_key="home_assistant")
    )
    logging_config: LoggingConfig = field(
        default_factory=LoggingConfig, metadata=dict(data_key="logging")
    )
    data_timeout_seconds: int = DEFAULT_DATA_TIMEOUT_SECONDS
    view_change_interval_seconds: int = DEFAULT_VIEW_CHANGE_SECONDS
    timezone: str = field(default=tzlocal.get_localzone_name())
    font_path: str = DEFAULT_FONT_PATH
    color_mode: ColorMode = DEFAULT_COLOR_MODE
    waste_detailed_days: int = DEFAULT_WASTE_DETAILED_DAYS
    waste_alert_days: int = DEFAULT_WASTE_ALERT_DAYS
    enable_inky: bool = DEFAULT_ENABLE_INKY
    flip_screen: bool = DEFAULT_FLIP_SCREEN

    config_file_path: Path = field(init=False, repr=False, compare=False)

    @classmethod
    def load(cls, config_file_path: Path) -> "Config":
        """Load the configuration from a file."""

        if not config_file_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_file_path}")

        with config_file_path.open() as config_file:
            config_dict = yaml.load(config_file, Loader=yaml.FullLoader)

        config = marshmallow_dataclass.class_schema(cls)().load(config_dict)
        config.config_file_path = config_file_path

        return config
