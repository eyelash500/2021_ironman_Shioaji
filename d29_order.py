import threading
import time
from datetime import datetime

import shioaji as sj


class trader:
    """The Shioaji Object"""

    def __init__(self) -> None:
        self.simulation = True  # 是否為測試環境
        self.id = "PAPIUSER07"
        self.pwd = "2222"
        self.api = sj.Shioaji()

        # option spread
        self.lef_leg_price = 0  # sell side
        self.right_leg_price = 0  # buy side

    def login(self, id=None, pwd=None, simulation=True):
        """Login to Shioaji.

        Args:
            id(str): user ID
            pwd(str): the login password

        Returns:
            bool: True is login successfully, False is not.
        """

        print(f"=start login-{datetime.now().strftime('%Y%m%d')}")
        if id and pwd:
            self.id = id
            self.pwd = pwd

        try:
            # 登入 shioaji
            self.api = sj.Shioaji(simulation=simulation)
            self.api.login(person_id=self.id, passwd=self.pwd)
        except Exception as exc:
            print(f"id={self.id}, pwd={self.pwd}...{exc}")
            return False

        return True


t = trader()
t.login()

# 選擇權下單
contract = t.api.Contracts.Options.TXO.TXO202110016300C
order = t.api.Order(
    action=sj.constant.Action.Buy,
    price=10,
    quantity=2,
    price_type=sj.constant.StockPriceType.LMT,
    order_type=sj.constant.FuturesOrderType.ROD,
    octype=sj.constant.FuturesOCType.Auto,
    account=t.api.futopt_account,
)

trade = t.api.place_order(contract, order)
trade

# 期貨下單
contract = t.api.Contracts.Futures.TXF.TXF202110
order = t.api.Order(
    action=sj.constant.Action.Buy,
    price=15000,
    quantity=2,
    price_type=sj.constant.StockPriceType.LMT,
    order_type=sj.constant.FuturesOrderType.ROD,
    octype=sj.constant.FuturesOCType.Auto,
    account=t.api.futopt_account,
)

trade = t.api.place_order(contract, order)
trade
