# Extract APKs from Lineage OS ZIPs & automatically upload to Github releases regularly

[![Build Status](https://travis-ci.com/tprasadtp/lineageos-apk-extractor.svg?branch=master)](https://travis-ci.com/tprasadtp/lineageos-apk-extractor)
[![license](https://img.shields.io/github/license/tprasadtp/lineageos-apk-extractor.svg?style=flat)](https://github.com/tprasadtp//blob/master/LICENSE)
![GitHub repo size](https://img.shields.io/github/repo-size/tprasadtp/lineageos-apk-extractor.svg?style=flat&icon=github)

### Lineage OS Details

[![Lineage Version](https://img.shields.io/badge/dynamic/json.svg?label=Lineage%20Version&style=flat&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release.json&query=$.lineage.version)](https://github.com/tprasadtp/lineageos-apk-extractor/releases/latest)
![Lineage Build Date](https://img.shields.io/badge/dynamic/json.svg?label=Build%20Date&style=flat&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release.json&query=$.lineage.build)
![Lineage Build Type](https://img.shields.io/badge/dynamic/json.svg?label=Build%20Type&style=flat&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release.json&query=$.lineage.build_type)


### CI

[![Last Built on](https://img.shields.io/badge/dynamic/json.svg?label=Last%20Build%20on&style=flat&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release.json&query=$.ci.build_ts&logo=travis&colorB=blue)](https://github.com/tprasadtp/lineageos-apk-extractor/releases/latest)
[![Last Build Deployed](https://img.shields.io/badge/dynamic/json.svg?label=Last%20Build%20Deployed&style=flat&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release.json&query=$.ci.deployed&logo=travis)](https://github.com/tprasadtp/lineageos-apk-extractor/releases/latest)
![Build Tag](https://img.shields.io/badge/dynamic/json.svg?label=Build%20Tag&style=flat&url=https://raw.githubusercontent.com/tprasadtp/lineageos-apk-extractor/gh-pages/release.json&query=release.tag&logo=github&link=$.release.tag)
[![GitHub (pre-)release](https://img.shields.io/github/release/tprasadtp/lineageos-apk-extractor/all.svg?style=flat&logo=github&label=Release&colorB=blue)](https://github.com/tprasadtp/lineageos-apk-extractor/releases)



Use Python 3.6+

![Python](https://static.prasadt.com/logo64/python.png)

## Details

- APKs are extracted weekly from Pixel(Marlin) or Nexus 5X(bullhead) devices.
- Some APKs might depend on LOS framework and fail to install on AOSP or other builds.
- I take absolutely no responsibility for the APKs.
- Log file of this verification can be obtained in releases.
- Releases are tagged according to their build dates mentioned in ZIPs.
- **No Tests** are carried out on APKs to ensure compatibility.
- `metadata` branch is a derivative branch, which holds necessary metadata related to  files/releases. Its being used as a persistance storage for some data like build  dates, tags, last executed date etc.

## Bugs

If you have a problems **other than** APKs being corrupt or not extracted properly, Please use Lineage OS Jira to open an issue.

- Build scripts are currently crappy. Plan is to migrate them to 100% Python.
- Travis release notes are buggy as they do not escape markdown. Temp solution is to use a ruby script.
- Travis executes scripts in a subshell, environment variables do not persist between scripts. Using Shellscript to export TAGS and build conditions for now.
- There is no easy way to mount ext4 image without being root. so, I have kept it outside python scripts.

## Credits

- Python icon by Freepik from flaticon.com
- Original `sdat2img.py` by [Andrei Conache](https://github.com/xpirt/sdat2img). Please note that licence information is missing from original repository.