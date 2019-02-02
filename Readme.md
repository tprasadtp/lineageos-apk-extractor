# Extract APKs from Lineage OS ZIPs & automatically upload to Github releases

[![Travis](https://img.shields.io/travis/com/tprasadtp/lineageos-apk-extractor.svg?style=for-the-badge)][travis]
[![License][license-badge]][license-link]

## Build, version and CI metadata

| Property           | Lineage OS 15.1                                  | Lineage OS 14.1                                  |
| ------------------ | ------------------------------------------------ | ------------------------------------------------ |
| Device             | [![Device][L15-device]][L15-dl-page]             | [![Device][L14-device]][L14-dl-page]             |
| Lineage version    | ![Lineage-Version][L15-version]                  | ![Lineage-Version][L14-version]                  |
| LOS type           | ![Lineage15-Type][L15-type]                      | ![Lineage14-Type][L14-type]                      |
| LOS build          | [![Lineage15-Build][L15-build]][travis]          | [![Lineage14-Build][L14-build]][travis]          |
| CI Build num       | [![Travis-Build][L15-ci-bnum]][travis]           | [![Travis-Build][L14-ci-bnum]][travis]           |
| CI Build on        | ![Travis Build Date][L15-ci-bdate]               | ![Travis Build Date][L14-ci-bdate]               |
| CI build deployed? | ![Travis-Deployed][L15-ci-bdeployed]             | ![Travis-Deployed][L14-ci-bdeployed]             |
| Latest Releases    | [![Release][L15-last-release-date]][gh-releases] | [![Release][L14-last-release-date]][gh-releases] |
| Latest Release CI# | ![CI-Build-Num][L15-last-release-bnum]           | ![CI-Build-Num][L14-last-release-bnum]           |

## Bugs

If you have a problems **other than** released APKs being corrupt or not extracted properly, please use Lineage OS Jira to open an issue.

- Build scripts are currently crappy. Plan is to migrate them to 100% Python.
- Travis executes scripts in a sub-shell, environment variables do not persist between scripts. Using Shell-script to export TAGS and build conditions for now.
- There is no easy way to mount ext4 image without using sudo. so, I have kept it outside python scripts.

## Credits

- Original `sdat2img.py` by [Andrei Conache](https://github.com/xpirt/sdat2img). Please note that license information is missing from original repository.
- Some builds use `brotli` to decompress `system.new.dat.br`.

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

<!-- LOS 15 References -->
[L15-device]: https://img.shields.io/badge/dynamic/json.svg?label=Device&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-bullhead.json&query=$.lineage.device

[L15-version]: https://img.shields.io/badge/dynamic/json.svg?label=Version&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-bullhead.json&query=$.lineage.version

[L15-build]: https://img.shields.io/badge/dynamic/json.svg?label=Build&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-bullhead.json&query=$.lineage.build

[L15-type]: https://img.shields.io/badge/dynamic/json.svg?label=Type&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-bullhead.json&query=$.lineage.build_type&colorB=b29505

[L15-ci-bdate]: https://img.shields.io/badge/dynamic/json.svg?label=CI%20Built%20on&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-bullhead.json&query=$.ci.build_date_human&colorB=blue

[L15-ci-bnum]: https://img.shields.io/badge/dynamic/json.svg?label=%23&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-bullhead.json&query=$.ci.build_number&colorB=blue

[L15-ci-bdeployed]: https://img.shields.io/badge/dynamic/json.svg?label=Last%20Build%20Deployed&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-bullhead.json&query=$.ci.deployed&logo&colorB=a442f4   

[L15-last-release-date]: https://img.shields.io/badge/dynamic/json.svg?label=Last%20Released%20On&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-bullhead.json&query=$.release.human_ts

[L15-last-release-bnum]: https://img.shields.io/badge/dynamic/json.svg?label=%23&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-bullhead.json&query=$.release.ci_bnum



<!-- LOS 14 References -->
[L14-device]: https://img.shields.io/badge/dynamic/json.svg?label=Device&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-hammerhead.json&query=$.lineage.device

[L14-version]: https://img.shields.io/badge/dynamic/json.svg?label=Version&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-hammerhead.json&query=$.lineage.version

[L14-build]: https://img.shields.io/badge/dynamic/json.svg?label=Build&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-hammerhead.json&query=$.lineage.build

[L14-type]: https://img.shields.io/badge/dynamic/json.svg?label=Type&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-hammerhead.json&query=$.lineage.build_type&colorB=b29505

[L14-ci-bdate]: https://img.shields.io/badge/dynamic/json.svg?label=CI%20Built%20on&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-hammerhead.json&query=$.ci.build_date_human&colorB=blue

[L14-ci-bnum]: https://img.shields.io/badge/dynamic/json.svg?label=%23&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-hammerhead.json&query=$.ci.build_number&colorB=blue

[L14-ci-bdeployed]: https://img.shields.io/badge/dynamic/json.svg?label=Last%20Build%20Deployed&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-hammerhead.json&query=$.ci.deployed&logo&colorB=a442f4   

[L14-last-release-date]: https://img.shields.io/badge/dynamic/json.svg?label=Last%20Released%20On&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-hammerhead.json&query=$.release.human_ts

[L14-last-release-bnum]: https://img.shields.io/badge/dynamic/json.svg?label=%23&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-hammerhead.json&query=$.release.ci_bnum



<!-- Other Links-->
[gh-releases]: https://github.com/tprasadtp/lineageos-apk-extractor/releases/latest "View latest releases"
[license-badge]: https://img.shields.io/github/license/tprasadtp/lineageos-apk-extractor.svg?style=for-the-badge
[license-link]: https://github.com/tprasadtp//blob/master/LICENSE "View License"
[logs]: https://github.com/tprasadtp/lineageos-apk-extractor/tree/gh-pages/logs "Logs"
[travis]: https://travis-ci.com/tprasadtp/lineageos-apk-extractor "Travis CI page"
[L14-dl-page]: https://download.lineageos.org/hammerhead "Download Lineage 14"
[L15-dl-page]: https://download.lineageos.org/bullhead "Download Lineage 15"
