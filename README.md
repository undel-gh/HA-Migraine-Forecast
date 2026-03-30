# 🧠 Migraine Risk (HACS)

Advanced migraine risk prediction for Home Assistant.

## Features

- Pressure tracking (6h / 24h)
- Weather-based scoring
- Forecast support
- Beautiful Lovelace card

## Installation

### HACS

1. Add custom repository
2. Install "Migraine Risk"
3. Restart HA

### Manual

Copy `custom_components/migraine_risk` to `/config/custom_components/`

## Lovelace

```yaml
type: custom:migraine-risk-card
entity_risk_score: sensor.migraine_risk_score
entity_forecast: sensor.migraine_risk_forecast
