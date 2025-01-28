import inputs, utils
import nse_queries

reference_date = inputs.ref_date
twelve_months_ago = utils.compute_date_from_reference(reference_date, -12)
fifteen_months_ago = utils.compute_date_from_reference(reference_date, -15)

price_df = nse_queries.get_price_history(inputs.underlying, inputs.underlying_type, fifteen_months_ago, reference_date)

#print(price_df[["DATE", "CLOSE", "DAILY_RETURN"]].tail(5))

volatility_windows_days_index = [3, 6, 10, 20, 30, 60]
volatility_windows_days_stock = [5, 10, 20, 30, 60, 90]

sequence_expiry_dates = nse_queries.get_nfo_expiry_history(inputs.underlying, fifteen_months_ago, reference_date)



print(sequence_expiry_dates)

