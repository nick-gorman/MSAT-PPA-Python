import pandas as pd
import scenario_runner

load_profiles = pd.read_csv('data/load_profiles.csv')
price_profiles = pd.read_csv('data/price_profiles.csv')
charge_set = pd.read_csv('data/charge_set.csv')
scenarios = pd.read_csv('data/scenarios.csv')
scenarios['retail'], scenarios['ppa'] = \
    zip(*scenarios.apply(scenario_runner.run_scenario_from_row, axis=1, price_profiles=price_profiles,
                         load_profiles=load_profiles, charge_set=charge_set))
scenarios.to_csv('data/costs.csv')