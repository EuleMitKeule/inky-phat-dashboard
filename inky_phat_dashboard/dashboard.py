"""Inky pHat Dashboard Module."""

import asyncio
import logging
from typing import Callable

from inky import auto
from PIL import Image

from inky_phat_dashboard.const import RESTART_DELAY_SECONDS
from inky_phat_dashboard.image_generator import ImageGenerator
from inky_phat_dashboard.models import (
    Config,
    DashboardViewData,
    DetailedViewData,
    DetailedViewTwoLinesData,
    ViewData,
)
from inky_phat_dashboard.waste_module import WasteModule


class Dashboard:
    """Inky pHat Dashboard."""

    def __init__(self, config: Config):
        """Initialize the Inky pHat Dashboard."""

        self._config = config
        self._image_generator = ImageGenerator(config)
        self._modules = [
            WasteModule(config),
        ]
        self._data_collection_task: asyncio.Task | None = None
        self._display_refresh_task: asyncio.Task | None = None
        self._last_view_data: ViewData | None = None
        self._inky_display = auto() if config.enable_inky else None

    async def start(self):
        """Start the Inky pHat Dashboard."""

        self._is_running = True

        for module in self._modules:
            logging.debug(f"Updating module {module}...")
            await module.update()

        self._data_collection_task = asyncio.create_task(
            self._run_with_restart(self._handle_data_collection)
        )
        self._display_refresh_task = asyncio.create_task(
            self._run_with_restart(self._handle_display_refresh)
        )

        await asyncio.gather(self._data_collection_task, self._display_refresh_task)

    async def _handle_data_collection(self):
        """Start data collection."""

        while self._is_running:
            for module in self._modules:
                logging.debug(f"Updating module {module}...")
                await module.update()
            await asyncio.sleep(self._config.data_timeout_seconds)

    async def _handle_display_refresh(self):
        """Start the display."""

        while self._is_running:
            logging.debug("Refreshing display...")
            await self._refresh_display()
            await asyncio.sleep(self._config.view_change_interval_seconds)

    async def _refresh_display(self):
        """Update the display."""

        view_datas: list[ViewData] = []

        for module in self._modules:
            module_view_datas = await module.get_view_datas()
            view_datas.extend(module_view_datas)

        if not view_datas:
            logging.warning("No view data available")
            return

        selected_view_data = (
            view_datas[(view_datas.index(self._last_view_data) + 1) % len(view_datas)]
            if self._last_view_data
            else view_datas[0]
        )

        image: Image.Image
        match selected_view_data:
            case DashboardViewData():
                image = self._image_generator.generate_dashboard_view(
                    selected_view_data
                )
            case DetailedViewData():
                image = self._image_generator.generate_detailed_view(selected_view_data)
            case DetailedViewTwoLinesData():
                image = self._image_generator.generate_detailed_view_two_lines(
                    selected_view_data
                )

        if self._config.enable_inky:
            self._inky_display.set_image(image)
        else:
            image.show()

        self._last_view_data = selected_view_data

    async def _run_with_restart(self, func: Callable, *args, **kwargs):
        """Run a task and restart it on exception."""

        while self._is_running:
            try:
                await func(*args, **kwargs)
            except Exception as ex:
                self._handle_exception(ex)
                await asyncio.sleep(RESTART_DELAY_SECONDS)
                logging.debug(f"Restarting task {func.__name__} after exception...")

    async def _handle_exception_in_func(self, func: Callable, *args, **kwargs):
        try:
            await func(*args, **kwargs)
        except Exception as ex:
            self._handle_exception(ex)

    def _handle_exception(self, exception: Exception):
        """Handle an exception in the event loop."""

        match exception:
            case Exception():
                logging.exception(exception)
