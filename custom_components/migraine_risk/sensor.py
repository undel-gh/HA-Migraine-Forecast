"""Migraine Risk Sensor."""
from datetime import datetime
import random

from homeassistant.helpers.entity import Entity

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Migraine Risk sensor."""
    async_add_entities([MigraineRiskSensor()])

class MigraineRiskSensor(Entity):
    """Representation of a migraine risk sensor."""

    def __init__(self):
        self._name = "Migraine Risk"
        self._risk_score = 0
        self._risk_level = "Low"
        self._forecast = {}
        self._pressure = None
        self._last_update = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        """Return the main risk score (0-100)."""
        return self._risk_score

    @property
    def extra_state_attributes(self):
        """Return additional attributes for the card."""
        return {
            "level": self._risk_level,
            "forecast": self._forecast,
            "pressure": self._pressure,
            "last_update": self._last_update,
        }

    async def async_update(self):
        """Fetch new data (fake example; replace with real API)."""
        # Симулируем прогноз и давление
        self._pressure = round(random.uniform(980, 1030), 1)  # hPa
        self._risk_score = random.randint(0, 100)

        if self._risk_score < 30:
            self._risk_level = "Low"
        elif self._risk_score < 70:
            self._risk_level = "Medium"
        else:
            self._risk_level = "High"

        # Симулируем прогноз на день (например, давление, температура, активность)
        self._forecast = {
            "morning": {"pressure": self._pressure + random.randint(-5, 5)},
            "afternoon": {"pressure": self._pressure + random.randint(-5, 5)},
            "evening": {"pressure": self._pressure + random.randint(-5, 5)},
        }

        self._last_update = datetime.now().isoformat()
