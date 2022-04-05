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

# Define Scenarios: Each row defines a set of input values for a scenario.
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

# Run PPA and tariff calculations on scenario inputs.
scenarios['retail'], scenarios['ppa'] = \
    zip(*scenarios.apply(scenario_runner.run_scenario_from_row, axis=1, price_profiles=prices,
                         load_profiles=profiles, charge_set=applicable_tariffs))

print(scenarios)
#    Scenario ID                                 PPA  ...   retail     ppa
# 0            1  Off-site - Contract for Difference  ...  34000.0  7200.0
# 1            2  Off-site - Contract for Difference  ...  34000.0  7600.0