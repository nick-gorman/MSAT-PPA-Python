import unittest
import pandas as pd
import residuals


class TestResidualCalc(unittest.TestCase):
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
        self.load['load'] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.load['re'] = [1, 8, 2, 4, 15, 6, 11, 1, 9]

    def test_runs_without_error(self):
        residual_profiles = residuals.calc(load_profiles=self.load, load_id='load', generator_id='re')
        x=1