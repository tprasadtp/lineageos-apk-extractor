# Extract APKs from Lineage OS ZIPs & automatically upload to Github releases

[![Travis][travis-badge]][travis]
[![license][mit-badge]][license]
[![black][black-badge]][black]


## Build, version and CI metadata

### LineageOS 15.1 APKs

[![Device][L15-device]][L15-dl-page]
![Lineage-Version][L15-version]
![Lineage15-Build][L15-build]
[![Release][L15-last-release-date]][gh-releases]
![CI-Build-Num][L15-last-release-bnum]

#### Last build status

![Travis-Build][L15-ci-bnum]
![Travis Build Date][L15-ci-bdate]
![Travis-Deployed][L15-ci-bdeployed]


### LineageOS 16 APKs

Currently unavailable.

## Bugs

If you have a problems **other than** released APKs being corrupt or not extracted properly, please use Lineage OS Jira to open an issue.

- Build scripts are currently crappy. Plan is to migrate them to 100% Python.
- Travis executes scripts in a sub-shell, environment variables do not persist between scripts. Using Shell-script to export TAGS and build conditions for now.
- There is no easy way to mount ext4 image without using sudo. so, I have kept it outside python scripts.

## Credits

- Original `sdat2img.py` by [Andrei Conache](https://github.com/xpirt/sdat2img). Please note that license information is missing from original repository.
- Some builds use `brotli` to decompress `system.new.dat.br`.
- New AB scheme images are extracted using [this](https://github.com/cyxx/extract_android_ota_payload) Please note that license information is missing from original repository.
- Protobufs were recompiled using protobuf3

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
[L15-device]: https://img.shields.io/badge/dynamic/json.svg?label=device&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-bullhead.json&query=$.lineage.device

[L15-version]: https://img.shields.io/badge/dynamic/json.svg?label=version&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-bullhead.json&query=$.lineage.version

[L15-build]: https://img.shields.io/badge/dynamic/json.svg?label=build&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-bullhead.json&query=$.lineage.build&colorB=brightgreen

[L15-ci-bdate]: https://img.shields.io/badge/dynamic/json.svg?label=at&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-bullhead.json&query=$.ci.build_date_human&colorB=brightgreen

[L15-ci-bnum]: https://img.shields.io/badge/dynamic/json.svg?label=%23&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-bullhead.json&query=$.ci.build_number&colorB=green

[L15-ci-bdeployed]: https://img.shields.io/badge/dynamic/json.svg?label=deployed&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-bullhead.json&query=$.ci.deployed&logo&colorB=yellow

[L15-last-release-date]: https://img.shields.io/badge/dynamic/json.svg?label=on&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-bullhead.json&query=$.release.human_ts

[L15-last-release-bnum]: https://img.shields.io/badge/dynamic/json.svg?label=%23&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-bullhead.json&query=$.release.ci_bnum&colorB=green



<!-- LOS 16 References -->
[L16-device]: https://img.shields.io/badge/dynamic/json.svg?label=device&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-guacamole.json&query=$.lineage.device

[L16-version]: https://img.shields.io/badge/dynamic/json.svg?label=version&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-guacamole.json&query=$.lineage.version

[L16-build]: https://img.shields.io/badge/dynamic/json.svg?label=build&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-guacamole.json&query=$.lineage.build&colorB=brightgreen

[L16-ci-bdate]: https://img.shields.io/badge/dynamic/json.svg?label=at&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-guacamole.json&query=$.ci.build_date_human&colorB=brightgreen

[L16-ci-bnum]: https://img.shields.io/badge/dynamic/json.svg?label=%23&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-guacamole.json&query=$.ci.build_number&colorB=green

[L16-ci-bdeployed]: https://img.shields.io/badge/dynamic/json.svg?label=deployed&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-guacamole.json&query=$.ci.deployed&logo&colorB=yellow

[L16-last-release-date]: https://img.shields.io/badge/dynamic/json.svg?label=on&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-guacamole.json&query=$.release.human_ts

[L16-last-release-bnum]: https://img.shields.io/badge/dynamic/json.svg?label=%23&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release-guacamole.json&query=$.release.ci_bnum&colorB=green



<!-- Other Links-->
[gh-releases]: https://github.com/tprasadtp/lineageos-apk-extractor/releases/latest "View latest releases"
[license]: https://github.com/tprasadtp//blob/master/LICENSE.md "View License"
[travis-badge]: https://travis-ci.com/tprasadtp/lineageos-apk-extractor.svg?branch=master
[travis]: https://travis-ci.com/tprasadtp/lineageos-apk-extractor "Travis CI page"
[L16-dl-page]: https://download.lineageos.org/guacamole "Download Lineage 16"
[L15-dl-page]: https://download.lineageos.org/bullhead "Download Lineage 15"
[black]: https://github.com/psf/black "Black"

[mit-badge]: https://img.shields.io/badge/license-MIT-green
[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
