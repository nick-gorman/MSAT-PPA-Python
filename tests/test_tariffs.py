import unittest
import pandas as pd
import tariffs


class TestSingleTOUCharges(unittest.TestCase):
    def setUp(self):
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
        self.load['Energy'] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_all_times(self):
        cost = tariffs.tou_calc('blah', rate=1, mlf=1, dlf=1, start_month=1, end_month=12, start_weekday=1,
                                end_weekday=7, start_hour=0, end_hour=23, load_profiles=self.load, load_id='Energy')
        self.assertEqual(sum([1, 2, 3, 4, 5, 6, 7, 8, 9])/1000, cost)


class TestSetOfTOUCharges(unittest.TestCase):
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
        self.load['Black'] = [1, 2, 3, 4, 15, 6, 7, 8, 9]
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

    def test_calc_tou_set_runs(self):
        tariffs.calc_tou_set(self.set_of_charges, self.load, 'Off-site - Contract for Difference', 'All RE')
