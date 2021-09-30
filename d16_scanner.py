from datetime import datetime

import shioaji as sj


class scanner_market:
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

    def scanner(self):
        """Get the scanner object

        Return:
            scanner(obj): the result of scanner
        """
        # 拿掉count: scanners() got an unexpected keyword argument 'count'
        scanner = self.api.scanners(scanner_type=sj.constant.ScannerType.AmountRank)
        return scanner


t = scanner_market()
t.login()
data = t.scanner()
print(data[0])
