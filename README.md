# memsCtrl


Quick start guide:

1. As the xsup user (probably), start the DM control process: `memsCtrl`
2. In a python session

```
from magpyx.utils import ImageStream
import numpy as np

# open the shared memory image stream
dm = ImageStream('dm02disp') # bad practice in general, but okay for now 

# Approach 1: send a 2D command
cmd = np.zeros((34,34))
cmd[15,15] = 10 # volts
dm.write(cmd)

# Approach 2: start with a 1D vector ordered by the BMC actuator convention and then convert and send as a 2D command
from scoobpy.utils import get_kilo_map_mask
from magpyx.dm import dmutils

dm_map, dm_mask = get_kilo_map_mask()
cmdvec = np.zeros(952)
cmdvec[345] = 10 # volts, 0-indexed
cmd = dmutils.map_vector_to_square(cmdvec, dm_map, dm_mask)
dm.write(cmd)
```
