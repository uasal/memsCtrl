#!/usr/bin/python
# -----------------------------------------------------------------------------
# @file      ArduinoCompileUpload.py
# @brief     python routines that use the arduino command line interface (arduino-cli)
# @author    Stephen Kaye <kaye2@arizona.edu>
# @date      2022-11-01
# @modified  Not yet
#
#            subprocess is used to create and run commands from the comand line
#            Currently this is specific to the prototype DM Driver Board
#            future effort may be exerted to generalize this interface
#
#            def Compile(<sketch name>) compiles the arduino sketch
#            def Upload(<sketch name>) uploads the sktech to the arduino
#
# -----------------------------------------------------------------------------


import subprocess

def Compile(sketch='cliDriverDACTest'):
    subprocess.run(["arduino-cli","compile","--verbose","--fqbn","arduino:sam:arduino_due_x_dbg",sketch],check=True);
    return;

def CompileTeensy(sketch='TeensySketch'):
    subprocess.run(["arduino-cli","compile","--verbose","--fqbn","arduino:sam:arduino_due_x_dbg",sketch],check=True);
    return;
    
def Upload(sketch='cliDriverDACTest'):
    error = subprocess.run(["arduino-cli","upload","-p","/dev/ttyACM0","--fqbn","arduino:sam:arduino_due_x_dbg",sketch],check=True);
    return;

def NativeCompile(sketch='cliDriverDACTest'):
    subprocess.run(["arduino-cli","compile","--verbose","--fqbn","arduino:sam:arduino_due_x",sketch],check=True);
    return;

def NativeUpload(sketch='cliDriverDACTest'):
    error = subprocess.run(["arduino-cli","upload","-p","/dev/ttyACM0","--fqbn","arduino:sam:arduino_due_x",sketch],check=True);
    return;
