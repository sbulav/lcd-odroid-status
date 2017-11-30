#!/usr/bin/python

import wiringpi2
import subprocess
from time import localtime, strftime, sleep
from threading import Timer

##############################################################################################
#        INITIALIZATION                                                                      #
##############################################################################################
LCD_ROW = 2 # 16 Char
LCD_COL = 16 # 2 Line
LCD_BUS = 4 # Interface 4 Bit mode

PORT_LCD_RS = 7 # GPIOY.BIT3(#83)
PORT_LCD_E = 0 # GPIOY.BIT8(#88)
PORT_LCD_D4 = 2 # GPIOX.BIT19(#116)
PORT_LCD_D5 = 3 # GPIOX.BIT18(#115)
PORT_LCD_D6 = 1 # GPIOY.BIT7(#87)
PORT_LCD_D7 = 4 # GPIOX.BIT4(#104)

PORT_BUTTON1 = 5
PORT_BUTTON2 = 6


wiringpi2.wiringPiSetup() # Initialize values for pin numbering

lcdHandle = wiringpi2.lcdInit(LCD_ROW, LCD_COL, LCD_BUS, # Main initialization function
PORT_LCD_RS, PORT_LCD_E,
PORT_LCD_D4, PORT_LCD_D5,
PORT_LCD_D6, PORT_LCD_D7, 0, 0, 0, 0);
lcdRow = 0 # LCD Row
lcdCol = 0 # LCD Column


# Working with LEDs
ledPorts = [ 21, 22, 23, 24, 11, 26, 27 ]
PUD_UP = 2 # Set pull-up resistor mode
INPUT = 0 # We use 0 for input 
OUTPUT = 1 # We use 1 for output 

# GPIO Init(Set resistor mode of ALL LED port to Output)
for led in ledPorts:
    wiringpi2.pinMode(led, OUTPUT)

# GPIO Init(Set resistor mode of Button 1 and 2 to input, enable Pull Up mode)
wiringpi2.pinMode(PORT_BUTTON1, INPUT )
wiringpi2.pullUpDnControl(PORT_BUTTON1, PUD_UP)
wiringpi2.pinMode(PORT_BUTTON2, INPUT )
wiringpi2.pullUpDnControl(PORT_BUTTON2, PUD_UP)
for led in ledPorts: # Turn off all LEDs
    wiringpi2.digitalWrite(led,0)

##############################################################################################
#        TIMER WITH ABILITY TO STOP                                                          #
##############################################################################################

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

##############################################################################################
#        DRAW LINE1 and LINE2 to LCD                                                         #
##############################################################################################

def draw_lcd(lcd_line1, lcd_line2):
    wiringpi2.lcdClear(lcdHandle)
    wiringpi2.lcdPosition(lcdHandle, lcdCol, lcdRow)
    wiringpi2.lcdPrintf(lcdHandle, lcd_line1)
    wiringpi2.lcdPosition(lcdHandle, lcdCol, lcdRow + 1)
    wiringpi2.lcdPrintf(lcdHandle, lcd_line2)
##############################################################################################
#        Run OS command and return its output                                                #
##############################################################################################

def run_cmd(cmd):
    # runs whatever is in the cmd variable in the terminal
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output = p.communicate()[0]
    return output

##############################################################################################
#        GET IP                                                                              #
##############################################################################################

def get_ipaddr():
    cmd = "ifconfig eth0 | grep 'inet addr' | cut -d ':' -f2 | cut -d ' ' -f1"
    ipaddr = run_cmd(cmd)[:-1] # set output of command into ipaddr variable
    return ipaddr

##############################################################################################
#        GET HOSTNAME                                                                        #
##############################################################################################

def get_hostname():
    cmd_hostname = "hostname -s"
    hostname = run_cmd(cmd_hostname)[:-1]
    return hostname

##############################################################################################
#        GET LOADAVG                                                                         #
##############################################################################################

def get_load():
    cmd_loadavg = "cat /proc/loadavg"
    loadavg = run_cmd(cmd_loadavg)[:-11]
    return loadavg


##############################################################################################
#        CALCULATE WORKING MODE                                                              #
##############################################################################################

def change_mode(mode, change_val):
    if mode == 0 and change_val == -1: # if mode is 0 and left btn pressed
        mode = 4
    elif mode == 4 and change_val == 1: # if mode is 4 and right btn pressed
        mode = 0
    else:
         mode = mode + change_val
    return mode

##############################################################################################
#        DRAW BUTTON PRESS                                                                   #
##############################################################################################

def draw_button_press(mode,change_val):
#    print "PORT_BUTTON1: " + str(is_button1_pressed)
#    print "PORT_BUTTON2: " + str(is_button2_pressed)
    mode = change_mode(mode, change_val) # Calculate working mode after BTN PRESS
    if change_val == -1:
        lcd_line1 = ' LEFT BTN PRESSED'
    elif change_val == 1:
        lcd_line1 = ' RIGHT BTN PRESSED'
    else:
        lcd_line1 = ' NO BTN PRESSED '
    lcd_line2 = 'MODE CHG TO: ' + str(mode)
    draw_lcd( lcd_line1, lcd_line2)
    for led in ledPorts:    #turn off all lights
        wiringpi2.digitalWrite(led,0)
    wiringpi2.digitalWrite(ledPorts[mode],1) #turn on led corresponding to mode
    sleep(2)
    return mode

##############################################################################################
#        DRAW IP ADDRESS                                                                     #
##############################################################################################

def draw_ip():
    lcd_line1 = 'IPADDR:'
    lcd_line2 = ipaddr
    draw_lcd( lcd_line1, lcd_line2)

##############################################################################################
#        DRAW HOSTNAME                                                                       #
##############################################################################################

def draw_hostname():
    lcd_line1 = 'HOSTNAME:'
    lcd_line2 = hostname
    draw_lcd( lcd_line1, lcd_line2)

##############################################################################################
#        DRAW LOADAVG                                                                        #
##############################################################################################

def draw_loadavg():
    lcd_line1 = 'Load average:'
    lcd_line2 = get_load()
    draw_lcd( lcd_line1, lcd_line2)

##############################################################################################
#        DRAW TIME                                                                           #
##############################################################################################

def draw_time():
    lcd_line1 = ' TIME: '
    lcd_line2 = strftime("%d-%m-%Y %H:%M", localtime())
    draw_lcd( lcd_line1, lcd_line2)

##############################################################################################
#        DRAW MULTIPLE MODES THOUGH CYCLE                                                    #
##############################################################################################
def draw_multimode():
    curtime = strftime('%S')
    if 0 <= int(curtime) <=10 :
        draw_ip()
    elif 11 <= int(curtime) <=20 :
        draw_hostname()
    elif 21 <= int(curtime) <=40 :
        draw_loadavg()
    elif 31 <= int(curtime) <=60 :
        draw_time()

##############################################################################################
#        INITIALIZE ONE-TIME OS PARAMETERS                                                   #
##############################################################################################

hostname = get_hostname()
ipaddr = get_ipaddr()
mode = 1 # 0 - cycle through all modes, 1 - ip, 2 - hostname, 3 - load average, 4 - time
change_val = 0 # Value to change mode

rt = RepeatedTimer(2, draw_multimode) #Start drawing multimode on begin

##############################################################################################
#        MAIN CYCLE                                                                          #
##############################################################################################

while True:

    is_button1_pressed = wiringpi2.digitalRead(PORT_BUTTON1)  # Check is Left BTN Pressed
    is_button2_pressed = wiringpi2.digitalRead(PORT_BUTTON2)  # Check if Right BTN Pressed

    if not is_button1_pressed: # Decide in which direction to change current mode
        change_val = -1
    elif not is_button2_pressed:
        change_val = 1
    else:
        change_val = 0
    # test only
#    curtime = strftime('%S')
#    if curtime == '30' or curtime == '00':
#        change_val = 1
#    else:
#        change_val = 0
    if change_val != 0: # If button was pressed and we have to change current working mode
        mode = draw_button_press(mode, change_val)   # Draw which button was pressed
        try:
            rt.stop()  # Stop timer if if was running
        except:
            pass
        finally:
            if mode == 0: # Multimode
                rt = RepeatedTimer(2, draw_multimode) # Start timer which will draw multimode every 2 sec
            elif mode == 1: # IP Address
                draw_ip()
            elif mode == 2: # Hostname
                draw_hostname()
            elif mode == 3: # Load Average
                draw_loadavg()
                rt = RepeatedTimer(5, draw_loadavg)
            elif mode == 4: # Time
                draw_time()
                rt = RepeatedTimer(60, draw_time)
    else:
        sleep(0.5) # don't abuse CPU
