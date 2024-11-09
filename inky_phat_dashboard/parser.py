"""Parser for sensor states."""

import datetime
from abc import ABC, abstractmethod

import tzlocal

from inky_phat_dashboard.models import StateInformation


class Parser(ABC):
    """Parser for sensor states."""

    @abstractmethod
    def parse_state(self, state: str) -> StateInformation:
        """Parse the state information from the sensor state."""


class RemainingDaysParser(Parser):
    """Parses states in the format 'In x Tag(en)'."""

    def parse_state(self, state: str) -> StateInformation:
        """Parse the state information from the sensor state."""

        try:
            remaining_days = int(state.split(" ")[1])
            datetime_now = datetime.datetime.now(tzlocal.get_localzone())
            due_date = datetime_now + datetime.timedelta(days=remaining_days)

            return StateInformation(is_available=True, due_date=due_date)
        except (IndexError, ValueError):
            return StateInformation(is_available=False)
