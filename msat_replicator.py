import pandas as pd
import scenario_runner

load_profiles = pd.read_csv('data/load_profiles.csv')
charge_set = pd.read_csv('data/charge_set.csv')
scenarios = pd.read_csv('data/scenarios.csv')
scenarios['retail_costs'] = scenarios.apply(scenario_runner.run_scenario_from_row, axis=1, load_profiles=load_profiles,
                                            charge_set=charge_set)
scenarios.to_csv('data/costs.csv')