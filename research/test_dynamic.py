import unittest
import numpy as np
import pandas as pd
from research.backtest import targets, PROXIES, CASH
class DynamicSelectionTests(unittest.TestCase):
    def test_filters(self):
        x=pd.DataFrame([[80,40,20,10,-10,-20,-40,-80],[-1]*8,[0]*8],columns=PROXIES)
        for strategy,count in [('mom_above_mean',4),('mom_above_zero',4),('mom_above_mean_positive',4),('mom_above_10',3),('mom_above_median',4)]:
            w=targets(strategy,x,x,x,x,x,1)
            self.assertEqual(int((w.iloc[0][PROXIES]>0).sum()),count)
            self.assertAlmostEqual(w.iloc[0][PROXIES].sum(),.995)
            self.assertAlmostEqual(w.iloc[1][CASH],.995)
            self.assertAlmostEqual(w.iloc[2][CASH],.995)
    def test_negative_mean(self):
        x=pd.DataFrame([[-1,-2,-3,-4,-5,-6,-7,-8]],columns=PROXIES)
        w=targets('mom_above_mean',x,x,x,x,x,1)
        self.assertEqual(int((w.iloc[0][PROXIES]>0).sum()),4)
        w=targets('mom_above_mean_positive',x,x,x,x,x,1)
        self.assertAlmostEqual(w.iloc[0][CASH],.995)
    def test_cash_slots(self):
        x=pd.DataFrame([[1,2,3,4,-1,-2,-3,-4]],columns=PROXIES)
        w=targets('mom_positive_cash_slots',x,x,x,x,x,1)
        self.assertAlmostEqual(w.iloc[0][CASH],.4975)
        self.assertAlmostEqual(w.iloc[0].sum(),.995)
