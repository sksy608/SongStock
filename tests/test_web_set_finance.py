import unittest
from web_set_finance import getTableData

Program_Dir = "~/git/SongStock/"

class TestFinance(unittest.TestCase):

    def test_getTableData(self):
        appl = wsf.getTableData("companyfinance", "PTT", "balance", 0)
        self.assertIsNotNone(appl)
