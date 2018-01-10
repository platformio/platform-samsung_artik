# Samsung ARTIK: development platform for [PlatformIO](http://platformio.org)
[![Build Status](https://travis-ci.org/platformio/platform-samsung_artik.svg?branch=develop)](https://travis-ci.org/platformio/platform-samsung_artik)
[![Build status](https://ci.appveyor.com/api/projects/status/uluymxw3k4w41g2c?svg=true)](https://ci.appveyor.com/project/ivankravets/platform-samsung-artik)

The Samsung ARTIK platform brings support to PlatformIO for the non Linux-based
ARTIK modules. The boards that are currently supported by this platform are:
 * `artik_053`: ARTIK 053 Wi-Fi module running TizenRT

* [Home](http://platformio.org/platforms/samsung_artik) (home page in PlatformIO Platform Registry)
* [Documentation](http://docs.platformio.org/page/platforms/samsung_artik.html) (advanced usage, packages, boards, frameworks, etc.)


# Usage

1. [Install PlatformIO](http://platformio.org)
2. Create PlatformIO project and configure a platform option in [platformio.ini](http://docs.platformio.org/page/projectconf.html) file:

## Stable version

```ini
[env:stable]
platform = samsung_artik
board = ...
...
```

## Development version

```ini
[env:development]
platform = https://github.com/platformio/platform-samsung_artik.git
board = ...
...
```

# Configuration

Please navigate to [documentation](http://docs.platformio.org/page/platforms/samsung_artik.html#configuration).
