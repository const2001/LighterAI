from yeelight import Bulb,discover_bulbs

def get_local_bulbs():
    return discover_bulbs()

def turn_on_bulb(ip):
    bulb = Bulb(ip,auto_on=True)
    bulb.turn_on()

def turn_off_bulb(ip):
    bulb = Bulb(ip)
    bulb.turn_off()    
def setBrightness(ip,lvl):
    bulb = Bulb(ip,auto_on=True)
    bulb.set_brightness(lvl)

    
if __name__ == "__main__":
    turn_on_bulb('192.168.2.209')
 