from yeelight import Bulb

def turn_on_bulb(ip):
    bulb = Bulb(ip)
    bulb.turn_on()

def turn_off_bulb(ip):
    bulb = Bulb(ip)
    bulb.turn_off()    


    
if __name__ == "__main__":
    turn_on_bulb('192.168.2.209')
 