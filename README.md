# LCD-odroid-status
Python script to show various info for Odroid C2 16x2 LCD screen

## Getting Started
Script support 5 different modes for output:

0. Multimode, cycle through all other modes
1. Show current ip address
2. Show hostname
3. Show load Average
4. Show current TIME

Modes can be switched by pressing buttons on 16x2 LCD Screen
Current mode is displayed by corresponding LED light(and you'll see a show message when pressing a button)

### Prerequisites

This script require module WiringPi2 for Pythong
```
https://github.com/Gadgetoid/WiringPi2-Python
```

### Installing

Clone and execute
```
git clone https://github.com/sbulav/lcd-odroid-status.git
cd lcd-odroid-status
sudo lcd-odroid-status &

```

### Starting as a systemd service

Copy python script to /usr/local/bin:
```
sudo cp lcd-odroid-status.py /usr/local/bin/lcd-odroid-status.py
```

Copy SystemD unit file to /etc/systemd/system:
```
sudo cp lcd-odroid-status.service /etc/systemd/system/
```

Load new unit file:
```
sudo systemctl daemon-reload
```

Start lcd-odroid-status and enable it if you'd like script to start at system boot:
```
sudo systemctl start lcd-odroid-status
sudo systemctl enable lcd-odroid-status 
```

Monitor status and errors:

```
systemctl status lcd-odroid-status
```

