import pandas as pd
import pprint

import ppa, residuals

# 1. One day of load and generation data
profiles = pd.DataFrame({
    'DateTime': pd.date_range("2022-01-01", periods=48, freq="30min"),
    'flat_load': [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0,
                  10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0,
                  10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0,
                  10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0,
                  10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
    'solar': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.5, 7.5, 12.5,
              17.5, 20.0, 20.0, 17.5, 12.5, 7.5, 2.5, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
})

# 2. One day of wholesale price data
prices = pd.DataFrame({
    'DateTime': pd.date_range("2022-01-01", periods=48, freq="30min"),
    'flat_price': [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0,
                   100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0,
                   100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0,
                   100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0,
                   100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]
    })

# 3. Calculate the residual profiles need for PPA and tariff calculations
residual_profiles = residuals.calc(profiles, load_id='flat_load', generator_id='solar')

print(residual_profiles)
#               DateTime  Load  RE Generator  Black  Excess RE  Used RE  Empty
# 0  2022-01-01 00:00:00  10.0           0.0   10.0        0.0      0.0    0.0
# 1  2022-01-01 00:30:00  10.0           0.0   10.0        0.0      0.0    0.0
# 2  2022-01-01 01:00:00  10.0           0.0   10.0        0.0      0.0    0.0
# 3  2022-01-01 01:30:00  10.0           0.0   10.0        0.0      0.0    0.0
# 4  2022-01-01 02:00:00  10.0           0.0   10.0        0.0      0.0    0.0

# 4. Calculate PPA costs
ppa_costs = ppa.calc(contract_type='Off-site - Contract for Difference',
                     ppa_volume='RE Uptill Load',  # In each 30 min interval the PPA volume is the lesser of generator
                                                   # or load volume.
                     contract_price=90.0,
                     wholesale_volume='RE Uptill Load',  # In each 30 min interval the volume bought from the wholesale
                                                         # market is less of generator or load volume.
                     residual_profiles=residual_profiles,
                     price_profile=prices['flat_price']
                     )

# 5. A summary of PPA costs
pprint.pprint(ppa_costs)
# {'Cost of Excess RE': 0.0,
#  'Generation shortfall penalty payment': 0,
#  'LGC purchase cost': 0,
#  'LGC shortfall penalty payment': 0,
#  'PPA': -1200.0,
#  'Payment from Excess RE': 0,
#  'Payment from wholesale of RE': 0.0,
#  'Wholesale cost': 12000.0}
