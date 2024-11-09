"""Tests for the Inky pHat Dashboard."""

import pytest

from inky_phat_dashboard.models import Config, HomeAssistantConfig, SensorConfig


@pytest.fixture
def config():
    """Return a default config."""

    return Config(
        color_palette="red",
        home_assistant_config=HomeAssistantConfig(
            url="",
            token="",
            sensor_configs=[
                SensorConfig(
                    name="sensor1", friendly_name="Sensor 1", entity_id="sensor.sensor1"
                ),
            ],
        ),
    )
