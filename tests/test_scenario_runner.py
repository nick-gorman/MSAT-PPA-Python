import scenario_runner
import unittest
import pandas as pd


class TestScenarioRunner(unittest.TestCase):
    def setUp(self):
        # Define test load profile
        self.load = pd.DataFrame()
        self.load['DateTime'] = ['2017/01/01 00:00:00',
                              '2017/01/01 00:30:00',
                              '2017/01/01 01:00:00',
                              '2017/01/01 01:30:00',
                              '2017/01/01 02:00:00',
                              '2017/01/01 02:30:00',
                              '2017/01/01 03:00:00',
                              '2017/01/01 04:30:00',
                              '2017/01/01 00:00:00']
        self.load.DateTime = pd.to_datetime(self.load.DateTime)
        self.load['load'] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.load['re'] = [1, 8, 2, 4, 15, 6, 11, 1, 9]
        # Define set of charges
        self.set_of_charges = pd.DataFrame.from_dict({
            'Charge Type': ['Energy', 'Network', 'Feed In'],
            'Volume Type': ['Energy ($/MWH)', 'Energy ($/MWH)', 'Energy ($/MWH)'],
            'Rate': [11.0, 12.0, -1.0],
            'MLF': [1.1, 1.0, 0.9], 'DLF': [0.9, 1.1, 1.0],
            'Start Month': [1, 1, 1], 'End Month': [12, 12, 12],
            'Start Weekday': [1, 1, 1], 'End Weekday': [7, 7, 7],
            'Start Hour': [0, 0, 0], 'End Hour': [23, 23, 23],
            'Alt Load Profile': ['', '', 'Other']
        })
        # Define mock scenario table
        self.scenario_table = pd.DataFrame.from_dict({
            'PPA': ['Off-site - Contract for Difference'],
            'Wholesale_Exposure_Volume': ['All RE'],
            'Load_ID': ['load'],
            'Generator_ID': ['re']
        })

    def test_runs_without_error(self):
        self.scenario_table['retail_costs'] = self.scenario_table.apply(
            scenario_runner.run_scenario_from_row, axis=1, load_profiles=self.load, charge_set=self.set_of_charges)
        x=1