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

    def _get_subscribe(self) -> bool:
        """Get the subscibe format."""

        print(self.api.quote.subscribe)

        return True

    def subscribe(self, contract):
        """subscribe the contract quote."""

        print("=Subscribe=")
        self.api.quote.subscribe(contract, quote_type=sj.constant.QuoteType.Tick)

    def unsubscribe(self, contract):
        """unsubscribe the contract."""

        print("unsubscribe")
        self.api.quote.unsubscribe(contract, quote_type=sj.constant.QuoteType.Tick)

    def quote_callback(self, topic: str, quote: dict):
        """Get the quote info and change the oder price.
        The quote's format is v0: quote is a dict and the value is a list.
        """
        print(
            f"{topic}-Price:[{quote['Close']}]rate:[{quote['DiffRate']}]volumn:[{quote['Volume']}]"
        )

        self.change_price(
            quote["Close"], True if quote["DiffRate"][0] > 0 else False, 10
        )

    def change_price(self, price, diff, points):
        """Simulate to change the price of the order."""

        print(
            f"current price:{price[0]}-new price:{price[0]-points if diff else price[0]+points}"
        )


def sleeper():
    """進行執行緒睡覺功能，用來等待並且處理價格"""
    print("-start sleep...")
    time.sleep(30)
    print("-Wake up!!!!")


timer = threading.Thread(target=sleeper)  # 建立執行緒

t = trader()
t.login()

t.subscribe(t.api.Contracts.Futures.TXF["TXF202110"])  # 訂閱台指期-2021/10

t.api.quote.set_quote_callback(t.quote_callback)  # 設定處理回報的功能

timer.start()  # 執行thread
timer.join()  # 等待結束thread

t.unsubscribe(t.api.Contracts.Futures.TXF["TXF202110"])  # 取消訂閱台指期-2021/10
