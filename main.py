import thread;
import socket;
import json;
import serial
import imu

# ATTENTION!!! The '\n' at the end of each network message is extremely IMPORTANT!!!

# constants...
# HOST = '127.0.0.1'
# HOST = '192.168.0.20'
HOST = '0.0.0.0'
PORT_IN = 4243
PORT_OUT = 4242
CLIENT = '192.168.0.68'

# global set of registered listeners
listeners = set()


# call this method to send a 'notify' message for all registered listeners
def do_notify(data):
    print 'notify; data: ', data
    notify = {'type': 'NOTIFY', 'driver': 'org.unbiquitous.ubihealth.IMUDriver', 'eventKey': 'update'}
    notify['parameters'] = {'data': data}
    for listener in listeners:
        print 'notify ', listener, ';'
        c = socket.socket()
        c.connect(listener)
        c.send(json.dumps(notify) + '\n')
        c.close()


# service call handlers...
def get_euler_angles(service_call, caller, responseData):
    print 'get euler angles;'
    responseData['angles'] = '0,0,0,0'


def register_listener(service_call, caller, responseData):
    print 'register listener;'
    # replaces output port...
    listeners.add((caller[0], PORT_OUT))


# socket handlers...
def handle_incoming(conn, addr):
    # gets input message
    print 'msg received from: ', addr, ';'
    msg = conn.recv(1024)
    while not msg.endswith('\n'):
        msg = msg + con.recv(1024)
    print msg

    # extracts service name and prepares response
    call = json.loads(msg)
    service = call['service']
    response = {'type': 'SERVICE_CALL_RESPONSE'}
    responseData = dict()

    # handles the service call
    if service == 'getEulerAngles':
        get_euler_angles(call, addr, responseData)
    elif service == 'registerListener':
        register_listener(call, addr, responseData)

    # responds
    response['responseData'] = responseData
    conn.send(json.dumps(response) + '\n')
    conn.close()

    # this is just a notify test!!! remove it!!!
    register_listener(call, addr, responseData)
    do_notify('newdata')


def server():
    s = socket.socket()
    localep = (HOST, PORT_IN)
    s.bind(localep)
    s.listen(5)
    print 'listening on: ', localep, ';'
    while True:
        conn, addr = s.accept()
        thread.start_new_thread(handle_incoming, (conn, addr))


# starts listening...
register_listener(None, ('192.168.0.68', 4242), None)

serial_port = serial.Serial('COM10', timeout=1)
sensor3 = imu.IMU(serial_port, 3)
sensor2 = imu.IMU(serial_port, 2)

sensor3.startStreaming()
sensor2.startStreaming()

for i in range(0,2500):
    q = sensor2.listen_streaming()
    if q != None:
        response = {'sensor': q[0], 'quaternion': {'x': q[1], 'y': q[2], 'z': q[3], 'w': q[4]}}
        do_notify(response)

sensor2.stop_streaming()
sensor3.stop_streaming()

server()
