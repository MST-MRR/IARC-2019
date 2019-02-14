import serial

class serialController:
""" A controller to simplify the connection of the Serial port as well as simplifying sending the commands
Parameters
----------
port_string : string
    The string of the serial port you want to open (for ardunio it has been "dev/ttyACM0")
baudrate : int
    The baudrate for the serial port (for arduino probably 9600 is standard)

Methods
-------
write_to(self,cmdString)
    Simplifies the sending of commands via Serial connection
"""
    def __init__(self,port_string,baudrate):
        self.ser = serial.Serial(port_string,baudrate)

    def write_to(self,cmdString):
        """
        Writes the given string command to the Serial Connection

        Parameters
        ----------
        cmdString : str
            The string command that you want to send over Serial
        """
        self.ser.write(cmdString.encode())

