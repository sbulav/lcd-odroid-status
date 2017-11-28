# LCD-odroid-status
Python script to show some system info for Odroid C2 16x2 LCD screen

## Getting Started
Script support 5 different modes for output:
0 - Multimode, cycle through all other modes
1 - Show current ip address
2 - Show hostname
3 - Show load Average
4 - Show current TIME

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

