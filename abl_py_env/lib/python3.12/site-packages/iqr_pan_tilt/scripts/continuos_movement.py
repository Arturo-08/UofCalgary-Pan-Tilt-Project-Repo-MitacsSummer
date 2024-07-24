import time
from iqr_pan_tilt.pan_tilt_driver import PanTiltDriver

def continuous_movement(yaw, speed, pitch_min, pitch_max, rate_hz):
    pitch = pitch_min
    direction = 1  # 1 for increasing, -1 for decreasing
    interval = 1.0 / rate_hz

    with PanTiltDriver(start_identity=False, end_identity=False) as driver:
        while True:
            driver.set_pan(yaw, speed)
            driver.set_tilt(pitch, speed)
            
            print("Current Yaw: {}, Pitch: {}, Speed: {}".format(yaw, pitch, speed))
            
            pitch += direction * speed / rate_hz

            # Reverse direction at limits
            if pitch >= pitch_max:
                direction = -1
            elif pitch <= pitch_min:
                direction = 1

            time.sleep(interval)

if __name__ == '__main__':
    try:
        while True:
            yaw = float(input("Input the yaw value (-55 to 55) Set -16.0 to align the platform well: "))
            if(yaw > 55 or yaw < -55 or not yaw):
                print("Invalid yaw value. Try again.")
            else:
                break

        while True:
            speed = float(input("Input the speed value 1 (min) - 30 (max):  "))
            if(speed > 30 or speed < 1 or not speed):
                print("Invalid speed value. Try again.")
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
            rate_hz = float(input("Input cycles frequency (greater than 0 Hz): "))
            if(rate_hz < 0 or not rate_hz):
                print("Invalid cycles frequency value. Try again.")
            else:
                break
        continuous_movement(yaw, speed, pitch_min, pitch_max, rate_hz)        
    except KeyboardInterrupt:
        print("Disrupted by user")
