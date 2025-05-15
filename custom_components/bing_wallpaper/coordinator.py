"""Data coordinator for bing_wallpaper."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import slugify

from .const import DOMAIN, LOGGER, MANUFACTURER
from .data import request_wallpaper

if TYPE_CHECKING:
    from datetime import datetime

    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant


class BingWallpaperCoordinator(DataUpdateCoordinator[dict]):
    """Class to manage fetching Bing Wallpaper data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            LOGGER,
            name=DOMAIN,
        )
        self.device = slugify(entry.title)
        self.config_entry = entry

        LOGGER.debug("Coordinator init for %s", entry.title)
        # Set up device info
        name = entry.title[0].upper() + entry.title[1:]
        self.device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{DOMAIN}_{self.device}")},
            name=name,
            manufacturer=MANUFACTURER,
            model=DOMAIN,
        )

    async def _async_update_data(self) -> dict[str, str | None]:
        """
        Get a new image from Bing Wallpaper.

        Calls TimothyYe/bing-wallpaper API
        See https://github.com/TimothyYe/bing-wallpaper
        """
        request_wallpaper()
        return {
            "image_description": None,
            "image_url": None,
        }

    async def time_update_callback(self, _event: datetime | None = None) -> None:
        """Update Data from listener."""
        await self.async_refresh()
