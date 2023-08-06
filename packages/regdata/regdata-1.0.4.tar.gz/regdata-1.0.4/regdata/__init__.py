
# Dataloaders
from .dataloaders.della_gatta_gene import DellaGattaGene
from .dataloaders.heinonen_4 import Heinonen4
from .dataloaders.jump1d import Jump1D
from .dataloaders.mcycle import MotorcycleHelmet
from .dataloaders.nonstat2d import NonStat2D
from .dataloaders.olympic import Olympic
from .dataloaders.sinejump import SineJump1D
from .dataloaders.noisy_sine import SineNoisy
from .dataloaders.smooth1d import Smooth1D
from .dataloaders.step import Step

from .config import set_backend
import os
os.environ['BACKEND'] = 'numpy'
os.environ['DATAPATH'] = '/tmp/somerandomtexthere_'
