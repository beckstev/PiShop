import time
import os
import phue
import RPi.GPIO as GPIO
#  from pprint import pprint

#  def get_IP(path_to_hue_ip):
    #  bridge_ip = 0
    #  with open(path_to_hue_ip, 'r') as f:
        #  bridge_ip = f.readline()[:-1]  # [:-1] to cut '\n'
    #  return bridge_ip


#  def connect(bridge_IP):
    #  bridge = phue.Bridge(bridge_IP)
    #  bridge.connect()
    #  return bridge


#  def on_off(bridge, lamp):
    #  # get_light returns a dict, 'on' is one key and represents the current
    #  # status of the bulb
    #  status = bridge.get_light(light_id=lamp, parameter='on')
    #  bridge.set_light(light_id=lamp, parameter='on', value=not status)


def setup(GPIO_TRIGGER, GPIO_ECHO):
    # set pin notation (BOARD/BCM)
    GPIO.setmode(GPIO.BOARD)

    # set gpio direction (IN/OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)


if __name__ == '__main__':

    path = os.getcwd() + '/hue_id.txt'

    # set pin numbers
    GPIO_TRIGGER = 12
    GPIO_ECHO = 18

    setup(GPIO_TRIGGER, GPIO_ECHO)

    # connect to bridge
    try:
        hue_ip = get_IP(path)
        b = phue.Bridge(ip=hue_ip)
        b.connect()
    except IOError as ioerr:
        print(ioerr)  # file hue_id.txt does not exist
        exit()

    try:
        while True:
            # TODO
            time.sleep(1)
    except KeyboardInterrupt:
        print('Thanks for using phillips hue')
        GPIO.cleanup()


    #  pprint(b.get_api())
    b.set_light(light_id=2, parameter='on', value=True)
    b.set_light(2, 'bri', 254)  # brightness beween 0 and 254, note: 0 is not off
    time.sleep(2)
    b.set_light(light_id=2, parameter='bri', value=10, transitiontime=300)
    b.set_light(2, 'on', False)
