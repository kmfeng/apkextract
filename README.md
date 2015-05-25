# APKextract

Inspired by [apk2gold](https://github.com/lxdvs/apk2gold), except with a very unorginal name. This is essentially a wrapper around a few Android apk extraction tools for OSX/Linux.

## Requirements

* Unix/Linux/OSX
* Java version 1.7+
* git (optional: For downloading repo)

## Installation

```bash
git clone https://github.com/binkybear/apkextract.git
cd apkextract
```

## Usage
Extract APK file
```bash
./apk.py -e [filename.apk]
```
Repackage APK file. Repackage will repack the apktool folder in your output directory but uses the filename.apk for the name of the output folder. 
```bash
./apk.py -r [filename.apk]
```

## Tools

* [apktool](https://github.com/iBotPeaches/Apktool)
* [dex2jar](https://github.com/pxb1988/dex2jar)
* [jd-cli](https://github.com/kwart/jd-cmd)
