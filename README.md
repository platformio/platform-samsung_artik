# Samsung ARTIK: development platform for PlatformIO

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
You should have `com.apple.driver.AppleUSBFTDI` or `com.FTDI.driver.FTDIUSBSerialDriver` listed.
If neither shows then you need to download and install proper driver for your macOS version from
[FTDI's website](http://www.ftdichip.com/Drivers/VCP.htm).

After platformio has installed the `tool-artik-openocd package`, look for the
following file in your platformio's installation directory:
```bash
/Users/<username>/.platformio/packages/tool-artik-openocd/switch-driver.py
```
Edit the `/etc/sudoers` file and add the following line
```bash
<username> ALL = (ALL) NOPASSWD: <Full path to switch-driver.py>
```
Make sure you replace `<username>` with the actual user logged into macOS.

### Linux

Create a new file named `/etc/udev/rules.d/51-artik053.rules` and add the
following line:
```bash
SUBSYSTEM=="usb", ATTR{idVendor}=="0403", ATTR{idProduct}=="6010", MODE="0660", GROUP="plugdev", SYMLINK+="artik053-%n"
```
