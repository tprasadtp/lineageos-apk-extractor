## WIP
Extract APKs from Lineage OS ZIPs automatically and regularly.

[![Build Status](https://travis-ci.org/tprasadtp/lineageos-apk-extractor.svg?branch=master)](https://travis-ci.org/tprasadtp/ubuntu-post-install)
[![license](https://img.shields.io/github/license/tprasadtp/lineageos-apk-extractor.svg?style=flat)](https://github.com/tprasadtp/ubuntu-post-install/blob/master/LICENSE)
![GitHub repo size in bytes](https://img.shields.io/github/repo-size/tprasadtp/lineageos-apk-extractor.svg?style=flat)

Use Python 3.6+

[![Python](https://static.prasadt.com/logo64/python.png)](lineageos-apk-extractor)

## Details
Cron job releases the APKs Automatically every week.
If latest APKs are not updated, please open an issue.

- APKs are extracted weekly from Pixel(Marlin) or Nexus 6P(Angler) devices.
- Some APKs might depend on LOS framework and fail to install on AOSP or other builds.
- I absolutely take no responsibility for the APKS.
- Sometimes a build is pushed early and cron jobs might take some time to push the
APKs to Github releases.
- APKs and Zips are verified against available public keys.
- Log file of this verification can be obtained in releases.
- Releases are tagged according to their build dates mentioned in ZIPs.
- **No Tests** are carried out on APKs to ensure compatibility.
- `metadata` branch is a derivative branch, which holds necessary metadata
related to  files/releases. Its being used as a persistance storage for some data
like build  dates, tags, last executed date etc. I know its not ideal but hey, it
gets the job done :-P.

## Bugs

If you have a problem with APKs other than being corrupt or not extracted properly,
Please use Lineage OS Jira to open an issue. If you have any other issues open an
issue here. I will not provide help in downloading or installing the APKs unless
they are related or caused by this project.


## You Should Know

- If for some reason a build fails due to infrastructure issues on Github/Lineage/CI side,
APKs cannot be updated till next build schedule.

## Credits
- Python icon by Freepik from flaticon.com
- Original `sdat2img.py` by [Andrei Conache](https://github.com/xpirt/sdat2img).
I have modified it a bit. Please note that licence information
is missing from original repository.