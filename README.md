# APKextract

Inspired by [apk2gold](https://github.com/lxdvs/apk2gold), except with a very unorginal name. This is essentially a wrapper around a few Android apk extraction tools for OSX/Linux/Windows.

## Requirements

* [Java version 1.7+](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
* [Python 2.7.+](https://www.python.org/download/releases/2.7.6/)
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
Repackage APK file
```bash
./apk.py -r [filename.apk]
```

## Notes

Repackage will repackage the apktool folder located in your output.  It only uses the "filename.apk" for it's naming convention.

## Tools

* [apktool](https://github.com/iBotPeaches/Apktool)
* [dex2jar](https://github.com/pxb1988/dex2jar)
* [jd-cli](https://github.com/kwart/jd-cmd)
