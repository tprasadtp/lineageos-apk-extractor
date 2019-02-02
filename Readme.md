# Extract APKs from Lineage OS ZIPs & automatically upload to Github releases

[![Travis (.com)](https://img.shields.io/travis/com/tprasadtp/lineageos-apk-extractor.svg?style=for-the-badge)](https://travis-ci.com/tprasadtp/lineageos-apk-extractor)

### Lineage 15 from Bullhead

[![Lineage 15 Version](https://img.shields.io/badge/dynamic/json.svg?label=Version&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-bullhead.json&query=$.lineage.version)](https://github.com/tprasadtp/lineageos-apk-extractor/releases/latest)
![Lineage 15 Build Date](https://img.shields.io/badge/dynamic/json.svg?label=Build%20Date&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-bullhead.json&query=$.lineage.build)
![Lineage 15 Build Type](https://img.shields.io/badge/dynamic/json.svg?label=Type&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-bullhead.json&query=$.lineage.build_type&colorB=b29505)

[![15 Last Built on](https://img.shields.io/badge/dynamic/json.svg?label=Last%20Built%20on&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-bullhead.json&query=$.ci.build_date_human&colorB=blue)](https://github.com/tprasadtp/lineageos-apk-extractor/tree/gh-pages/logs)
[![15 Last Built on](https://img.shields.io/badge/dynamic/json.svg?label=Build&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-bullhead.json&query=$.ci.build_number&colorB=blue)](https://travis-ci.com/tprasadtp/lineageos-apk-extractor)

[![Last Build Deployed](https://img.shields.io/badge/dynamic/json.svg?label=Last%20Build%20Deployed&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-bullhead.json&query=$.ci.deployed&logo&colorB=a442f4)](https://github.com/tprasadtp/lineageos-apk-extractor/releases/latest) [![Last Released On](https://img.shields.io/badge/dynamic/json.svg?label=Last%20Released%20On&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-bullhead.json&query=$.release.human_ts)](https://github.com/tprasadtp/lineageos-apk-extractor/releases/latest)


### Lineage 14 from hammerhead

[![Lineage 15 Version](https://img.shields.io/badge/dynamic/json.svg?label=Version&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-hammerhead.json.json&query=$.lineage.version)](https://github.com/tprasadtp/lineageos-apk-extractor/releases/latest)
![Lineage 15 Build Date](https://img.shields.io/badge/dynamic/json.svg?label=Build%20Date&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-hammerhead.json.json&query=$.lineage.build)
![Lineage 15 Build Type](https://img.shields.io/badge/dynamic/json.svg?label=Type&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-hammerhead.json.json&query=$.lineage.build_type&colorB=b29505)

[![15 Last Built on](https://img.shields.io/badge/dynamic/json.svg?label=Last%20Built%20on&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-hammerhead.json.json&query=$.ci.build_date_human&colorB=blue)](https://github.com/tprasadtp/lineageos-apk-extractor/tree/gh-pages/logs)
[![15 Last Built on](https://img.shields.io/badge/dynamic/json.svg?label=Build&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-hammerhead.json.json&query=$.ci.build_number&colorB=blue)](https://travis-ci.com/tprasadtp/lineageos-apk-extractor)

[![Last Build Deployed](https://img.shields.io/badge/dynamic/json.svg?label=Last%20Build%20Deployed&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-hammerhead.json.json&query=$.ci.deployed&logo&colorB=a442f4)](https://github.com/tprasadtp/lineageos-apk-extractor/releases/latest) [![Last Released On](https://img.shields.io/badge/dynamic/json.svg?label=Last%20Released%20On&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-hammerhead.json.json&query=$.release.human_ts)](https://github.com/tprasadtp/lineageos-apk-extractor/releases/latest)


### Other Metadata

[![Updates](https://pyup.io/repos/github/tprasadtp/lineageos-apk-extractor/shield.svg)](https://github/tprasadtp/lineageos-apk-extractor/)
![GitHub pull requests](https://img.shields.io/github/issues-pr-raw/tprasadtp/lineageos-apk-extractor.svg)
[![license](https://img.shields.io/github/license/tprasadtp/lineageos-apk-extractor.svg)](https://github.com/tprasadtp//blob/master/LICENSE)

## Details

- APKs are extracted weekly from Pixel(Marlin) or Nexus 5X(bullhead) devices.
- Some APKs might depend on LOS framework and fail to install on AOSP or other builds.
- I take absolutely no responsibility for the APKs.
- Log file of this verification can be obtained in releases.
- Releases are tagged according to their build dates mentioned in ZIPs.
- **No Tests** are carried out on APKs to ensure compatibility.
- `metadata` branch is a derivative branch, which holds necessary metadata related to  files/releases. Its being used as a persistance storage for some data like build  dates, tags, last executed date etc.

## Bugs

If you have a problems **other than** released APKs being corrupt or not extracted properly, please use Lineage OS Jira to open an issue.

- Build scripts are currently crappy. Plan is to migrate them to 100% Python.
- Travis executes scripts in a subshell, environment variables do not persist between scripts. Using Shellscript to export TAGS and build conditions for now.
- There is no easy way to mount ext4 image without using sudo. so, I have kept it outside python scripts.

## Credits

- Python icon by Freepik from flat-squareicon.com
- Original `sdat2img.py` by [Andrei Conache](https://github.com/xpirt/sdat2img). Please note that licence information is missing from original repository.
- Builds use `brotli` to decompress `system.new.dat.br`.

## APKs

```json
{
    "Email": "/mnt/lineage/app/Email/Email.apk",
    "Gallery": "/mnt/lineage/priv-app/Gallery2/Gallery2.apk",
    "Music": "/mnt/lineage/priv-app/Eleven/Eleven.apk",
    "Calendar": "/mnt/lineage/app/Calendar/Calendar.apk",
    "Jelly": "/mnt/lineage/app/Jelly/Jelly.apk",
    "Trebuchet": "/mnt/lineage/priv-app/Trebuchet/Trebuchet.apk",
    "Recorder": "/mnt/lineage/priv-app/Recorder/Recorder.apk",
    "messaging": "/mnt/lineage/app/messaging/messaging.apk",
    "DeskClock": "/mnt/lineage/app/DeskClock/DeskClock.apk"
}
```
