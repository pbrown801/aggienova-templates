import matplotlib.pyplot as plt
import numpy as np
import math
from spectrophot_array_in import *
from countsin_sedout import *
from speccounts import *
from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM(H0=73, Om0=0.3)
import numpy as np
import matplotlib.pyplot as plt
from operator import truediv

snname = sys.argv[1]
filename =  snname + '_uvotB15.1.dat'




