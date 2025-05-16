"""Image platform for bing_wallpaper."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.image import (
    ImageEntity,
    ImageEntityDescription,
)
from homeassistant.util.dt import as_local, utcnow

from .const import DOMAIN, LOGGER

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
    from homeassistant.helpers.typing import UndefinedType

    from .coordinator import BingWallpaperCoordinator


ENTITY_DESCRIPTIONS = (
    ImageEntityDescription(
        key="picture",
        translation_key="picture",
        icon="mdi:image",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the image platform."""
    async_add_entities(
        BingWallpaperImage(hass, entry, entity_description)
        for entity_description in ENTITY_DESCRIPTIONS
    )


class BingWallpaperImage(ImageEntity):
    """bing_wallpaper image class."""

    _attr_has_entity_name = True

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        description: ImageEntityDescription,
    ) -> None:
        """Initialize the image class."""
        super().__init__(hass)
        self.entity_description = description

        self.coordinator: BingWallpaperCoordinator = hass.data[DOMAIN][entry.entry_id]

        device = self.coordinator.device

        self.entity_id = f"image.{DOMAIN}_{description.key}_{device}"
        self._attr_unique_id = f"{DOMAIN}_{description.key}_{device}"

        # Set up device info
        self._attr_device_info = self.coordinator.device_info

        # Register update callback
        self.coordinator.register_callback(self.async_update_value)

    @property
    def device(self) -> str | None:
        """Return the device name."""
        return self.coordinator.device

    @property
    def image_url(self) -> str | None | UndefinedType:
        """Return URL of image."""
        return self._attr_image_url

    def _set_native_value(self) -> None:
        """Set the native value."""
        now = as_local(utcnow())
        self._attr_image_url = self.coordinator.data.get("image_url")
        self._attr_image_last_updated = now
        self._cached_image = None

    async def async_update_value(self) -> None:
        """Update image URL."""
        self._set_native_value()
        self.async_write_ha_state()
        LOGGER.debug("url : %s", self._attr_image_url)

    async def async_added_to_hass(self) -> None:
        """Run when entity about to be added to hass."""
        self._set_native_value()
