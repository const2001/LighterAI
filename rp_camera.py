import picamera
import picamera.array
import numpy as np
from time import sleep
import datetime
from postgres import connectPostgressDatabase,getDbCursor



def main():
    conn = connectPostgressDatabase()
    curr = getDbCursor(conn)
    
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        with picamera.array.PiRGBArray(camera) as stream:
            camera.exposure_mode = 'auto'
            camera.awb_mode = 'auto'
            print("Initializing Pi Camera")
            sleep(2)
            rec = 0
            camera.exposure_mode = 'off'
            data = []
            while True:
                
                try:
                    camera.capture(stream, format='rgb')
                    # pixAverage = int(np.average(stream.array[...,1]))
                    pixAverage = np.average(stream.array[...,1])
                    
                    data.append(pixAverage,datetime.datetime.now())
                    print ("Light Meter pixAverage: {:.1f}".format(pixAverage))

                    sleep(1)
                    stream.truncate()
                    stream.seek(0)
                    rec = rec + 1
                    if rec == 50 :
                        for value in data:
                            curr.execute("INSERT INTO light_meter_average (average, reading_timestamp) VALUES (%s, %s)", value)
                        data = []
                        rec = 0
                except KeyboardInterrupt:
                    curr.close()
                    conn.close()
                    print("\nExiting ..")
                    break

if __name__ == "__main__": main()