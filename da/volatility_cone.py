import math
import numpy as np
from pandas import DataFrame

import inputs, utils
from exchanges import nse_queries

reference_date = inputs.ref_date
twelve_months_ago = utils.compute_date_from_reference(reference_date, -12)
fifteen_months_ago = utils.compute_date_from_reference(reference_date, -15)

print(f"getting price history of {inputs.underlying}")
price_df = nse_queries.get_price_history(inputs.underlying, inputs.underlying_type, fifteen_months_ago, reference_date)
#print(price_df[["DATE", "CLOSE", "DAILY_RETURN"]].tail(5))

print(f"getting sequence expiry of {inputs.underlying}")
sequence_expiry_dates = nse_queries.get_nfo_expiry_history(inputs.underlying, twelve_months_ago, reference_date)
#print(f"{sequence_expiry_dates}")

volatility_cone_windows = utils.get_volatility_cone_windows(inputs.underlying_type)

annulaized_realized_volatitlies = {}

for window_length in volatility_cone_windows:
    annulaized_realized_volatitlies[window_length] = {}
    for expiry_date in sequence_expiry_dates:
        window = price_df[price_df['DATE'] <= expiry_date].tail(window_length)
        window_volatility_pct = window["DAILY_RETURN"].std()
        annualized_window_volatiltiy = window_volatility_pct * math.sqrt(252)
        annulaized_realized_volatitlies[window_length][expiry_date] = round(annualized_window_volatiltiy.item()*100, 5)

print(annulaized_realized_volatitlies)

volat_cone = dict()

for window_length in annulaized_realized_volatitlies:
    values = list(annulaized_realized_volatitlies[window_length].values())
    volatility_array = np.array(values)
    std = round(volatility_array.std(),2)
    mean = round(volatility_array.mean(), 2)
    std_1 = round(mean + (1 * std), 2)
    std_2 = round(mean + (2 * std), 2)
    std_n2 = round(mean - (2 * std), 2)
    std_n1 = round(mean - (1 * std), 2)
    volt_max = round(volatility_array.max(), 2)
    volt_min = round(volatility_array.min(), 2)
    #print(window_length, volt_max, std_2, std_1, mean, std_n1, std_n2, volt_min, std)
    volat_cone[str(window_length)] = {'volt_max': volt_max, 'std_2': std_2, 'std_1': std_1, 'mean': mean, 'std_n1': std_n1, 'std_n2': std_n2, 'volt_min': volt_min, 'dev':  std}

print("Volatility cone data")
volat_cone_df = DataFrame.from_dict(volat_cone)
print(volat_cone_df)
plt = volat_cone_df.T.plot()
fig = plt.get_figure()
fig.savefig('out.png')