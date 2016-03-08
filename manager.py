import math
import serial
import imu
import stimulator
import thread
import time
import control

# ref = 1.5
# current_biceps = 2 #6
# current_triceps = 2 #6

def main():
    # serial_port = serial.Serial('COM10', timeout=1)
    sensor2.calibrate()
    sensor2.tare()
    sensor2.reset_timestamp()
    sensor2.startStreaming()

    # stim.initialization(50,3)
    data = ''
    error = []
    while running:
        q = sensor2.listen_streaming()
        if q != None:
            response = {'sensor': q[0], 'quaternion': {'x': q[1], 'y': q[2], 'z': q[3], 'w': q[4]}, 'timestamp': q[5]}
            print response.get('quaternion')
        # data = sensor2.getEulerAngles()
        # data = data.split(',')
        # if len(data) > 3:
        #     ang = data[4]
        #     e = ref - float(ang)
        #     error.append(e)
        #     c = control.control_signal(error)
        #     # print ang
        #     print c
        #     if c > 0:
        #         stim.update(3,[c,0],[current_biceps,current_triceps])
        #     else:
        #         stim.update(3,[0,-c],[current_biceps,current_triceps])


serial_port = serial.Serial(imu.get_port(),timeout=1,baudrate=115200)
# stim_port = serial.Serial(stimulator.get_port(), timeout=1, baudrate=115200)

sensor2 = imu.IMU(serial_port, 2)
# stim = stimulator.Stimulator(stim_port)

running = True
t = thread.start_new_thread(main,())
i = raw_input('Parar?')
running = False
time.sleep(0.5)
# stim.stop()
# sensor2.stop_streaming()
# sensor2.stop_streaming()

serial_port.close()
# stim_port.close()

print 'adeus'