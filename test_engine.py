import unittest
import pandas as pd
import numpy as np
from engine import breadth, states

class EngineTest(unittest.TestCase):
    def test_scores(self):
        idx=pd.date_range('2020-01-01',periods=200)
        p=pd.DataFrame({'A':np.exp(np.arange(200)/100),'B':np.exp(-np.arange(200)/100)},index=idx)
        r=breadth(p,['A','B'],stale=0)
        self.assertEqual(r.Valid.iloc[-1],2)
        self.assertAlmostEqual(r.Trend.iloc[-1],0)
        self.assertTrue(r.Composite.dropna().between(-100,100).all())
        self.assertTrue(np.allclose(r[['UF','UP','DP','DF','Neutral']].dropna().sum(axis=1),100))
    def test_missing(self):
        p=pd.DataFrame({'A':range(100)},index=pd.date_range('2020-01-01',periods=100))
        r=breadth(p,['A','B'],coverage=.6)
        self.assertTrue(r.Composite.isna().all())
    def test_prefix(self):
        p=pd.Series(np.sin(np.arange(150)/10)+10)
        pd.testing.assert_series_equal(states(p).iloc[:100],states(p.iloc[:100]))
