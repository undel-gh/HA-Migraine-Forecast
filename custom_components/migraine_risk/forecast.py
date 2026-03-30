from homeassistant.helpers.entity import Entity

class MigraineForecastSensor(Entity):

    def __init__(self, weather_entity):
        self.weather_entity = weather_entity

    @property
    def name(self):
        return "Migraine Risk Forecast"

    @property
    def state(self):
        weather = self.hass.states.get(self.weather_entity)
        if not weather:
            return 0

        temp = weather.attributes.get("temperature")
        uv = weather.attributes.get("uv_index", 0)

        score = 0

        if temp and (temp < 5 or temp > 30):
            score += 2

        if uv > 6:
            score += 2

        return score

    @property
    def extra_state_attributes(self):
        return {
            "risk_level": "Moderate",
            "uv_index": 5,
            "temp_min": 10,
            "temp_max": 20,
            "rain_chance": "30%"
        }
