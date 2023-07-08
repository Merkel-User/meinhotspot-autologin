#!/usr/bin/env python3

import os
import ssl
import subprocess
import sys
import time
import urllib.request

def exec_wmic(where=''):
    return subprocess.run(('wmic', 'nic', 'where', where), capture_output=True, text=True).stdout

def print_error(msg):
    print(msg, file=sys.stderr)
    subprocess.run(('msg', os.environ['USERNAME'], '[meinhotspot auto login] ' + msg))

interface_name = False
for name in ['WiFi', 'WLAN']:
    if subprocess.run(('netsh', 'interface', 'show', 'interface', name), stdout=subprocess.DEVNULL).returncode == 0:
        interface_name = name
        break

if not interface_name:
    print_error('Could not find the Wi-Fi interface!')
    sys.exit(1)

print(f'Using MAC address of interface "{interface_name}"')

adapter_data = exec_wmic(f'NetConnectionID="{interface_name}"')
mac_addr = adapter_data.split('\n')[2][adapter_data.find('MACAddress'):].split(' ')[0]

print('Found MAC address: ' + mac_addr)

LOGIN_PAYLOAD = urllib.parse.urlencode((
    ('dst', 'https://connect.meinhotspot.com/de/client/redirect'),
    ('popup', 'true'),
    ('username', mac_addr),
    ('password', mac_addr),
    ('mac', mac_addr),
)).encode('utf-8')

# allow connections with insecure TLS standards
security_ctx = ssl.create_default_context()
security_ctx.check_hostname = False
security_ctx.set_ciphers('DEFAULT@SECLEVEL=0')

while True:
    try:
        with urllib.request.urlopen('https://example.com', timeout=30) as res:
            logged_in = res.getcode() == 200
    except:
        logged_in = False
    if not logged_in:
        print('Trying to log in ...')
        req = urllib.request.Request('https://login.meinhotspot.com/login', headers={
            'Connection': 'Close',
            'Content-Length': len(LOGIN_PAYLOAD),
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://connect.meinhotspot.com/en/client/welcome',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
        })
        with urllib.request.urlopen(req, LOGIN_PAYLOAD, context=security_ctx) as res:
            code = res.getcode()
            if code == 200:
                print('Successfully logged in.')
            else:
                print_error('Failed to log in!\nError code: ' + code)
    
    time.sleep(60)