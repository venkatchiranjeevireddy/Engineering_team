import unittest
import datetime
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):
    def test_deposit(self):
        account = Account()
        account.deposit(100)
        self.assertEqual(account.balance, 100)
        self.assertEqual(len(account.transactions),1)
        self.assertEqual(account.transactions[0]['type'],'deposit')
        with self.assertRaises(ValueError):
            account.deposit(-50)

    def test_withdraw(self):
        account = Account(100)
        account.withdraw(50)
        self.assertEqual(account.balance, 50)
        self.assertEqual(len(account.transactions),1)
        self.assertEqual(account.transactions[0]['type'],'withdrawal')
        with self.assertRaises(ValueError):
            account.withdraw(150)

    def test_buy(self):
        account = Account(1000)
        account.buy("AAPL", 5, 170)
        self.assertEqual(account.balance, 1150)
        self.assertEqual(account.holdings["AAPL"], 5)
        self.assertEqual(len(account.transactions), 1)
        self.assertEqual(account.transactions[0]['type'],'buy')
        with self.assertRaises(ValueError):
            account.buy("AAPL",-5,170)
        with self.assertRaises(ValueError):
            account.buy("AAPL",5,-170)
        with self.assertRaises(ValueError):
            account.buy("AAPL",100,170)

    def test_sell(self):
        account = Account()
        account.buy("AAPL", 5, 170)
        account.sell("AAPL", 3, 180)
        self.assertEqual(account.balance, 540)
        self.assertEqual(account.holdings["AAPL"], 2)
        self.assertEqual(len(account.transactions), 2)
        self.assertEqual(account.transactions[1]['type'],'sell')
        with self.assertRaises(ValueError):
            account.sell("AAPL", 10, 180)
        with self.assertRaises(ValueError):
            account.sell("TSLA", 3, 180)
        with self.assertRaises(ValueError):
            account.sell("AAPL", -3, 180)
        with self.assertRaises(ValueError):
            account.sell("AAPL", 3, -180)

    def test_get_portfolio_value(self):
        account = Account()
        account.buy("AAPL", 5, 170)
        account.buy("TSLA", 2, 250)
        self.assertAlmostEqual(account.get_portfolio_value(), 2350)

    def test_get_profit_loss(self):
        account = Account(1000)
        account.buy("AAPL", 5, 170)
        account.sell("AAPL", 3, 180)
        self.assertAlmostEqual(account.get_profit_loss(), 540-1000 + 3*180)

    def test_get_holdings(self):
        account = Account()
        account.buy("AAPL", 5, 170)
        self.assertEqual(account.get_holdings(), {"AAPL": 5})

    def test_get_transactions(self):
        account = Account()
        account.deposit(100)
        self.assertEqual(len(account.get_transactions()),1)
        self.assertEqual(account.get_transactions()[0]['type'],'deposit')

    def test_negative_initial_deposit(self):
        with self.assertRaises(ValueError):
            Account(-100)

    def test_str_representation(self):
        account = Account(100)
        account.buy("AAPL", 2, 150)
        self.assertTrue("\nBalance: 700.00\nHoldings: {'AAPL': 2}\nTransactions:" in str(account))

if __name__ == '__main__':
    unittest.main()