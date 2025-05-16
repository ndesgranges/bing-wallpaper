"""Constants for bing_wallpaper."""

from enum import Enum
from logging import Logger, getLogger

from homeassistant.const import Platform

STORAGE_KEY = "bing_wallpaper_data"

LOGGER: Logger = getLogger(__package__)

DOMAIN = "bing_wallpaper"

STORAGE_DIR = "bing_wallpaper"

MANUFACTURER = "Bing Wallpaper"


class LangOption(Enum):
    """Language options for Bing Wallpaper."""

    EN_US = "en-US"
    JA_JP = "ja-JP"
    EN_AU = "en-AU"
    EN_GB = "en-GB"
    DE_DE = "de-DE"
    EN_NZ = "en-NZ"
    EN_CA = "en-CA"
    EN_IN = "en-IN"
    FR_FR = "fr-FR"
    FR_CA = "fr-CA"
    IT_IT = "it-IT"
    ES_ES = "es-ES"
    PT_BR = "pt-BR"
    EN_ROW = "en-ROW"
    ZH_CN = "zh-CN"


LANG_OPTIONS = [lang.value for lang in LangOption.__members__.values()]


class ResolutionOption(Enum):
    """Resolution options for Bing Wallpaper."""

    UHD = "UHD"
    WUXGA = "1920x1200"
    FHD = "1920x1080"
    WXGA_HD = "1366x768"
    WXGA = "1280x768"
    WXGA_PORTRAIT = "768x1280"
    HD_PORTRAIT = "720x1280"
    XGA = "1024x768"
    SVGA = "800x600"
    WVGA = "800x480"
    WVGA_PORTRAIT = "480x800"
    VGA = "640x480"
    WQVGA = "400x240"
    QVGA = "320x240"
    QVGA_PORTRAIT = "240x320"


RESOLUTION_OPTIONS = [lang.value for lang in ResolutionOption.__members__.values()]

PLATFORMS: list[Platform] = [
    Platform.IMAGE,
    Platform.TEXT,
]
