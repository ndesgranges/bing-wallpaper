"""Data coordinator for bing_wallpaper."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import slugify

from .const import DOMAIN, LOGGER, MANUFACTURER, LangOption, ResolutionOption
from .data import request_wallpaper

if TYPE_CHECKING:
    from collections.abc import Callable
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
        self._update_callbacks = []

        LOGGER.debug("Coordinator init for %s", entry.title)
        # Set up device info
        name = entry.title[0].upper() + entry.title[1:]
        self.device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{DOMAIN}_{self.device}")},
            name=name,
            manufacturer=MANUFACTURER,
            model=DOMAIN,
        )

    def register_callback(self, callback: Callable) -> None:
        """Register a callback to be called when data is updated."""
        self._update_callbacks.append(callback)

    async def _async_update_data(self) -> dict[str, str]:
        """
        Get a new image from Bing Wallpaper.

        Calls TimothyYe/bing-wallpaper API
        See https://github.com/TimothyYe/bing-wallpaper
        """
        index = self.config_entry.data.get("index")
        mkt = self.config_entry.data.get("mkt")
        resolution = self.config_entry.data.get("resolution")

        if index is None or mkt is None or resolution is None:
            raise ValueError

        index = int(float(index)) if index != "random" else "random"
        mkt = LangOption(mkt)
        resolution = ResolutionOption(resolution)

        if index == "random":
            index = random.randint(0, 7)  # noqa: S311 - Not for security

        return await request_wallpaper(index, mkt, resolution)

    async def time_update_callback(self, _event: datetime | None = None) -> None:
        """Update Data from listener."""
        await self.async_refresh()
        for update in self._update_callbacks:
            await update()
