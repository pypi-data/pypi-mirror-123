import numpy as np
import numba as nb
import math as m
from numba.experimental import jitclass
from ._looper import iterasator
# from numba.typed import List


# specs for the jitclass which needs to be statically typed
spec = [
		('iteratools', nb.types.List(iterasator.class_type.instance_type, reflected=True)),
		('nx', nb.int32),
		('ny', nb.int32),
		('nxy', nb.int32),
		('dx', nb.float64),
		('dy', nb.float64),
		('dxy', nb.float64),
		('receivers', nb.int32[:]),
		('donors', nb.int32[:]),
		('nbdonors', nb.int32[:]),
		('nbreceivers', nb.int32[:]),
		('length2donors', nb.float64[:]),
		('length2receivers', nb.float64[:]),
		('graph_type', nb.types.unicode_type),

	]

