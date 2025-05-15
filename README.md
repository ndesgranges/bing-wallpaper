
![Microsoft Bing Icon](custom_components/bing_wallpaper/brands/icon.png)
# Bing Wallpaper


[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![buymeacoffee](https://img.shields.io/badge/buy%20me%20a%20coffee-%23FFDD00?style=for-the-badge&logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/ndesgranges)

Bing Wallpaper aims to provide a very simple integration to expose an image from Bing Wallpaper to Home Assistant and refresh it regularly.

Use it to display in an image entity card or with the awesome [j-a-n/lovelace-wallpanel](https://github.com/j-a-n/lovelace-wallpanel) integration



## Installation

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ndesgranges&repository=bing_wallpaper&category=integration)

OR

1. Install HACS if you don't have it already
2. Open HACS in Home Assistant
3. On the top right side, click the three dot and click `Custom repositories`
4. Where asked for a URL, paste the link of this repository:
https://github.com/ndesgranges/bing-wallpaper
5. Where asked for a type, select `integration`
6. Click the download button. ⬇️

## Parameters

| Name | Description | Values |
| ---- | ----------- | ------ |
| refresh_rate | Minutes between refresh of the image | integer >= 1 (default: 1) |
| index | The index of wallpaper. 0 means today's image, 1 means yesterday, and so on. `random` chooses randomely between 0 and 7. | integer >= 0 or `random` (default) |
| mkt | region parameter, this changes the description language and might also change the image returned | `en-US` (default), `ja-JP`, `en-AU`, `en-GB`, `de-DE`, `en-NZ`, `en-CA`, `en-IN`, `fr-FR`, `fr-CA`, `it-IT`, `es-ES`, `pt-BR`, `en-ROW`, `zh-CN` |
| resolution | resolution of the image | `UHD` (default), `1920x1200`, `1920x1080`, `1366x768`, `1280x768`, `1024x768`, `800x600`, `800x480`, `768x1280`, `720x1280`, `640x480`, `480x800`, `400x240`, `320x240`, `240x320` |


## entities

| Type | Description |
| ---- | ----------- |
| image | Hold the link of the image |
| sensor | Hold the description of the image and copyright |

## TODO

See the [list of tasks to do](https://github.com/ndesgranges/bing-wallpaper/issues?q=is%3Aissue%20state%3Aopen%20label%3Aaccepted)


## Credits

This project is powered by [TimothyYe/bing-wallpaper](https://github.com/TimothyYe/bing-wallpaper)
