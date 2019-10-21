import ppa
import unittest
import pandas as pd


class TestPPA(unittest.TestCase):
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
        self.load['Load'] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.load['Used RE'] = [1, 8, 2, 4, 15, 6, 11, 1, 9]
        self.load['Excess RE'] = [1, 8, 2, 4, 15, 6, 11, 12, 9]
        self.load['RE Generator'] = [7, 8, 2, 4, 15, 6, 11, 1, 9]
        self.load['Empty'] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        # Define test load profile
        self.price = pd.DataFrame()
        self.price['DateTime'] = ['2017/01/01 00:00:00',
                              '2017/01/01 00:30:00',
                              '2017/01/01 01:00:00',
                              '2017/01/01 01:30:00',
                              '2017/01/01 02:00:00',
                              '2017/01/01 02:30:00',
                              '2017/01/01 03:00:00',
                              '2017/01/01 04:30:00',
                              '2017/01/01 00:00:00']
        self.price.DateTime = pd.to_datetime(self.load.DateTime)
        self.price['NSW'] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # Define mock scenario table
        self.scenario_table = pd.DataFrame.from_dict({
            'PPA': ['Off-site - Contract for Difference'],
            'PPA_Volume': ['All RE'],
            'Wholesale_Exposure_Volume': ['All RE'],
            'PPA_Price': [5.0],
            'Excess_RE_Purchase_Price': [0.0],
            'Excess_RE_Sale_Price': [0.0],
            'Load_MLF': [0.90],
            'Load_DLF': [0.95],
            'Generator_MLF': [1.1],
            'Generator_DLF': [1.2],
        })

    def test_runs_without_error(self):
        self.scenario_table['ppa_costs'] = self.scenario_table.apply(
            ppa.calc_by_row, axis=1, price_profile=self.price['NSW'], residual_profiles=self.load)
        x=1