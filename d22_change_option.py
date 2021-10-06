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
        self.diff = 0  # 大臺的點數差

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
            f"{topic}-Price:[{quote['Close']}]Diff:[{quote['DiffPrice']}]volumn:[{quote['Volume']}]"
        )

        if topic.find("TFE/TXF") > 0:
            self.diff = quote["DiffPrice"][0]
        elif topic.find("OPT/TX") > 0:
            reduced_point = 1

            # 設定要減少的點數
            if self.diff < quote["Close"][0]:
                reduced_point = self.diff  # 比市價還要低的數字
            else:
                # 當變動很多時，要剪去的價格會比較大，但比現價還要小
                reduced_point = quote["Close"][0] - reduced_point

            self.change_price(quote["Close"], True, reduced_point)  # 價格比現價還要低，

    def change_price(self, price, diff, points):
        """Simulate to change the price of the order."""

        self.mxf_price = price[0] - points if diff else price[0] + points
        print(f"選擇權：current price:{price[0]}-new price:{self.mxf_price}")


def sleeper():
    """For sleeping... Let us get the quote and change the price."""

    print("-start sleep...")
    time.sleep(60)
    print("-Wake up!!!!")


timer = threading.Thread(target=sleeper)  # 建立執行緒

t = trader()
t.login()

t.subscribe(t.api.Contracts.Futures.TXF["TXF202110"])  # 訂閱臺指期-2021/10
t.subscribe(t.api.Contracts.Options.TX2.TX2202110016300C)  # 訂閱臺指選擇權10W2月 16300C

t.api.quote.set_quote_callback(t.quote_callback)  # 設定處理回報的功能

timer.start()  # 執行thread
timer.join()  # 等待結束thread

t.unsubscribe(t.api.Contracts.Futures.TXF["TXF202110"])  # 取消訂閱臺指期-2021/10
t.unsubscribe(t.api.Contracts.Options.TX2.TX2202110016300C)  # 取消訂閱臺指選擇權10W2月 16300C
