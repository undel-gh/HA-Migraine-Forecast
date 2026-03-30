"""Migraine Risk integration."""
from homeassistant.helpers import entity_platform

DOMAIN = "migraine_risk"

async def async_setup(hass, config):
    """Set up the Migraine Risk integration."""
    return True

async def async_setup_entry(hass, entry):
    """Not used; we are YAML only."""
    return True
