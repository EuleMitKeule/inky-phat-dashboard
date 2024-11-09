"""Waste module for the Inky pHat Dashboard."""

import logging

import aiohttp

from inky_phat_dashboard.base_module import BaseModule
from inky_phat_dashboard.models import (
    Config,
    DashboardElementData,
    DashboardViewData,
    DetailedViewTwoLinesData,
    SensorConfig,
    StateInformation,
    ViewData,
)
from inky_phat_dashboard.parser import RemainingDaysParser


class WasteModule(BaseModule):
    """Waste module for the Inky pHat Dashboard."""

    def __init__(self, config: Config):
        """Initialize the waste module."""

        self._config = config
        self._parser = RemainingDaysParser()
        self._is_running: bool = False
        self._latest_states: dict[SensorConfig, StateInformation | None] = {
            sensor_config: None
            for sensor_config in self._config.home_assistant_config.sensor_configs
        }

    async def update(self):
        """Update the waste module."""

        async with aiohttp.ClientSession() as session:
            sensor_configs = list(self._latest_states.keys())

            for sensor_config in sensor_configs:
                state = await self._get_sensor_state(session, sensor_config)
                self._latest_states[sensor_config] = self._parser.parse_state(state)

    async def get_view_datas(self):
        """Get the view datas for the waste module."""

        view_datas: list[ViewData] = []

        available_sensors = [
            (sensor_config, state_information)
            for sensor_config, state_information in self._latest_states.items()
            if state_information is not None and state_information.is_available
        ]

        unavailable_sensors = [
            (sensor_config, state_information)
            for sensor_config, state_information in self._latest_states.items()
            if state_information is not None and not state_information.is_available
        ]

        if not available_sensors:
            logging.warning("No sensors available")

        if not available_sensors and not unavailable_sensors:
            return view_datas

        for sensor_config, state_information in unavailable_sensors:
            logging.warning(f"Sensor {sensor_config.name} is unavailable")

        for sensor_config, state_information in available_sensors:
            logging.info(
                f"{sensor_config.friendly_name} is due on {state_information.due_date.date()}"
            )

        dashboard_view_data = DashboardViewData(
            elements=[
                DashboardElementData(
                    icon_path=sensor_config.icon_path_small,
                    text=self._text_from_remaining_days(
                        state_information.remaining_days
                    )
                    if state_information.is_available
                    else "Nicht verfügbar",
                    is_icon_alert=not state_information.is_available
                    or state_information.remaining_days
                    <= self._config.waste_alert_days,
                    is_text_alert=not state_information.is_available
                    or state_information.remaining_days
                    <= self._config.waste_alert_days,
                )
                for sensor_config, state_information in self._latest_states.items()
            ],
            is_border_alert=any(
                not state_information.is_available
                for state_information in self._latest_states.values()
            )
            or any(
                state_information.remaining_days <= self._config.waste_alert_days
                for state_information in self._latest_states.values()
            ),
        )

        view_datas.append(dashboard_view_data)

        for sensor_config, state_information in available_sensors:
            if state_information.remaining_days > self._config.waste_detailed_days:
                continue

            detailed_view_data = DetailedViewTwoLinesData(
                icon_path=sensor_config.icon_path_large,
                upper_text=sensor_config.friendly_name,
                lower_text=self._text_from_remaining_days(
                    state_information.remaining_days
                ),
                is_icon_alert=state_information.remaining_days
                <= self._config.waste_alert_days,
            )

            view_datas.append(detailed_view_data)

        return view_datas

    def _text_from_remaining_days(self, remaining_days: int) -> str:
        """Get the text from the remaining days."""

        if remaining_days == 0:
            return "Heute"

        if remaining_days == 1:
            return "Morgen"

        return f"{remaining_days} Tage"

    async def _get_sensor_state(
        self, session: aiohttp.ClientSession, sensor_config: SensorConfig
    ) -> str:
        """Get the state of a sensor entity."""

        logging.debug(f"Getting state for sensor {sensor_config.name}...")

        async with session.get(
            f"{self._config.home_assistant_config.url}/api/states/{sensor_config.entity_id}",
            headers={
                "Authorization": f"Bearer {self._config.home_assistant_config.token}",
                "content-type": "application/json",
            },
        ) as response:
            response.raise_for_status()

            logging.debug(f"Response: {response.status} {response.reason}")

            response_json = await response.json()
            state = response_json["state"]

            if not isinstance(state, str):
                raise ValueError(f"Invalid state: {state}")

            logging.debug(f"State: {state}")

            return state
