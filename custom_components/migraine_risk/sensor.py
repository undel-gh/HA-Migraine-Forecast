import logging
from datetime import datetime, timedelta
import asyncio
import voluptuous as vol

from homeassistant.helpers.entity import Entity
from homeassistant.helpers import config_validation as cv
from homeassistant.const import CONF_NAME

_LOGGER = logging.getLogger(__name__)

DOMAIN = "migraine_risk"
DEFAULT_NAME = "Migraine Risk"

CONF_FORECAST_SOURCE = "forecast_source"
CONF_PRESSURE_SENSOR = "pressure_sensor"

PLATFORM_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Required(CONF_FORECAST_SOURCE): cv.entity_id,
        vol.Required(CONF_PRESSURE_SENSOR): cv.entity_id,
    }
)

LEVELS = ["low", "medium", "high"]

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Migraine Risk sensor."""
    name = config.get(CONF_NAME)
    forecast_source = config.get(CONF_FORECAST_SOURCE)
    pressure_sensor = config.get(CONF_PRESSURE_SENSOR)

    async_add_entities([MigraineRiskSensor(hass, name, forecast_source, pressure_sensor)], True)

class MigraineRiskSensor(Entity):
    """Representation of a Migraine Risk sensor."""

    def __init__(self, hass, name, forecast_source, pressure_sensor):
        self.hass = hass
        self._name = name
        self._forecast_source = forecast_source
        self._pressure_sensor = pressure_sensor
        self._state = None
        self._attributes = {}
        self._last_update = None

        # загрузка переводов из файла ru.json, если есть
        self._translations = {}
        try:
            translations = hass.config.path(f"custom_components/{DOMAIN}/translations/ru.json")
            import json
            with open(translations, "r", encoding="utf-8") as f:
                self._translations = json.load(f).get("state", {})
        except Exception:
            _LOGGER.warning("Translations not loaded, using default labels")

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    async def async_update(self):
        """Fetch new state data for the sensor."""

        # получение текущего давления
        pressure = self.hass.states.get(self._pressure_sensor)
        if pressure is None:
            _LOGGER.warning("Pressure sensor %s not found", self._pressure_sensor)
            return

        try:
            pressure_value = float(pressure.state)
        except ValueError:
            _LOGGER.warning("Pressure sensor value is not a number: %s", pressure.state)
            return

        # получение прогноза
        forecast = self.hass.states.get(self._forecast_source)
        if forecast is None:
            _LOGGER.warning("Forecast source %s not found", self._forecast_source)
            return

        forecast_data = {}
        try:
            forecast_data = forecast.attributes.get("forecast", {})
        except Exception:
            _LOGGER.warning("Forecast data not found")

        # простая логика риска: низкий/средний/высокий по давлению
        if pressure_value < 985:
            level_key = "high"
        elif pressure_value < 995:
            level_key = "medium"
        else:
            level_key = "low"

        # перевод уровня
        self._state = self._translations.get(level_key, level_key.capitalize())

        # формируем атрибуты
        self._attributes = {
            "forecast": forecast_data,
            "pressure": pressure_value,
            "last_update": datetime.now().isoformat(),
        }
