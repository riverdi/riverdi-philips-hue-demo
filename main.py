import streams
import json
import requests
import mcu
import pwm

from wireless import wifi
from espressif.esp32net import esp32wifi as wifi_driver

from riverdi.displays.bt81x import ctp50
from bridgetek.bt81x import bt81x

from okdo.iot import iot
from okdo.iot import mqtt_client

import gui
import hue

# image resources
new_resource('images/gui_riverdi_logo.png')
new_resource('images/gui_addr_hue.png')
new_resource('images/gui_auth_hue.png')
new_resource('images/gui_menu_bar.png')

# wifi credentials
ssid = "ssid"                  # this is the SSID of the WiFi network
wifiPWD = "password"           # this is the Password for WiFi

# okdo cloud
device_id = "okdoID"          # this is the device identifier. Can be obtained from the OKDO cloud dashboard
device_token = "maker:token"  # this is the device token. Can be obtained from the OKDO cloud dashboard

# hue credentials
hueIP = '192.168.0.59'
hueUSER = ''

# hue devices status
bulb_1_old_value = False
bulb_1_new_value = False
bulb_2_old_value = False
bulb_2_new_value = False

saturation_new_value = 0
hue_new_value = 0
brightness_new_value = 0

saturation_old_value = 0
hue_old_value = 0
brightness_old_value = 0

# screen layouts/stages:
# 1 - connectig with WiFi spinner
# 2 - entering HUE Bridge IP
# 3 - spinner (looking for HUE Bridge)
# 4 - spinner (creating new user)
# 5 - authentication
# 6 - spinner (entering to mainmenu)
# 7 - mainmenu
screenLayout = 0

 # open serial channel to display debug messages
streams.serial()

# pwm buzzer
pinMode(D23.PWM,OUTPUT)

# short beep
def beep():
    pwm.write(D23.PWM,1000,1000//2,MICROS)
    sleep(50)
    pwm.write(D23.PWM,0,0)

# okDO handlers
def bulb_1_cb(asset,value, previous_value):
    global bulb_1_new_value
    bulb_1_new_value = value

def bulb_2_cb(asset,value, previous_value):
    global bulb_2_new_value
    bulb_2_new_value = value

# buttons handler
def pressed(tag, tracked, tp):

    # entering HUE IP
    if (screenLayout == 2):

        global hueIP
        global screenLayout

        # emit sound
        beep()

        # remove last character
        if (tag != 67):

            # max length of IP
            if len(hueIP) >= 15:
                return

            hueIP = hueIP + str(chr(tag))

        else:
            if len(hueIP) > 0:
                hueIP = hueIP[:-1]

        # connect -> go to next screen
        if (tag == 1):
            hueIP = hueIP[:-1]
            screenLayout = 3

    # mainmenu screen
    elif (screenLayout == 7):

        global bulb_1_new_value
        global bulb_2_new_value

        # on/off switching
        if (tag == 2):
            bulb_1_new_value = True
        elif (tag == 3):
            bulb_1_new_value = False
        elif (tag == 4):
            bulb_2_new_value = True
        elif (tag == 5):
            bulb_2_new_value = False
        elif (tag == 6):
            if (saturation_new_value  > 0):
                saturation_new_value -= 24
        elif (tag == 7):
            if (hue_new_value  > 0):
                hue_new_value -= 6550
        elif (tag == 8):
            if (brightness_new_value  > 0):
                brightness_new_value -= 24
        elif (tag == 9):
            if (saturation_new_value < 240):
                saturation_new_value += 24
        elif (tag == 10):
            if (hue_new_value < 65500):
                hue_new_value += 6550
        elif (tag == 11):
            if (brightness_new_value < 240):
                brightness_new_value += 24

# init display
bt81x.init(SPI0, D4, D33, D34)

# one callback for all tags
bt81x.touch_loop(((-1, pressed), ))

# [0] show logo
gui.loadImage('gui_riverdi_logo.png')
gui.showLogo()
sleep(4000)

# [1] show spinner - connecting with predefined WiFi network
screenLayout = 1
gui.showSpinner("Connecting with predefined WiFi network...")

# [2] init wifi driver
wifi_driver.auto_init()

# [3] connect to predefined wifi network
for _ in range(0,5):
    try:
        wifi.link(ssid,wifi.WIFI_WPA2,wifiPWD)
        break
    except:
        gui.showSpinner("Trying to reconnect...")
else:
    gui.showSpinner("Connection Error - restarting...")
    mcu.reset()

# [4] connect and setup connection with OKdo cloud
device = iot.Device(device_id,device_token,mqtt_client.MqttClient)
device.connect()

# [5]  check HUE Bridge availability - loop till we get connection
gui.loadImage('gui_addr_hue.png')
while True:

    # enter IP address of HUE gateway
    screenLayout = 2
    while (screenLayout == 2):
        gui.showAddrScreen(hueIP)

    # show spinner (looking for HUE)
    screenLayout = 3
    gui.showSpinner("Looking for HUE Bridge...")

    # check HUE availability
    status = hue.testConnection(hueIP)
    if (status):
        break;

# [6] authentication - if hueUSER is not set - create new one
screenLayout = 4
gui.showSpinner("Creating new user...")
gui.loadImage('gui_auth_hue.png')
while True:

    # show authScreen
    screenLayout = 5
    gui.showAuthScreen()

    # check status
    username = hue.createUser(hueIP)
    if (username):
        # todo save user and password to flash
        break;

# [7] entering to mainmenu
screenLayout = 6
gui.showSpinner("Starting MainMenu...")

# [8] define the callbacks to call when an OKdo asset command is received
device.watch_command("Switch-Kitchen", bulb_1_cb)
device.watch_command("Switch-Bedroom", bulb_2_cb)
device.run()

# [9] mainloop
screenLayout = 7
gui.loadImage('gui_menu_bar.png')

while True:

    gui.showMainMenu(saturation_old_value, hue_old_value, brightness_old_value)

    if (bulb_1_new_value != bulb_1_old_value):
        beep()
        hue.turnLight(hueIP, username ,"4", bulb_1_new_value)
        device.publish_asset("Kitchen", bulb_1_new_value)
        bulb_1_old_value = bulb_1_new_value

    if (bulb_2_new_value != bulb_2_old_value):
        beep()
        hue.turnLight(hueIP, username ,"2", bulb_2_new_value)
        device.publish_asset("Bedroom", bulb_2_new_value)
        bulb_2_old_value = bulb_2_new_value

    if (saturation_new_value != saturation_old_value):
        beep()
        hue.changeColor(hueIP, username ,"3", True, saturation_new_value, brightness_new_value, hue_new_value)
        saturation_old_value = saturation_new_value

    if (hue_new_value != hue_old_value):
        beep()
        hue.changeColor(hueIP, username ,"3", True, saturation_new_value, brightness_new_value, hue_new_value)
        hue_old_value = hue_new_value

    if (brightness_new_value != brightness_old_value):
        beep()
        hue.changeColor(hueIP, username ,"3", True, saturation_new_value, brightness_new_value, hue_new_value)
        brightness_old_value = brightness_new_value
