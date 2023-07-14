from time import sleep
from time import time
import numpy as np

from magpyx.utils import ImageStream
from magpyx.dm import dmutils
from scoobpy.utils import get_kilo_map_mask

from .DMComm import DM

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('memsCtrl')

def run_DM(shmim_name='dm01disp', vmax=180.0, nbits=16):
    '''
    Open DM connection and await commands via shared memory image
    '''

    # ---- Setup ----
    dm_map, dm_mask = get_kilo_map_mask()
    shmim = ImageStream(shmim_name)
    logger.info(f'Connected to shared memory image {shmim_name}.')

    if shmim.semindex is None:
        shmim.semindex = shmim.getsemwaitindex(2)
        logger.info(f'Got semaphore index {shmim.semindex}.')

    logger.info('Opening DM/Arduino connection')
    dmhandle = DM()

    logger.info('Ready for commands. Ctrl+c to exit.')

    try:
        while True:
            # wait on a new command
            shmim.semwait(shmim.semindex)

            # get command (in Volts)
            cmd2d = shmim.grab_latest()

            # convert to DAC value
            cm2d_dac = cmd2d / vmax * (2**nbits)

            # clip to maximum DAC value
            cmd2d_clipped = np.clip(cm2d_dac , 0, 2**nbits)

            # send clipped 2D array
            logger.info('Sending command!')
            t0 = time()
            send_array(cmd2d_clipped, dmhandle, dm_map, dm_mask)
            t1 = time()
            logger.info(f'Took {t1-t0} seconds')

    except KeyboardInterrupt: # this is broken, as always
        pass

    logger.info('Zeroing out all actuators')
    send_array(np.zeros(shmim.shape), dmhandle, dm_map, dm_mask)

    logger.info('Closing DM connection')
    dmhandle.close()
    logger.info(f'Closing shared memory image {shmim}')
    shmim.close()


def send_array(arr, dm, dm_map, dm_mask):
    '''
    Map 2D array of commands to 1D vector in BMC actuator ordering
    and send to DM sequentially
    '''
    vec = np.rint(dmutils.map_square_to_vector(arr, dm_map, dm_mask)).astype(np.uint16)
    for i, val in enumerate(vec):
        print(i, val)
        dm.setMirror(mirror=i, dacSetting=val)