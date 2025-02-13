import nsepython as nse
from datetime import datetime, timedelta

Underlying = "NIFTY"
Index = "NIFTY 50"
Today = datetime.now().strftime("%d-%m-%Y")
OneYearAgo = (datetime.now()-timedelta(days=365)).strftime("%d-%m-%Y")

nse.index_history("NIFTY 50", OneYearAgo, Today)
