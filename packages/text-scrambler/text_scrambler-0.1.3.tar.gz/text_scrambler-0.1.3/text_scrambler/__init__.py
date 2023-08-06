from pkg_resources import get_distribution, DistributionNotFound

from .text_scrambler import Scrambler

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "text-scrambler"
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound
