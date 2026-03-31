import logging
from datetime import datetime
from homeassistant.helpers.entity import Entity
from homeassistant.components.weather import DOMAIN as WEATHER_DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Setup migraine risk sensor from config entry."""
    config = config_entry.data
    name = config.get("name", "Migraine Risk")
    forecast_source = config.get("forecast_source")
    pressure_sensor = config.get("pressure_sensor")
    async_add_entities([MigraineRiskSensor(hass, name, forecast_source, pressure_sensor)], True)


class MigraineRiskSensor(Entity):
    """Representation of the Migraine Risk sensor."""

    def __init__(self, hass, name, forecast_entity, pressure_entity):
        self.hass = hass
        self._name = name
        self._forecast_entity = forecast_entity
        self._pressure_entity = pressure_entity
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return "migraine_risk_sensor"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    async def async_update(self):
        """Fetch new state data for the sensor."""
        # Получаем текущее давление
        pressure = None
        if self._pressure_entity and self._pressure_entity in self.hass.states:
            pressure = self.hass.states.get(self._pressure_entity).state
        else:
            _LOGGER.warning("Pressure sensor %s not found", self._pressure_entity)

        # Получаем прогноз погоды (state + attributes)
        forecast_data = {}
        if self._forecast_entity and self._forecast_entity in self.hass.states:
            weather = self.hass.states.get(self._forecast_entity)
            forecast_data = weather.attributes.get("forecast", {})
        else:
            _LOGGER.warning("Forecast entity %s not found", self._forecast_entity)

        # Простейшая логика риска (можно заменить на более сложную)
        level = "low"
        if pressure is not None:
            try:
                p = float(pressure)
                if p < 980:
                    level = "high"
                elif p < 990:
                    level = "medium"
            except Exception as e:
                _LOGGER.error("Error parsing pressure: %s", e)

        self._state = level
        self._attributes = {
            "pressure": pressure,
            "forecast": forecast_data,
            "last_update": datetime.now().isoformat(),
        }
