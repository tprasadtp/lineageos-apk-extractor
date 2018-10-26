# Extract APKs from Lineage OS ZIPs automatically and upload to github releases regularly

[![Build Status](https://travis-ci.org/tprasadtp/lineageos-apk-extractor.svg?branch=master)](https://travis-ci.org/tprasadtp/ubuntu-post-install)
[![license](https://img.shields.io/github/license/tprasadtp/lineageos-apk-extractor.svg?style=flat)](https://github.com/tprasadtp/ubuntu-post-install/blob/master/LICENSE)
![GitHub repo size in bytes](https://img.shields.io/github/repo-size/tprasadtp/lineageos-apk-extractor.svg?style=flat)

Use Python 3.6+

[![Python](https://static.prasadt.com/logo64/python.png)](lineageos-apk-extractor)

## Details

Cron job releases the APKs Automatically every week.

- APKs are extracted weekly from Pixel(Marlin) or Nexus 6P(Angler) devices.
- Some APKs might depend on LOS framework and fail to install on AOSP or other builds.
- I absolutely take no responsibility for the APKS.
- Sometimes a build is pushed early and cron jobs might take some time to push the APKs to Github releases.
- APKs and Zips are verified against available public keys.
- Log file of this verification can be obtained in releases.
- Releases are tagged according to their build dates mentioned in ZIPs.
- **No Tests** are carried out on APKs to ensure compatibility.
- `metadata` branch is a derivative branch, which holds necessary metadata related to  files/releases. Its being used as a persistance storage for some data like build  dates, tags,last executed date etc. I know its not ideal but hey, it. gets the job done :-P.

## Bugs

If you have a problems **other than** APKs being corrupt or not extracted properly, Please use Lineage OS Jira to open an issue.

- Build scripts are currently crappy. Plan is to migrate to 100% Python.
- Travis release notes are buggy as they do not escape markdown. Temp solution is to use a ruby script.
- Travis executes scripts in a subshell, environment variables do not persist between scripts unless sourced. Use Shellscript to export TAGS and Build conditions for now.
- There is no easy way to mount ext4 image without being root. so, I have kept it outside python scripts.

## You Should Know

- If for some reason a build fails due to infrastructure issues on Github/Lineage/CI side, APKs cannot be updated till next build schedule.

## Credits

- Python icon by Freepik from flaticon.com
- Original `sdat2img.py` by [Andrei Conache](https://github.com/xpirt/sdat2img). Please note that licence information is missing from original repository.