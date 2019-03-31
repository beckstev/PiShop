import time
import phue
from pprint import pprint

def get_IP(path_to_hue_ip):
    bridge_ip = 0
    with open(path_to_hue_ip, 'r') as f:
        bridge_ip = f.readline()[:-1]  # [:-1] to cut '\n'
    return bridge_ip


def connect(bridge_IP):
    bridge = phue.Bridge(bridge_IP)
    bridge.connect()
    return bridge


def on_off(bridge, lamp):
    # get_light returns a dict, 'on' is one key and represents the current
    # status of the bulb
    status = bridge.get_light(light_id=lamp, parameter='on')
    bridge.set_light(light_id=lamp, parameter='on', value=not status)


if __name__ == '__main__':
    hue_ip = get_IP('./hue_id.txt')
    bridge = connect(hue_ip)
    pprint(bridge.get_api())
    #on_off(bridge, lamp=2)
    #bridge.set_light(2, 'bri', 10)
    #time.sleep(1)
    #bridge.set_light(light_id=2, parameter='bri', value=254, transitiontime=6000)
