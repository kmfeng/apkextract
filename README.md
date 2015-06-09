# APKextract

Inspired by [apk2gold](https://github.com/lxdvs/apk2gold), except with a very unorginal name. This is essentially a wrapper around a few Android apk extraction tools for OSX/Linux/Windows.

## Requirements

* [Java version 1.7+](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
* [Python 3.+](https://www.python.org/downloads/)
* git (optional: For downloading repo)

## Installation

```bash
git clone https://github.com/binkybear/apkextract.git
cd apkextract
```

## Usage
Extract APK file
```bash
python3 apk.py -e [filename.apk]
```
Extract APK file to specified output folder
```bash
python3 apk.py -e [filename.apk] -o flappybirdrocks
```
Repackage APK from a working directory
```bash
python3 apk.py -r flapplybirdrocks
```

## Notes

Repackage will repackage the apktool folder located in your output.  It only uses the "filename.apk" for it's naming convention.

## Tools

* [apktool](https://github.com/iBotPeaches/Apktool)
* [enjarify](https://github.com/google/enjarify)
* [jd-cli](https://github.com/kwart/jd-cmd)
