import time
from iqr_pan_tilt.pan_tilt_driver import PanTiltDriver

def slowly_movement(rate_hz=0.33333334):
    yaw = -18.0
    speed = 1
    pitch_min = -15.0
    pitch_max = 15.0
    pitch = pitch_min
    direction = 1  # 1 for increasing, -1 for decreasing
    interval = 1.0 / rate_hz

    with PanTiltDriver(start_identity=False, end_identity=False) as driver:
        while True:
            driver.set_pose(int(yaw), int(pitch), int(speed))
            
            print("Current Yaw: {}, Pitch: {}, Speed: {}".format(yaw, pitch, speed))
            
            pitch += direction * 0.05

            # Reverse direction at limits
            if pitch >= pitch_max:
                direction = -1
            elif pitch <= pitch_min:
                direction = 1

            time.sleep(interval)

if __name__ == '__main__':
    try:
        slowly_movement()
    except KeyboardInterrupt:
        print("Disrupted by user")
