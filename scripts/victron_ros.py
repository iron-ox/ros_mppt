#!/usr/bin/env python

"""
    This file is part of ros_mppt.
    ros_mppt is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.
    ros_mppt is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with ros_mppt.  If not, see <https://www.gnu.org/licenses/>.
"""


import rospy
import time
import serial
import logging
from ros_mppt.msg import batt

logging.basicConfig(level=logging.INFO, filename='ros_mppt.log', filemode='a', format='[%(asctime)s - %(levelname)s]: %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logging.info('Initializing ros_mppt package...')

def sender():
    pub = rospy.Publisher('batt_channel', mppt, queue_size=10)
    rospy.init_node('ros_batt', anonymous=True)
    r = rospy.Rate(10)
    msg = batt()

    #Predefined values of msg
    msg.v_bat = -1
    msg.i_bat = -1
    msg.p_batt = -1
    msg.ce_batt = -1
    msg.soc_batt = -1
    msg.ttg_batt = -1

    while not rospy.is_shutdown():

        try:
            batt_read = ser.readline().decode("utf-8")
            batt_split = batt_read.split("\t")
        except: logging.warning('Skipping decoding from batt_read line: ' + batt_read)

        param = batt_split[0]

        if param == "V":  # Volts
            try:
                msg.v_bat = float(batt_split[1]) * 0.001
            except Exception as e:
                logging.error('Skipping voltage decode from gauge_read', exc_info=True)
        elif param == "I":  # Amps
            try:
                msg.i_bat = float(batt_split[1]) * 0.001
            except Exception as e:
                logging.error('Skipping amperage decode from gauge_read', exc_info=True)
        elif param == "P":  # Watts
            try:
                msg.p_batt = float(batt_split[1])
            except Exception as e:
                logging.error('Skipping power decode from gauge_read', exc_info=True)
        elif param == "CE":  # Ah consumed
            try:
                msg.ce_batt = float(batt_split[1])
            except Exception as e:
                logging.error('Skipping Ah decode from gauge_read', exc_info=True)
        elif param == "SOC":  # % SoC
            try:
                msg.soc_batt = float(batt_split[1])
            except Exception as e:
                logging.error('Skipping SoC decode from gauge_read', exc_info=True)
        elif param == "TTG":  # Time to go
            try:
                msg.ttg_batt = float(batt_split[1])
            except Exception as e:
                logging.error('Skipping TTG decode from gauge_read', exc_info=True)

        rospy.loginfo(msg)
        pub.publish(msg)
        r.sleep()

if __name__ == '__main__':
    try:
        ser = serial.Serial('/dev/ttyUSB0', 19200, timeout=10)
        sender()
    except rospy.ROSInterruptException: pass
    finally:
        ser.close()
