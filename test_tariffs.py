import unittest
import pandas as pd
import tariffs

class TestConvertingTOU(unittest.TestCase):
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
                                end_weekday=7, start_hour=0, end_hour=23, load_profile=self.load)
        self.assertEqual(sum([1, 2, 3, 4, 5, 6, 7, 8, 9])/1000, cost)