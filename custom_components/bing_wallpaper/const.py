"""Constants for bing_wallpaper."""

from logging import Logger, getLogger

from homeassistant.const import Platform

STORAGE_KEY = "bing_wallpaper_data"

LOGGER: Logger = getLogger(__package__)

DOMAIN = "bing_wallpaper"

STORAGE_DIR = "bing_wallpaper"

MANUFACTURER = "Bing Wallpaper"

HEALTH_OPTIONS = [
    "notset",
    "poor",
    "fair",
    "good",
    "verygood",
    "excellent",
]

IMAGES_MIME_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".bmp": "image/bmp",
    ".webp": "image/webp",
    ".tiff": "image/tiff",
    ".svg": "image/svg+xml",
}

PLATFORMS: list[Platform] = [
    Platform.BUTTON,
    Platform.BINARY_SENSOR,
    Platform.DATE,
    Platform.IMAGE,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.SENSOR,
]
