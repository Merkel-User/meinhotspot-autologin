# [meinhotspot-autologin](https://github.com/Merkel-User/meinhotspot-autologin)

\[Windows only\]

## Automatically log into Mein Hotspot

## Description

The script automatically logs into Mein Hotspot every minute, if the computer is not connected to the internet.

It first tries to find the MAC address of a network interface that is either named `WiFi` or `WLAN`.

*Note: Your WiFi network interface should already be named like that if you installed your Windows as English or German.*

The MAC address is then used to authenticate with Mein Hotspot.

## Running on startup

1. Press WIN+R, copy the following text into the menu and press return:

```plain
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
```

2. In the *Startup* directory, create a shortcut to `hotspot-login.py` by right clicking on an empty spot in the file list and then clicking *New* -> *Shortcut*

## Credit

This script was written by ever and me

## License

© evur, Merkel User, and contributors

This software and it's accompanying files are licensed under the *Mozilla Public License Version 2.0*.

For the license's contents, see [LICENSE](LICENSE) or go to <https://mozilla.org/MPL/2.0/>.
