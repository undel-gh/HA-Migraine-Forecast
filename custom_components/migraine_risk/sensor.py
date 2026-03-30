from homeassistant.helpers.entity import Entity
from .const import DOMAIN, MAX_SCORE, RISK_LEVELS
from .pressure import PressureTracker

def score_threshold(value, thresholds):
    score = 0
    for t, pts in thresholds:
        if abs(value) >= t:
            score = pts
    return score

class MigraineRiskSensor(Entity):
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._tracker = PressureTracker()

    @property
    def name(self):
        return "Migraine Risk Score"

    @property
    def state(self):
        data = self.coordinator.data

        pressure = data.get("pressure")
        humidity = data.get("humidity")
        temp = data.get("temperature")
        wind = data.get("wind")

        self._tracker.add(pressure)

        score = 0

        # pressure change
        score += score_threshold(self._tracker.change(6), [(4,1),(6,2),(10,3),(14,4)])

        if humidity:
            score += score_threshold(humidity, [(70,1),(80,2)])

        if temp:
            if temp < 5 or temp > 35:
                score += 2
            elif temp < 10 or temp > 30:
                score += 1

        if wind:
            score += score_threshold(wind, [(30,1),(50,2)])

        return score

    @property
    def extra_state_attributes(self):
        score = self.state
        pct = score / MAX_SCORE

        for threshold, label in RISK_LEVELS:
            if pct >= threshold:
                level = label
                break

        return {
            "risk_level": level,
            "max_score": MAX_SCORE,
        }
