### Import MySportsFeeds class(es) upon initiation of the program
from .MySportsFeeds_API import MySportsFeeds
from .v1_0 import API_v1_0
from .v1_1 import API_v1_1
from .v1_2 import API_v1_2
from .v2_0 import API_v2_0
from .v2_1 import API_v2_1
from pkg_resources import get_distribution

__version__ = "2.1.1" #get_distribution('ohmysportsfeedspy').version
