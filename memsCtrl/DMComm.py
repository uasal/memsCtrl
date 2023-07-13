#!/usr/bin/python
import serial
import DMMap as dmap
import time
import sys


# Communication variables
#port = 'COM15';
port = '/dev/ttyACM4';
#baud = 9600;  # can we get a fast baud?  Or is it timing out and not returning from \n
baud = 115200;
#timeout = 10; # this is a 10 second timeout.  Try something shorter.
timeout = 3;  # a 3 second timeout.  Do we get all the data?

class DM:
    def __init__(self):
        """ This creates the serial connection to the DM Arduino """

        try:
            self.ardconnect = serial.Serial(port, baud, timeout=timeout);
            # One suggested solution.  Just this line subbed for the above line
#            self.ardconnect = serial.Serial(port, baud, timeout=timeout, dsrdtr=None);
# Or add these two following lines
##            self.ardconnect.setDTR(False);
##            time.sleep(0.5);  # apparently the sleep is very important
        except (serial.SerialException,ValueError):
            print("There was an error opening the port")
            return;# -1;
        print("Opened the port successfully.")
        print("Getting data already in buffer.")
        for ii in range(32):
            try:
                reply = self.ardconnect.readline()
#                print(reply.decode("utf-8"))
                sys.stdout.write(reply.decode("utf-8"))
            except serial.Timeout:
                print("Timeout trying to get data from buffer")

    def setMirror(self,mirror=0,dacSetting=0):
        """ This will set the mirror number to the desired setting """
        mcoords = dmap.actuatorMap[mirror];
        dac = mcoords[1];
        dacChan = mcoords[2];
#        print(mirror);
#        print(dac);
#        print(dacChan);
        self.setHV(dac,dacChan,dacSetting);

        
    def setHV(self,dac,dacChan,dacSetting):
        """ This will create the command to write to the serial port and send it to the DM Arduino """
        # First let's create the string to send
        ardCommand = '@{dac},{dacChan}${dacSetting}\n'.format(dac=dac,dacChan=dacChan,dacSetting=dacSetting)
#        print(ardCommand)
#        print(ardCommand.encode())
        self.ardconnect.write(ardCommand.encode());
        # Now we can get a reply to make sure command we received and processed correctly
#        reply = self.ardconnect.readline(); # this is blocking, but I have to test to see what I get back
        try:
            reply = self.ardconnect.readall();  # with a 0.1s timeout this is now fast
            print(reply.decode());
        except serial.Timeout:
            print("Timeout trying to get data from buffer.")
        # parse the reply and compare to the settings requested
        ### Put code here once I understand the reply and how to parse
        return reply.decode();  # I can return the reply as well

    def close(self):
        self.ardconnect.close()

#def getDataSet(interval=0,numSamples=25):
#    q = dvm.DVM();  # connect and instantiate the DVM
#    data = q.getDataSet(interval,numSamples);  # get a data set of numSamples large with an interval between samples
#    q.close();  # close the connection
#    return data
#
#def getDigSet(sPerSec=1000000,numSamples=100000,vrange=1000):
#    q = dvm.DVM();
#    data = q.getDigitizedData(Samppersec=sPerSec,vrange=vrange,num_samples=numSamples);
#    q.close()
#    return data

# Let's start with a single channel
# Board F, DAC 23, Ch 7
# Probe point: Samtec 2B, pin A01 (top left corner of the connector)
# Start with 3 voltages and 1000 samples each
def runVoltages(dmcon,dac=23,ch=7,voltages=[10,20,30],interval=0,numSamples=1000,hvin=180.0):
    # Go through the voltages requested and take 100 samples each
    for volt in voltages:
        digValue = round(volt/hvin*2.0**16);
        reply = dmcon.setHV(dac,ch,digValue);
        data = getDataSet(interval,numSamples);
        #dvm.writeDataToFile(data,'dm_')
        
def digVoltages(dmcon,dac=23,ch=7,voltages=[10,20,30],sPerSec=1000000,numSamples=100000,hvin=180.0):
    for volt in voltages:
        digValue = round(volt/hvin*2.0**16);
        reply = dmcon.setHV(dac,ch,digValue);
        vrange = 100;  # default value
        if (volt >= 100):
            vrange = 1000; # this is the highest we need to go
        data = getDigSet(sPerSec,numSamples,vrange);
        #dvm.writeDataToFile(data,'digdm_');
    #q = dvm.DVM()
    #q.connection.write("sens:func 'VOLTage'");
    #q.connection.write("trigger:continuous restart;");
    #q.close();
    return;

def runDacCodes(dmcon,dac=23,ch=7,voltage=10,interval=0,numSamples=1000,hvin=180.0):
    """ Will run a series of voltages each one bit apart starting at the requested starting voltage """
    dac_code = round(voltage/hvin*2.0**16)
    for ii in range(10):
        reply = dmcon.setHV(dac,ch,dac_code)
        data = getDataSet(interval,numSamples)
#        dvm.writeDataToFile(data,'dm_')
        dac_code = dac_code + 1;
