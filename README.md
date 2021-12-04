# LineageOS APKs

[![build](https://github.com/tprasadtp/lineageos-apk-extractor/actions/workflows/los-17.yml/badge.svg)](https://github.com/tprasadtp/lineageos-apk-extractor/actions/workflows/los-17.yml)
[![build](https://github.com/tprasadtp/lineageos-apk-extractor/actions/workflows/los-17.yml/badge.svg)](https://github.com/tprasadtp/lineageos-apk-extractor/actions/workflows/los-18.yml)


## Development

- AFAIK there is no API provided by LineageOS team, so currently the project uses bs4 to parse download page
- APKs are released on `tprasadtp/los-xx-apks` repositories to deal with multiple devices.

## Build

- Create a python virtual environment & activate it
- Install dependencies
    ```bash
    make install
    ```
- Set device codename name. See https://download.lineageos.org/ for codenames.
    ```bash
    export DEVICE=coral
    ```
- Download, Verify and extract payload.bin
    ```bash
    make build-payload
    ```
- Check that images are extractd to `build/$DEVICE`
- Mount desired image and check path of required APKs
- Update `data/transfer-$DEVICE.json` to match you image and APKs. For some targets, predefined `transfer.json` is available.
- Define Image name (Without extensions or path)
    ```bash
    export APK_IMG=product
    ```
-  Mount image and copy APKs (Requires root)
    ```bash
    make apks
    ```
