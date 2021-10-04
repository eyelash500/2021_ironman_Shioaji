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
        self.api = None

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
        print("訂閱中")
        self.api.quote.subscribe(contract, quote_type=sj.constant.QuoteType.Tick)

    def unsubscribe(self, contract):
        self.api.quote.unsubscribe(contract, quote_type=sj.constant.QuoteType.Tick)
        print("取消訂閱")


def scraper():
    print("start sleeping...")
    time.sleep(30)
    print("Wake up!!")


timer = threading.Thread(target=scraper)  # 建立執行緒

t = trader()
t.login()
t._get_subscribe()


@t.api.quote.on_quote
def quote_callback(topic: str, quote: dict):
    """Print quote info.

    此版本沒有 from shioaji import TickSTKv1了，
    所以不能用範例QuoteVersion.v1，
    只能用QuoteVersion.v0
    """

    print(f"Topic: {topic}, Quote: {quote}")


t.subscribe(t.api.Contracts.Futures.TXF["TXF202110"])
timer.start()  # 執行
timer.join()  # 等待執行緒跑完

t.unsubscribe(t.api.Contracts.Futures.TXF["TXF202110"])
