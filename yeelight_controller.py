from yeelight import Bulb,discover_bulbs

def get_local_bulbs():
    return discover_bulbs()

def turn_on_bulb(ip):
    bulb = Bulb(ip,auto_on=True)
    bulb.turn_on()

def turn_off_bulb(ip):
    bulb = Bulb(ip)
    bulb.turn_off()    

def set_brightness(ip,lvl):
    bulb = Bulb(ip,auto_on=True)
    bulb.set_brightness(lvl)

def get_properties(ip):
    bulb = Bulb(ip)
    return bulb.get_properties 

    
if __name__ == "__main__":
   print(get_local_bulbs())
 