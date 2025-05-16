"""Interface with API to get image."""

from http import HTTPStatus, client

import aiohttp

from .const import LOGGER, LangOption, ResolutionOption


async def request_wallpaper(
    index: int, mkt: LangOption, resolution: ResolutionOption
) -> dict[str, str]:
    """
    Request a new image to Bing.

    Uses API from https://github.com/TimothyYe/bing-wallpaper
    """
    index_as_str = str(index)
    mkt_as_str = str(mkt.value)
    resolution_as_str = str(resolution.value)

    url = f"https://bing.biturl.top/?resolution={resolution_as_str}&format=json&index={index_as_str}&mkt={mkt_as_str}"
    LOGGER.info("Requesting new wallpaper at %s", url)

    async with aiohttp.ClientSession() as session, session.get(url) as response:
        if not HTTPStatus(response.status).is_success:
            LOGGER.error("HTTP error when requesting a new image: %s", response.status)
            raise client.HTTPException

        data = await response.json()

    image_description = str(data.get("copyright"))
    image_url = str(data.get("url"))

    return {
        "image_description": image_description.split("(", 1)[0],
        "image_url": image_url,
    }
