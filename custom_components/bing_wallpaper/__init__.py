"""
Custom integration to integrate bing_wallpaper with Home Assistant.

For more details about this integration, please refer to
https://github.com/ndesgranges/bing-wallpaper
"""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntryState
from homeassistant.helpers.config_validation import config_entry_only_config_schema
from homeassistant.helpers.device_registry import (
    EVENT_DEVICE_REGISTRY_UPDATED,
    EventDeviceRegistryUpdatedData,
    async_entries_for_config_entry,
    async_get,
)
from homeassistant.helpers.event import (
    async_track_time_interval,
)

from .const import DOMAIN, LOGGER, PLATFORMS
from .coordinator import BingWallpaperCoordinator

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import Event, HomeAssistant
    from homeassistant.helpers.typing import ConfigType


CONFIG_SCHEMA = config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, _config: ConfigType) -> bool:
    """Set up the Bing Wallpaper component."""
    hass.data.setdefault(DOMAIN, {})

    # Register listener at integration level instead of per-entry
    async def handle_device_registry_update(
        event: Event[EventDeviceRegistryUpdatedData],
    ) -> None:
        """Handle device registry updates."""
        changes = event.data.get("changes")
        if (
            not changes
            or not isinstance(changes, dict)
            or "name_by_user" not in changes
        ):
            return

        device_registry = async_get(hass)
        device = device_registry.async_get(event.data.get("device_id"))
        if not device:
            return

        # Process entries related to this device
        for entry_id in device.config_entries:
            entry = hass.config_entries.async_get_entry(entry_id)
            if not entry or entry.domain != DOMAIN:
                continue

            device_name_from_entry_title = entry.title[0].upper() + entry.title[1:]
            if (
                device_name_from_entry_title == device.name_by_user
                or device.name_by_user is None
            ):
                continue

            LOGGER.debug(
                "Renaming entry %s to %s",
                entry.title,
                device.name_by_user,
            )
            data = dict(entry.data)
            data.update(
                {
                    "name": device.name_by_user,
                    "name_by_user": device.name_by_user,
                }
            )

            hass.config_entries.async_update_entry(
                entry, data=data, title=device.name_by_user
            )

            device_registry.async_remove_device(device.id)

            hass.config_entries.async_schedule_reload(entry.entry_id)

    # Register the listener once for the whole integration
    hass.bus.async_listen(
        EVENT_DEVICE_REGISTRY_UPDATED,
        handle_device_registry_update,
    )

    return True


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    LOGGER.debug("Setting up entry %s", entry.title)
    coordinator = BingWallpaperCoordinator(hass, entry)

    if entry.state == ConfigEntryState.SETUP_IN_PROGRESS:
        await coordinator.async_config_entry_first_refresh()
    else:
        await coordinator.async_request_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    refresh_rate = entry.data.get("refresh_rate")

    if refresh_rate is None:
        LOGGER.error(
            "entry %s : wrong value for refresh_rate (%s)", entry.title, refresh_rate
        )
        raise ValueError
    interval = timedelta(minutes=float(refresh_rate))

    entry.async_on_unload(
        async_track_time_interval(
            hass, coordinator.time_update_callback, interval, cancel_on_shutdown=True
        )
    )

    entry.async_on_unload(entry.add_update_listener(async_reload_on_rename))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle unloading of an entry."""
    # Unload platforms
    LOGGER.debug("Unloading %s", entry.title)
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    LOGGER.debug("Unloading status : %s", "OK" if unload_ok else "NOK")

    # Remove entry data
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_reload_on_rename(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> None:
    """Reload config entry."""
    if entry.title == entry.data.get("name"):
        return
    LOGGER.info("Changing name of %s to %s", entry.data.get("name"), entry.title)
    # Update entry
    data = dict(entry.data)
    data.update({"name": entry.title, "name_by_user": entry.title})
    hass.config_entries.async_update_entry(entry, data=data)
    # remove obsolete device
    device_name = entry.title[0].upper() + entry.title[1:]
    device_registry = async_get(hass)
    for device in async_entries_for_config_entry(device_registry, entry.entry_id):
        if device.name != device_name:
            device_registry.async_remove_device(device.id)
    hass.config_entries.async_schedule_reload(entry.entry_id)
