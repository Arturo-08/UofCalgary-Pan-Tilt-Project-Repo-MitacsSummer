import time
import datetime as dt
from iqr_pan_tilt.pan_tilt_driver import PanTiltDriver

def continuous_movement(yaw, pitch_min, pitch_max, speed, delayTimeMovement):
    
    pitch = pitch_min
    current_date = dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    initial_delay_flag = True
    with PanTiltDriver(start_identity=False, end_identity=False) as driver:
        print(f"Start datetime: {current_date}")
        while True:
            if(initial_delay_flag):
                driver.set_pose(int(yaw), int(pitch), 10)
                initial_delay_flag = False
                print("Setting to initial position...")
                time.sleep(2*(abs(pitch)/10))
            else:
                driver.set_pose(int(yaw), int(pitch), int(speed))
            
                print("Current Yaw: {}, Pitch: {}, Speed: {}".format(yaw, pitch, speed))

                # Reverse direction at limits
                if pitch == pitch_max:
                    pitch = pitch_min
                elif pitch == pitch_min:
                    pitch = pitch_max
                time.sleep(delayTimeMovement)

if __name__ == '__main__':
    try:
        while True:
            yaw = float(input("Input the yaw value (-44 to 60) Set -10.0 to align the platform well: "))
            if(yaw > 60 or yaw < -44 or not yaw):
                print("Invalid yaw value. Try again.")
            else:
                break

        while True:
            pitch_min = float(input("Input minimum pitch value (-60 min):  "))
            if(pitch_min > 60 or pitch_min < -60 or not pitch_min):
                print("Invalid minimum pitch value. Try again.")
            else:
                break

        while True:
            pitch_max = float(input("Input maximum pitch value (60 max): "))
            if(pitch_max > 60 or pitch_max < -60 or not pitch_max):
                print("Invalid maximum pitch value. Try again.")
            else:
                break

        while True:
            delayTimeMovement = float(input("Input delay time in seconds: "))
            if(delayTimeMovement < 0 or not delayTimeMovement):
                print("Invalid delay time. Try again.")
            else:
                break

        while True:
            speed = float(input("Input speed (1°/s min to 30°/s max): "))
            if(speed < 1 or  speed > 30 or not speed):
                print("Invalid speed. Try again.")
            else:
                break
        continuous_movement(yaw, pitch_min, pitch_max, speed, delayTimeMovement)        
    except KeyboardInterrupt:
        print("Disrupted by user")
