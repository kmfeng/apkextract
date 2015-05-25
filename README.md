# APKextract

Inspired by [apk2gold](https://github.com/lxdvs/apk2gold), except with a very unorginal name. This is essentially a wrapper around a few Android apk extraction tools for OSX/Linux.

## Why not use apk2gold?

They are very similar but I wanted one python script to act as a wrapper.  There is nothing wrong with apk2gold, but I want to expand on extraction/recompilation down the road.

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
```bash
./apk.py [filename.apk]
```
## Tools

* [apktool](https://github.com/iBotPeaches/Apktool)
* [dex2jar](https://github.com/pxb1988/dex2jar)
* [jd-cli](https://github.com/kwart/jd-cmd)
