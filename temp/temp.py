import datetime

import utils
from exchanges import nse_queries
from exchanges.nse_queries import NSEIndeces
from utils import UnderlyingType

#print(nse_queries.get_index_constituents(NSEIndeces.NIFTYMID50))

print(nse_queries.get_price_history("M&M", UnderlyingType.EQ, utils.compute_date_from_reference(datetime.datetime.now(),0,-10), datetime.datetime.now()))

