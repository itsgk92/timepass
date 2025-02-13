
from nsepython import equity_history

symbol = "HCLTECH"
series = "EQ"
start_date = "4-01-2025"
end_date ="14-01-2025"
h = equity_history(symbol,series,start_date,end_date)
print(type(h))