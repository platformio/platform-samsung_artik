# Samsung ARTIK: development platform for [PlatformIO](http://platformio.org)
[![Build Status](https://travis-ci.org/platformio/platform-samsung_artik.svg?branch=develop)](https://travis-ci.org/platformio/platform-samsung_artik)
[![Build status](https://ci.appveyor.com/api/projects/status/6vyuk4avv66atccu/branch/develop?svg=true)](https://ci.appveyor.com/project/ivankravets/platform-samsung-artik/branch/develop)

The Samsung ARTIK platform brings support to PlatformIO for the non Linux-based
ARTIK modules. The boards that are currently supported by this platform are:
 * `artik_053`: ARTIK 053 Wi-Fi module running TizenRT

## Usage

1. [Install PlatformIO Core](http://docs.platformio.org/page/core.html)
2. Install Samsung ARTIK development platform:
```bash
# install the latest stable version
> platformio platform install samsung_artik

# install development version
> platformio platform install https://github.com/platformio/platform-samsung_artik.git
```

## Configuration instructions

If you are using the Samsung ARTIK platform on macOS or Linux, you need to
perform the configuration steps detailed below to enable support for deployment
and debugging.

### macOS

First check that you have a FTDI compatible driver on your mac:
```bash
$ kextstat | grep FTDI
```
You should have `com.apple.driver.AppleUSBFTDI`.
1. install [Artik_FTDI_Driver](http://developer.artik.io/downloads/artik_ide/platformio/Artik053FTDIDriver.pkg).
2. reboot your system.

### Linux

Create a new file named `/etc/udev/rules.d/51-artik053.rules` and add the
following line:
```bash
SUBSYSTEM=="usb", ATTR{idVendor}=="0403", ATTR{idProduct}=="6010", MODE="0660", GROUP="plugdev", SYMLINK+="artik053-%n"
```

### windows
1. Usually windows update service will automatically install [FTDI driver](http://developer.artik.io/downloads/artik_ide/platformio/CDM_v2.12.26_WHQL_Certified.zip),If necessary you can choose an offline installation.
2. After install FTDI driver it will has two FTDI device and use [zadig](http://developer.artik.io/downloads/artik_ide/platformio/zadig-2.3.exe) tool change one FTDI device to a libusb compatible device.
