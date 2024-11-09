"""Base module for Inky pHAT Dashboard."""

from abc import ABC, abstractmethod

from inky_phat_dashboard.models import ViewData


class BaseModule(ABC):
    """Base module for Inky pHAT Dashboard."""

    @abstractmethod
    async def update(self) -> None:
        """Update the module."""

    @abstractmethod
    async def get_view_datas(self) -> list[ViewData]:
        """Get the view datas for the module."""
