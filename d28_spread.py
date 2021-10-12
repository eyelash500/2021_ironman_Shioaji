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

    def subscribe_bid_ask(self, contract):
        """subscribe the contract quote."""

        print("=Subscribe=")
        self.api.quote.subscribe(contract, quote_type=sj.constant.QuoteType.BidAsk)

    def set_init_spread_price(self, left_leg, right_leg):
        """Get the two legs' price which is the call option spread."""

        option1 = self.api.snapshots(left_leg)
        option2 = self.api.snapshots(right_leg)

        self.lef_leg_price = option1[0]["sell_price"]
        self.right_leg_price = option2[0]["buy_price"]

    def quote_callback(self, topic: str, quote: dict):
        """Get the quote info and change the oder price.
        The quote's format is v0: quote is a dict and the value is a list.
        """

        if topic.find("16300") > 0:
            self.lef_leg_price = quote["AskPrice"][0]  # 取得ask的第一個值
        elif topic.find("16350") > 0:
            self.right_leg_price = quote["BidPrice"][0]  # 取得bid的第一個值

        print(
            f"價差組合：16300-sell={self.lef_leg_price}_16350-buy={self.right_leg_price}_diff={self.lef_leg_price-self.right_leg_price}"
        )


def sleeper():
    """For sleeping... Let us get the quote and change the price."""

    print("-start sleep...")
    time.sleep(10)
    print("-Wake up!!!!")


t = trader()
t.login()


timer = threading.Thread(target=sleeper)  # 建立執行緒

# 設定初始值
option_sell = [t.api.Contracts.Options.TX2.TX2202110016300C]
option_buy = [t.api.Contracts.Options.TX2.TX2202110016350C]
t.set_init_spread_price(option_sell, option_buy)


t.subscribe_bid_ask(t.api.Contracts.Options.TX2.TX2202110016300C)  # 訂閱臺指選擇權10W2月 16300C
t.subscribe_bid_ask(t.api.Contracts.Options.TX2.TX2202110016350C)  # 訂閱臺指選擇權10W2月 16350C
t.api.quote.set_quote_callback(t.quote_callback)  # 設定處理回報的功能

timer.start()  # 執行thread
timer.join()  # 等待結束thread

t.unsubscribe(t.api.Contracts.Options.TX2.TX2202110016300C)  # 訂閱臺指選擇權10W2月 16300C
t.unsubscribe(t.api.Contracts.Options.TX2.TX2202110016350C)  # 訂閱臺指選擇權10W2月 16350C
