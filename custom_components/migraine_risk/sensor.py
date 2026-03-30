"""Migraine Risk sensor."""
from datetime import datetime
from homeassistant.helpers.entity import Entity

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensor."""
    async_add_entities([MigraineRiskSensor()])


class MigraineRiskSensor(Entity):
    """Representation of the migraine risk sensor."""

    def __init__(self):
        self._data = {
            "score": 0,
            "level": "Low",
            "pressure": None,
            "forecast": {},
            "last_update": None,
        }

    @property
    def name(self):
        return "Migraine Risk"

    @property
    def state(self):
        """Return the state (score)."""
        return self._data["score"]

    @property
    def extra_state_attributes(self):
        """Return extra attributes."""
        return {
            self.hass.localize("component.migraine_risk.attributes.level"): self._data["level"],
            self.hass.localize("component.migraine_risk.attributes.pressure"): self._data["pressure"],
            self.hass.localize("component.migraine_risk.attributes.last_update"): self._data["last_update"],
            self.hass.localize("component.migraine_risk.attributes.forecast"): self._data["forecast"],
        }

    async def async_update(self):
        """Fetch new data."""
        # TODO: Реальная логика, сейчас dummy
        import random
        self._data["score"] = random.randint(0, 22)

        # map score → level
        if self._data["score"] >= 12:
            self._data["level"] = self.hass.localize("component.migraine_risk.state.high")
        elif self._data["score"] >= 8:
            self._data["level"] = self.hass.localize("component.migraine_risk.state.medium")
        else:
            self._data["level"] = self.hass.localize("component.migraine_risk.state.low")

        self._data["pressure"] = round(random.uniform(980, 1030), 1)
        self._data["last_update"] = datetime.now().isoformat()

        # Forecast dummy
        self._data["forecast"] = {
            self.hass.localize("component.migraine_risk.attributes.morning"):
                {"pressure": self._data["pressure"] + random.randint(-5, 5)},
            self.hass.localize("component.migraine_risk.attributes.afternoon"):
                {"pressure": self._data["pressure"] + random.randint(-5, 5)},
            self.hass.localize("component.migraine_risk.attributes.evening"):
                {"pressure": self._data["pressure"] + random.randint(-5, 5)},
        }
