"""Text platform for bing_wallpaper."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.text import (
    TextEntity,
    TextEntityDescription,
)

from .const import DOMAIN

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import BingWallpaperCoordinator


ENTITY_DESCRIPTIONS = (
    TextEntityDescription(
        key="description",
        translation_key="description",
        icon="mdi:image-text",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        BingWallpaperSensor(hass, entry, entity_description)
        for entity_description in ENTITY_DESCRIPTIONS
    )


class BingWallpaperSensor(TextEntity):
    """bing_wallpaper text class."""

    _attr_has_entity_name = True

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        description: TextEntityDescription,
    ) -> None:
        """Initialize the text class."""
        super().__init__()
        self.entity_description = description
        self._attr_native_value: str | None = None
        self.coordinator: BingWallpaperCoordinator = hass.data[DOMAIN][entry.entry_id]

        device = self.coordinator.device

        self.entity_id = f"sensor.{DOMAIN}_{description.key}_{device}"
        self._attr_unique_id = f"{DOMAIN}_{description.key}_{device}"

        # Set up device info
        self._attr_device_info = self.coordinator.device_info

        # Register update callback
        self.coordinator.register_callback(self.async_update_value)

    @property
    def device(self) -> str | None:
        """Return the device name."""
        return self.coordinator.device

    def _set_native_value(self) -> None:
        """Set the native value."""
        self._attr_native_value = self.coordinator.data.get("image_description")

    async def async_update_value(self) -> None:
        """Update the entity state."""
        self._set_native_value()
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """Run when entity about to be added to hass."""
        self._set_native_value()
