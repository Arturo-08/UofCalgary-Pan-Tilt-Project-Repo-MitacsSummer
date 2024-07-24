import time
from iqr_pan_tilt.pan_tilt_driver import PanTiltDriver

def continuous_movement(yaw, pitch_min, pitch_max, total_time_minutes):

    total_pitch_change = abs((pitch_max - pitch_min)) * 2
    total_time_seconds = 60 * total_time_minutes

    pitch_change_per_update = total_pitch_change / total_time_seconds
    if pitch_change_per_update < 0.05:
        pitch_change_per_update = 0.05
        
    total_updates = total_pitch_change / pitch_change_per_update

    interval = total_time_seconds / total_updates
    rate_hz = 1/interval

    speed = pitch_change_per_update / interval
    if speed < 1 or speed > 30:
        print(f"Calculated speed {speed} °/s out of range allowed. Setting the speed to nearest value allowed...")
        speed = max(1, min(speed, 30))  # Ajusta la velocidad dentro del rango permitido
    
    pitch = pitch_min
    direction = 1  # 1 for increasing, -1 for decreasing

    print(f"Speed Calculated: {speed}°/s, Frecuency: {rate_hz} Hz, Total time per cycle: {total_time_minutes} min.")
    print(f"{pitch_change_per_update},{total_updates},{interval},{speed}")
    with PanTiltDriver(start_identity=False, end_identity=False) as driver:
        while True:
            driver.set_pose(int(yaw), int(pitch), int(speed))
            
            print("Current Yaw: {}, Pitch: {}, Speed: {}".format(yaw, pitch, speed))
            
            pitch += direction * pitch_change_per_update

            # Reverse direction at limits
            if pitch >= pitch_max:
                direction = -1
            elif pitch <= pitch_min:
                direction = 1

            time.sleep(interval)

if __name__ == '__main__':
    try:
        while True:
            yaw = float(input("Input the yaw value (-44 to 60) Set -18.0 to align the platform well: "))
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
            total_time_cycle = float(input("Input total time of the cycle in minutes: "))
            if(total_time_cycle < 0 or not total_time_cycle):
                print("Invalid cycle time. Try again.")
            else:
                break
        continuous_movement(yaw, pitch_min, pitch_max, total_time_cycle)        
    except KeyboardInterrupt:
        print("Disrupted by user")
