import serial
from typing import Union


port_name = "COM3"  # On Windows
baud_rate = 9600
try:
    ser = serial.Serial(port_name, baud_rate)
    SERIAL_OPEN = True
    print("Serial port " + port_name + " opened")
    print("Baudrate : " + str(baud_rate) + " Bd")
except Exception:
    SERIAL_OPEN = False
    print("WARNING: unable to open port "+port_name)


START_MARKER = ord('<')
END_MARKER = ord('>')


def with_serial(func):
    def func_wrapper(*args):
        if SERIAL_OPEN:
            return func(*args)
        else:
            print("WARNING: no connection with Arduino")
    return func_wrapper


@with_serial
def _recvFromArduino():
    """
    Read on serial until message with start marker and end marker is found

    """
    msg = ""
    current_char = ser.read()

    # Wait for the start character
    while ord(current_char) != START_MARKER:
        current_char = ser.read()
    current_char = ser.read()  # current_char is the first caracter after the start character

    # Save data until the end marker is found
    while ord(current_char) != END_MARKER:
        msg = msg + current_char.decode("utf-8")
        current_char = ser.read()

    return msg


@with_serial
def waitArduinoSetup():
    """
    Wait until the Arduino sends 'Arduino Ready' - allows time for Arduino reset
    It also ensures that any bytes left over from a previous message are discarded

    """

    msg = ""
    while msg.find("Arduino is ready") == -1:

        while ser.inWaiting() == 0:
            pass

        msg = _recvFromArduino()
        print(msg)


@with_serial
def sendToArduino(msg: str):
    """
    Send message to Arduino and wait for the answer

    Return: the answer message

    """
    ser.write(msg.encode('utf-8'))
    answer = _recvFromArduino()
    return answer


def _check_pos(pos):
    if not isinstance(pos, str) and not isinstance(pos, int):
        raise TypeError("int or str of an int is expected")
    try:
        int(pos)
    except Exception:
        raise TypeError("int or str of an int is expected")


@with_serial
def sendPosToArduino(pos: list[Union[int, str]]):
    """
    Send new servo position message

    Return: the answer message

    """
    msg = "<"
    for i in range(len(pos)):
        _check_pos(pos[i])
        msg += str(pos[i])+","
    msg = msg[:-1] + ">"
    return sendToArduino(msg)
