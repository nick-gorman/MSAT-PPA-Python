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
1. [Contract for difference PPA and wholesale energy purchase](#contract-for-difference-ppa-and-wholesale-energy-purchase)
2. [Running PPA and Tariff calculations across scenarios](#Running-PPA-and-Tariff-calculations-across-scenarios)


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
data. Note many of the possible PPA cost are 0.0 because we did not have the associated contract terms in the simple
5. Define the tariffs applicable to the energy bought on the standard retail agreement
6. Calculate Tariff costs
example. 

```python
import pandas as pd
import pprint

import ppa, residuals, tariffs

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

print('\n Load profiles used for cost calculations:')
print(residual_profiles)
#               DateTime  Load  RE Generator  Black  Excess RE  Used RE
# 0  2022-01-01 00:00:00  10.0           0.0   10.0        0.0      0.0
# 1  2022-01-01 00:30:00  10.0           0.0   10.0        0.0      0.0
# 2  2022-01-01 01:00:00  10.0           0.0   10.0        0.0      0.0
# 3  2022-01-01 01:30:00  10.0           0.0   10.0        0.0      0.0
# 4  2022-01-01 02:00:00  10.0           0.0   10.0        0.0      0.0

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
print('\n PPA cost summary:')
pprint.pprint(ppa_costs)
# {'Cost of Excess RE': 0.0,
#  'Generation shortfall penalty payment': 0,
#  'LGC purchase cost': 0,
#  'LGC shortfall penalty payment': 0,
#  'PPA': -1200.0,
#  'Payment from Excess RE': 0,
#  'Payment from wholesale of RE': 0.0,
#  'Wholesale cost': 12000.0}

# 5. Define tariffs
applicable_tariffs = pd.DataFrame({
    'Charge name': ['peak', 'off_peak'],
    'Charge Type': ['Energy', 'Energy'],
    'Volume Type': ['Energy ($/MWh)', 'Energy ($/MWh)'],
    'Rate': [100.0, 70.0],
    'MLF': [1.0, 1.0],
    'DLF': [1.0, 1.0],
    'Start Month': [1, 1],
    'End Month': [12, 12],
    'Start Weekday': [1, 1],
    'End Weekday': [7, 7],
    'Start Hour': [7, 21],
    'End Hour': [20, 6]
})

# 6. Calculate Tariff costs
tariff_costs = tariffs.calc_tou_set(tou_set=applicable_tariffs, contract_type='Off-site - Contract for Difference',
                                    wholesale_volume='RE Uptill Load', load_profiles=residual_profiles)

print('\n Tariffs and costs summary:')
print(tariff_costs)
#   Charge name Charge Type     Volume Type  ...  End Hour  Alt Load ID     Cost
# 0        peak      Energy  Energy ($/MWh)  ...        20        Black  20000.0
# 1    off_peak      Energy  Energy ($/MWh)  ...         6        Black  14000.0
```

## Running PPA and Tariff calculations across scenarios
This example demonstrates the use of the scenario calculation functionality. The details of the contract are the same 
as the previous example, except we run two scenarios with different PPA strike prices. The scenario inputs are 
defined in pandas DataFrame with each row defining the complete set of inputs for a given scenario. This is quite a 
verbose way of defining the inputs, but the DataFrame could be constructed programmatically to easily create a large 
number of scenarios.

The steps in the example are as follows:
1. Define the load and solar generation data in a pandas DataFrame
2. Define the whole energy price data (we keep it simple with 100 $/MWh for all intervals)
3. Define the tariffs applicable to the energy bought on the standard retail agreement
4. Define Scenarios: Each row defines a set of input values for a scenario
5. Run PPA and tariff calculations on scenario inputs

```python
import pandas as pd
import scenario_runner

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

# 3. Define tariffs
applicable_tariffs = pd.DataFrame({
    'Charge name': ['peak', 'off_peak'],
    'Charge Type': ['Energy', 'Energy'],
    'Volume Type': ['Energy ($/MWh)', 'Energy ($/MWh)'],
    'Rate': [100.0, 70.0],
    'MLF': [1.0, 1.0],
    'DLF': [1.0, 1.0],
    'Start Month': [1, 1],
    'End Month': [12, 12],
    'Start Weekday': [1, 1],
    'End Weekday': [7, 7],
    'Start Hour': [7, 21],
    'End Hour': [20, 6]
})

# 4. Define Scenarios: Each row defines a set of input values for a scenario.
scenarios = pd.DataFrame({
    'Scenario ID': [1, 2],
    'PPA': ['Off-site - Contract for Difference', 'Off-site - Contract for Difference'],
    'Wholesale_Price_ID': ['flat_price', 'flat_price'],
    'Average_Wholesale_Price': [100.0, 100.0],
    'Wholesale_Exposure_Volume': ['RE Uptill Load', 'RE Uptill Load'],
    'Load_ID': ['flat_load', 'flat_load'],
    'Generator_ID': ['solar', 'solar'],
    'PPA_Volume': ['RE Uptill Load', 'RE Uptill Load'],
    'PPA_Price': [90.0, 95.0],  # The PPA strike prices is varied.
    'Excess_RE_Purchase_Price': [0.0, 0.0],
    'Excess_RE_Sale_Price': [0.0, 0.0],
    'LGC_Volume_Type': [0.0, 0.0],
    'LGC_Purchase_Volume': [0.0, 0.0],
    'LGC_Purchase_Price': [0.0, 0.0],
    'Yearly_Target_MWh': [0.0, 0.0],
    'Target_Period': ['Yearly', 'Yearly'],
    'Yearly_Short_Fall_Penalty_MWh': [0.0, 0.0],
    'Yearly_LGC_target_LGC': [0.0, 0.0],
    'Yearly_LGC_short_fall_penalty_LGC': [0.0, 0.0],
    'Load_MLF': [1.0, 1.0], 'Load_DLF': [1.0, 1.0],
    'Generator_MLF': [1.0, 1.0], 'Generator_DLF': [1.0, 1.0],
    'TOU_1': [100.0, 100.0], 'TOU_2': [70.0, 70.0], 'TOU_3': [0.0, 0.0], 'TOU_4': [0.0, 0.0], 'TOU_5': [0.0, 0.0],
    'TOU_6': [0.0, 0.0], 'TOU_7': [0.0, 0.0], 'TOU_8': [0.0, 0.0], 'TOU_9': [0.0, 0.0], 'TOU_10': [0.0, 0.0],
    'Flat_1': [0.0, 0.0], 'Flat_2': [0.0, 0.0], 'Flat_3': [0.0, 0.0], 'Flat_4': [0.0, 0.0], 'Flat_5': [0.0, 0.0],
    'Flat_6': [0.0, 0.0], 'Flat_7': [0.0, 0.0], 'Flat_8': [0.0, 0.0]
})

# 5. Run PPA and tariff calculations on scenario inputs.
scenarios['retail'], scenarios['ppa'] = \
    zip(*scenarios.apply(scenario_runner.run_scenario_from_row, axis=1, price_profiles=prices,
                         load_profiles=profiles, charge_set=applicable_tariffs))

print(scenarios)
#    Scenario ID                                 PPA  ...   retail     ppa
# 0            1  Off-site - Contract for Difference  ...  34000.0  7200.0
# 1            2  Off-site - Contract for Difference  ...  34000.0  7600.0
```



