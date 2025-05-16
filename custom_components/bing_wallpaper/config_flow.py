"""Adds config flow for Bing Wallpaper."""

from __future__ import annotations

import voluptuous as vol
from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.const import UnitOfTime
from homeassistant.core import callback
from homeassistant.helpers import selector
from homeassistant.util import slugify

from .const import DOMAIN, LANG_OPTIONS, LOGGER, RESOLUTION_OPTIONS

## CONFIG FLOW SCHEMAS


def user_form(suggested: dict | None = None, *, edit: bool = False) -> vol.Schema:
    """Return a new device form."""
    LOGGER.debug("config_flow, 1st call : displaying form")
    LOGGER.debug("edit = %d", edit)
    if suggested is None:
        suggested = {
            "name": None,
            "refresh_rate": None,
            "index": None,
            "mkt": None,
            "resolution": None,
        }

    LOGGER.debug(suggested)

    schema = vol.Schema({})
    if not edit:
        schema = vol.Schema(
            {
                vol.Optional(
                    "name", default="Bing Wallpaper", description=suggested["name"]
                ): selector.TextSelector(
                    selector.TextSelectorConfig(multiline=False, multiple=False)
                ),
            }
        )

    return schema.extend(
        {
            vol.Optional(
                "refresh_rate",
                default=1,
                description={"suggested_value": suggested["refresh_rate"]},
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=1,
                    mode=selector.NumberSelectorMode.BOX,
                    unit_of_measurement=UnitOfTime.MINUTES,
                ),
            ),
            vol.Optional(
                "index",
                default="random",
                description={"suggested_value": suggested["index"]},
            ): selector.TextSelector(
                selector.TextSelectorConfig(
                    multiline=False,
                ),
            ),
            vol.Optional(
                "mkt",
                default="en-US",
                description={"suggested_value": suggested["mkt"]},
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    {
                        "options": LANG_OPTIONS,
                        "custom_value": False,
                        "sort": True,
                    }
                )
            ),
            vol.Optional(
                "resolution",
                default="UHD",
                description={"suggested_value": suggested["resolution"]},
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    {
                        "options": RESOLUTION_OPTIONS,
                        "custom_value": False,
                        "sort": False,
                    }
                )
            ),
        }
    )


## CONFIG FLOWS


class BingWallpaperFlowHandler(ConfigFlow, domain=DOMAIN):
    """Config flow for Bing Wallpaper."""

    def __init__(self) -> None:
        """Init."""
        self._user_inputs: dict = {}

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Get options flow for this handler."""
        return BingWallpaperOptionFlowHandler(config_entry)

    async def async_step_user(self, user_input: dict | None = None) -> ConfigFlowResult:
        """
        Provide Base information Config Flow.

        1st call = return form to show
        2nd call = return form with user input
        """
        if user_input is None:
            # 1st call
            return self.async_show_form(step_id="user", data_schema=user_form())
        # 2nd call
        # Verify name
        domain_entries = self.hass.config_entries.async_entries(domain=DOMAIN)
        domain_entries_title_slugs = [slugify(entry.title) for entry in domain_entries]
        LOGGER.debug(domain_entries_title_slugs)
        if slugify(user_input["name"]) in domain_entries_title_slugs:
            return self.async_show_form(
                step_id="user",
                data_schema=user_form(),
                errors={"base": "name_exist"},
            )
        user_input["name_by_user"] = user_input["name"]
        # Verify index
        if "index" in user_input:
            index_as_str = user_input["index"]
            if index_as_str != "random" and not index_as_str.isdigit():
                return self.async_show_form(
                    step_id="user",
                    data_schema=user_form(),
                    errors={"base": "invalid_index"},
                )

        return self.async_create_entry(title=user_input["name"], data=user_input)


class BingWallpaperOptionFlowHandler(OptionsFlow):
    """Reconfiguration flow for Bing Wallpaper."""

    def __init__(self, entry: ConfigEntry) -> None:
        """Init."""
        self.user_inputs: dict = {}
        self.entry = entry

    async def async_step_init(self, user_input: dict | None = None) -> ConfigFlowResult:
        """
        Provide new information.

        1st call = return form to show
        2nd call = return form with user input
        """
        suggested = {
            key: self.entry.data.get(key)
            for key in ["name", "refresh_rate", "index", "mkt", "resolution"]
        }
        form = user_form(suggested, edit=True)

        LOGGER.debug(
            "Option flow %s",
            self.config_entry.entry_id,
        )
        LOGGER.debug(suggested)

        if user_input is None:
            # 1st call
            return self.async_show_form(step_id="init", data_schema=form)

        # 2nd call
        LOGGER.debug(
            "Option flow %s 2nd Call",
            self.config_entry.entry_id,
        )
        LOGGER.debug(user_input)
        if "index" in user_input:
            index_as_str = user_input["index"]
            if index_as_str != "random" and not index_as_str.isdigit():
                return self.async_show_form(
                    step_id="init",
                    data_schema=user_form(suggested, edit=True),
                    errors={"base": "invalid_index"},
                )

        self.user_inputs = user_input

        # On appelle le step de fin pour enregistrer les modifications
        return await self.async_end()

    async def async_end(self) -> ConfigFlowResult:
        """Finitsh ConfigEntry modification."""
        LOGGER.info(
            "Entry %s is being recreated",
            self.config_entry.entry_id,
        )

        data = dict(self.config_entry.data)
        data.update(self.user_inputs)

        LOGGER.debug(self.user_inputs)
        LOGGER.debug(data)
        self.hass.config_entries.async_update_entry(self.config_entry, data=data)

        self.hass.config_entries.async_schedule_reload(self.config_entry.entry_id)

        return self.async_create_entry(
            # No data as config entry has been modified
            title=None,
            data={},
        )
