#!/bin/bash

#Path to directory
cd ~/ros_python/Pan-Tilt-UofC-Python-Project

#Activate virtual python  environment 

source abl_py_env/bin/activate

#Run python script
python ~/ros_python/Pan-Tilt-UofC-Python-Project/src/iqr_pan_tilt/scripts/continuos_movement.py
