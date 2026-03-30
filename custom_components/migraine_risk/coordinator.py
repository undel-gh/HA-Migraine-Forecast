from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant
from .const import UPDATE_INTERVAL

class MigraineCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, sensors: dict):
        super().__init__(
            hass,
            logger=None,
            name="migraine_risk",
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self.sensors = sensors
        self.history = []

    async def _async_update_data(self):
        data = {}

        for key, entity_id in self.sensors.items():
            state = self.hass.states.get(entity_id)
            if state:
                try:
                    data[key] = float(state.state)
                except:
                    data[key] = None

        return data
