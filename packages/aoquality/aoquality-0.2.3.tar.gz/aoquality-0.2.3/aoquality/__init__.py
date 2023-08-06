try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

try:
    __version__ = importlib_metadata.version(__name__)
except importlib_metadata.PackageNotFoundError:
    __version__ = 'dev'

from .aoquality import make_ant_matrix, pol_dict, available_stats
from .aoquality import AOQualityBaselineStat, AOQualityFrequencyStat, AOQualityTimeStat
