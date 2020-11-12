# league-bot

[Features](#features)

[Installation](#installation-on-linux)

[Known Bugs](#known-bugs)

## Features
 - Champion runes, build and summoner spells getting
 - Getting champions for all positions
 - Getting summoner stats

## Installation on linux
### New systems
At the beginning, you have to create `rc-local` service. 

To do this, execute this command:
```sh
sudo nano /etc/systemd/system/rc-local.service
```
and then insert this data into it:
```
[Unit]
 Description=/etc/rc.local Compatibility
 ConditionPathExists=/etc/rc.local

[Service]
 Type=forking
 ExecStart=/etc/rc.local start
 TimeoutSec=0
 StandardOutput=tty
 RemainAfterExit=yes
 SysVStartPriority=99

[Install]
 WantedBy=multi-user.target
```
After previous steps create file `/etc/rc.local`, and insert this:
```sh
#!/bin/bash
python3 /root/league-bot/main.py
```
But we need to make it executable, so execute this command:
```sh
sudo chmod +x /etc/rc.local
```

Now, we will add this service to system boot, so execute this:
```sh
sudo systemctl enable rc-local
```

And the output should look like this:
```sh
Created symlink from /etc/systemd/system/multi-user.target.wants/rc-local.service to /etc/systemd/system/rc-local.service.
```

At the end we need to start our service and check if this working
```sh
sudo systemctl start rc-local.service
sudo systemctl status rc-local.service
```
`sudo systemctl status rc-local.service` should return this:
```sh
● rc-local.service - /etc/rc.local Compatibility
 Loaded: loaded (/etc/systemd/system/rc-local.service; enabled; vendor preset: enabled)
 Active: active (running) since Fri 2015-11-27 00:32:56 CST; 14min ago
 Process: 879 ExecStart=/etc/rc.local start (code=exited, status=0/SUCCESS)
 Main PID: 880 (watch)
 CGroup: /system.slice/rc-local.service
```

It should work now.

## Known bugs
I don't know any bugs yet. :wink:
