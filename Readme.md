## WIP
Extract APKs from Lineage OS ZIPs automatically and regularly.

[![Build Status](https://travis-ci.org/tprasadtp/lineageos-apk-extractor.svg?branch=master)](https://travis-ci.org/tprasadtp/ubuntu-post-install)
[![license](https://img.shields.io/github/license/tprasadtp/ubuntu-post-install.svg?style=flat)](https://github.com/tprasadtp/ubuntu-post-install/blob/master/LICENSE)
![GitHub repo size in bytes](https://img.shields.io/github/repo-size/tprasadtp/ubuntu-post-install.svg?style=flat)

[![Bash](https://static.prasadt.com/logo64/bash.png)](https://github.com/tprasadtp/ubuntu-post-install)


## Python 2

Use Python 3.6+
Python 2 is **NOT** supported.


## Details

- APKs are extracted weekly from Pixel or Nexus 6P devices.
- Some APKs might depend on LOS framework and fail to isntall on AOSP or other builds.
- I absolutely take no responsibility for the APKS.
- Sometimes a build is pushed early and cron jons might take some time to push the
APKs to Github releases.
- APKs and Zips are verified agaist Public keys available.
- Log file of this verification can be obtained in Releases.
- Releases are tagged according to their build dates mentioned in ZIPs.
- **No Tests** are carried out on APKs to ensure compatibility.


## Bugs

If you have a problem with APKs other than being corrupt or not extracted properly, Please use Lineage OS Jira
to open an issue. If you have any other issues open an issue here. I will not provide help in downloading or
installing the APKs unless they are related or caused by this project.

## PRs Welcome.