from datetime import datetime, timedelta
from pathlib import Path
import warnings

import toml


def is_weekend(dt: datetime):
    weekday = dt.weekday()
    #  Saturday, Sunday
    if weekday in (5, 6):
        return True
    return False


class FuturesTradingCalendar:

    def __init__(self):
        # tips
        #   这里的日期为自然日，非交易结算日
        #   周末没有日盘与夜盘，程序逻辑排除

        config_file_path = Path(__file__).parent / 'data' / 'futures.toml'
        self.config = toml.load(config_file_path)

        now = datetime.now()
        if now.date() > self.config['expire_date']:
            warnings.warn('the trading calendar config is expired...')

        # Special cases
        self.no_day_trading_dates = set(self.config['holiday_dates'])
        self.no_night_trading_dates = set(self.config['holiday_dates']) | set(self.config['no_night_trading_dates'])

    def has_day_trading(self, dt: datetime):
        if is_weekend(dt):
            return False
        if dt.date() in self.no_day_trading_dates:
            return False
        return True

    def has_night_trading(self, dt: datetime):
        dt = dt - timedelta(hours=4)  # 夜盘跨自然日的情况
        if is_weekend(dt):
            return False
        if dt.date() in self.no_night_trading_dates:
            return False
        return True
