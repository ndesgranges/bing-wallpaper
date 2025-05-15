"""Constants for bing_wallpaper."""

from logging import Logger, getLogger

from homeassistant.const import Platform

STORAGE_KEY = "bing_wallpaper_data"

LOGGER: Logger = getLogger(__package__)

DOMAIN = "bing_wallpaper"

STORAGE_DIR = "bing_wallpaper"

MANUFACTURER = "Bing Wallpaper"

LANG_OPTIONS = [
    "en-US",
    "ja-JP",
    "en-AU",
    "en-GB",
    "de-DE",
    "en-NZ",
    "en-CA",
    "en-IN",
    "fr-FR",
    "fr-CA",
    "it-IT",
    "es-ES",
    "pt-BR",
    "en-ROW",
    "zh-CN",
]

RESOLUTION_OPTIONS = [
    "UHD",
    "1920x1200",
    "1920x1080",
    "1366x768",
    "1280x768",
    "1024x768",
    "800x600",
    "800x480",
    "768x1280",
    "720x1280",
    "640x480",
    "480x800",
    "400x240",
    "320x240",
    "240x320",
]

PLATFORMS: list[Platform] = [
    Platform.IMAGE,
    Platform.TEXT,
]
