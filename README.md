# MSAT-PPA Python

This python library replicates the functionality of the MS Excel based tool [Multi-factor Sensitivity Analysis Tool for 
Renewable PPAs (MSAT-PPA)](http://www.ceem.unsw.edu.au/renewable-ppa-tool). MSAT-PPA was created with MS Excel to ensure
it was accessible to large energy users, e.g. large business or local governments, who commonly use MS Excel for a wide
variety of tasks. However, it can be hard to test the functionality for large spreadsheets to ensure there are no 
errors. To provide the MSAT-PPA development team with confidence that the tool was performing as expected, MSAT-PPA was 
replicated in Python and results between the two versions compared. Recently, some interest in using the Python 
version of MSAT-PPA has been expressed, so we have published the code here to allow stakeholders to assess it.

# Development stage

As discussed above MSAT-PPA Python was not originally developed for external use. As such, it is not 'production ready',
it lacks a fully developed test suite and complete documentation. Testing was conduct by comparison of results from the
MS Excel version, the documentation of the MS Excel version may also be helpful in understanding the Python version. 
Below some examples are used to demonstrate the basic functionality. It may be developed into production ready software
in the future.

# Examples
## Contract for difference PPA and wholesale energy purchase
This is a simple example of a contract for difference PPA and the purchase of energy though the whole sale market.
Calculations are done a one day of data to simplify things for the sake of writing an easy to understand example.

The basic description of the PPA being modelled is:
* A energy user with a flat load of 20 MW (10 MWh per half hour) has signed a PPA for purchase of renewable energy from
a solar farm. The PPA is being facilitated thought a retailer.
* The user has agreed to buy the output from the solar farm every hour up to the volume of energy they use in each half
hour. To realise this they have signed a contract for difference with the solar farm at a strike price of 90 $/MWh, and
the retailer has agreed to pass through the wholesale price to user for the same volume every half hour.
* When the solar farm does produce enough energy to cover the users load the user buys the residual from the retailer
according to their agreed set of tariffs.

The steps in the example are as follows:
1. Define the load and solar generation data in a pandas DataFrame
2. Define the whole energy price data (we keep it simple with 100 $/MWh for all intervals)
3. Calculate the residual load profiles. This is bought through the grid ('black), from the RE generator, and how much
excess RE there is in each half hour interval
4. Pass to the ppa.calc function the correct setting to for the PPA described above, and the load and wholesale price 
   data
5. Print a summary of the PPA costs. Note many of the possible PPA cost are 0.0 because we did not have the associated
contract terms in the simple example. 

```python
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

```

