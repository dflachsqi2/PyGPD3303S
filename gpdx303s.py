"""
This is some dope code for the GW INSTEK GPD-x303S.
"""
import time
try:
    from rich import print
except:
    pass

try:
    from exceptions import RuntimeError, ImportError
except:
    pass
import serial
import sys

'''
class MySerial(serial.Serial):
    """
    Wrapper for Serial
    """
    try:
        import io
    except ImportError:
        # serial.Serial inherits serial.FileLike
        pass
    else:
        def readline(self, eol=b'\r'):
            """
            Overrides io.RawIOBase.readline which cannot handle with '\r' delimiters
            """
            leneol = len(eol)
            ret = b''
            while True:
                c = self.read(1)
                if c:
                    ret += c
                    if ret[-leneol:] == eol:
                        break
                else:
                    break

            return ret

'''

class GPDX303S(object):
    def __init__(self, port=""):
        self.__baudRate = 9600 # 9600 bps
        self.__parityBit = 'N' # None
        self.__dataBit = 8
        self.__stopBit = 1
        self.__dataFlowControl = None
        self.eol = b'\r'
        self.supported = [
                { "model": "GPD-4303S", "nchannels": 4 }, 
                { "model": "GPD-3303S", "nchannels": 2 }, 
                { "model": "GPD-2303S", "nchannels": 2 }] 
        self.model = {}
        self.channels = []
        if port:
            self.open(port)
    def getline(self):
        try:
            l = self.serial.readline().decode('utf-8').strip()
        except:
            print("something went wrong with readline()")
            l = ''
        self.checkError()
        return l

    def open(self, port, readTimeOut = 1, writeTimeOut = 1):
        # self.serial = MySerial(port         = port,
        self.serial = serial.Serial(port         = port,
                               baudrate     = self.__baudRate,
                               bytesize     = self.__dataBit,
                               parity       = self.__parityBit,
                               stopbits     = self.__stopBit,
                               timeout      = readTimeOut,
                               writeTimeout = writeTimeOut,
                               dsrdtr       = self.__dataFlowControl)
        # self.checkError()
        self.setRemoteMode()
        self.setTimeout(0.1)

        # ret = self.serial.read(1)
        # self.setTimeout(readTimeOut)
        # if ret == b'\n':
        #     self.setDelimiter(b'\r\n')

        idstr = self.getIdentification()
        for s in self.supported:
            for k,v in s.items():
                if "model" == k:
                    if v in idstr:
                        self.model = s
        if self.model is not {}:
            print(f"Found supported model {self.model['model']}")
            self.channels = [c+1 for c in range(0,self.model['nchannels'])]
            # self.printHelp()
        else:
            print("Didn't find a supported model")
            self.close() 
         

    def close(self):
        self.setLocalMode()
        self.serial.close()

    def setDelimiter(self, eol = b'\r\n'):
        """
        Must call this method for new-firmware (2.0 or above?) instruments.
        Because the delimiter setting has been changed. 
        """
        self.eol = eol

    def setTimeout(self, timeout):
        if hasattr(self.serial, 'setTimeout') and \
           callable(getattr(self.serial, 'setTimeout')):
            # pySerial <= v2.7
            self.serial.setTimeout(timeout)
        else:
            # pySerial v3
            self.serial.timeout = timeout

    def isValidChannel(self, channel):
        return channel in self.channels
        # if channel not in self.channels:
        #     raise RuntimeError('Invalid channel number: %d was given.' % channel)
        # return True

    def isValidMemory(self, memory):
        """
        Check if the given memory number is valid or not. Only memory 1 to 2
        are allowed.
        """
        if not (memory <= 0 or 4 < memory):
            raise RuntimeError('Invalid memory number: %d was given.' % memory)

        return True

    def isValidFloat(self, value):
        """
        Check if the given float number is valid or not. Three or less
        significant figures are allowed.
        """
        if value < 0:
            raise RuntimeError('Invalid float value: %f was given.' % value)
        
        str = "%f" % value
        position = str.find(".")
        maxDigits = 5
        if 0 <= position and position <= maxDigits : # found
            str = str[0:maxDigits + 1]
        else: # not found
            str = str[0:maxDigits]

        if float(str) != value:
            sys.stderr.write('Invalid float value: %f was given.' % value)
            return False
        
        return True

    def setCurrent(self, channel, current):
        """
        ISET<X>:<NR2>
        """
        self.isValidChannel(channel)
        self.serial.write(b'ISET%d:%.3f\n' % (channel, current))
        self.checkError()
        
    def getCurrent(self, channel):
        """
        ISET<X>?
        """
        self.isValidChannel(channel)
        self.serial.write(b'ISET%d?\n' % channel)
        ret = self.getline() # self.serial.readline() #eol=self.eol)
        return float(ret.replace('A', ''))

    def setVoltage(self, channel, voltage):
        """
        VSET<X>:<NR2>
        """
        self.isValidChannel(channel)
        self.serial.write(b'VSET%d:%.3f\n' % (channel, voltage))
        self.checkError()
        
    def getVoltage(self, channel):
        """
        VSET<X>?
        """
        self.isValidChannel(channel)
        self.serial.write(b'VSET%d?\n' % channel)
        ret = self.getline() # self.serial.readline() #eol=self.eol)
        return float(ret.replace('V', ''))

    def getCurrentOutput(self, channel):
        """
        IOUT<X>?
        """
        self.isValidChannel(channel)
        self.serial.write(b'IOUT%d?\n' % channel)
        ret = self.getline() # self.serial.readline() #eol=self.eol)
        # print(ret)
        return float(ret.replace('A',''))

    def getVoltageOutput(self, channel):
        """
        VOUT<X>?
        """
        self.isValidChannel(channel)
        self.serial.write(b'VOUT%d?\n' % channel)
        ret = self.getline() # self.serial.readline() #eol=self.eol)
        return float(ret.replace('V', ''))

    def selectIndependentMode(self):
        """
        TRACK<NR1>
        """
        self.serial.write(b'TRACK0\n')
        self.checkError()

    def selectTrackingSeriesMode(self):
        """
        TRACK<NR1>
        """
        self.serial.write(b'TRACK1\n')
        self.checkError()

    def selectTrackingParallelMode(self):
        """
        TRACK<NR1>
        """
        self.serial.write(b'TRACK2\n')
        self.checkError()

    def enableBeep(self, enable = True):
        """
        BEEP<Boolean>
        """
        self.serial.write(b'BEEP%d\n' % int(enable))
        self.checkError()

    def enableOutput(self, enable = True):
        """
        OUT<Boolean>
        """
        self.serial.write(b'OUT%d\n' % int(enable))
        self.checkError()

    def printStatus(self):
        """
        STATUS?
        """
        self.serial.write(b'STATUS?\n')

        for i in range(3):
            ret = self.getline() # self.serial.readline() #eol=self.eol)
            print(ret[:-len(self.eol)])

    def getIdentification(self):
        """
        *IDN?
        """
        self.serial.write(b'*IDN?\n')
        ret = self.getline() # self.serial.readline() #eol=self.eol)
        return ret[:-len(self.eol)]

    def recallSetting(self, memory):
        """
        RCL<NR1>
        """
        self.isValidMemory(memory)
        self.serial.write(b'RCL%d\n' % memory)
        
        ret = self.getline() # self.serial.readline() #eol=self.eol)
        return ret[:-len(self.eol)]

    def saveSetting(self, memory):
        """
        SAV<NR1>
        """
        self.isValidMemory(memory)
        self.serial.write(b'SAV%d\n' % memory)

        self.checkError()
        
    def printHelp(self):
        """
        HELP?
        """
        self.serial.write(b'HELP?\n')
        
        for i in range(19):
            ret = self.getline() # self.serial.readline() #eol=self.eol).decode('utf-8')
            print(ret.replace('\r','\n'))
            # print(ret[:-len(self.eol)].replace('\r','\n'))
            if not ret:
                break

    def getError(self):
        """
        ERR?
        """
        self.serial.write(b'ERR?\n')
        ret = self.serial.readline().decode('utf-8').strip() #eol=self.eol)
        if ret:
            if ret == "No Error.":
                ret = ""
            return ret 
        else:
            raise RuntimeError('Cannot read error message')

    def checkError(self):
        err = self.getError()
        if err:
            raise RuntimeError(err)

    def setRemoteMode(self):
        """
        REMOTE
        """
        self.serial.write(b'REMOTE\n')
        self.checkError()

    def setLocalMode(self):
        """
        LOCAL
        """
        self.serial.write(b'LOCAL\n')
