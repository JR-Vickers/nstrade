"""
EMA Crossover 1 strategy for Bitcoin.
Goes long when the fast SMA crosses above the slow SMA, and exits when it crosses below.
It's weighted towards the most recent data points.
"""

from src.core.strategy import Strategy
import pandas as pd

class EMACrossoverStrategy(Strategy):
    def __init__(self, initial_capital=10000, fast=20, slow=100):
        super().__init__(
            initial_capital=initial_capital,
            author_name="Jarrett",
            strategy_name="EMA Crossover 1",
            description="Goes long when the fast EMA crosses above the slow EMA, and exits when it crosses below. It's weighted towards the most recent data points."
        )
        self.fast = fast
        self.slow = slow
        self.alpha_fast = 2 / (fast + 1)
        self.alpha_slow = 2 / (slow + 1)
        self.fast_ema = None     # will hold the running EMA values
        self.slow_ema = None
        self.last_signal = 'hold'

    def process_bar(self, bar):
        price = bar['close']
        self.current_bar = bar

        # Initialise on first tick
        if self.fast_ema is None:
            self.fast_ema = price
            self.slow_ema = price
            self.last_signal = 'hold'
            return

        # Update EMAs
        self.fast_ema = price * self.alpha_fast + self.fast_ema * (1 - self.alpha_fast)
        self.slow_ema = price * self.alpha_slow + self.slow_ema * (1 - self.alpha_slow)

        # Generate signal
        if self.fast_ema > self.slow_ema and self.position == 0:
            self.last_signal = 'buy'
        elif self.fast_ema < self.slow_ema and self.position == 1:
            self.last_signal = 'sell'
        else:
            self.last_signal = 'hold'

    def get_signal(self):
        return self.last_signal

    def get_signals(self, df: pd.DataFrame) -> pd.Series:
        signals = pd.Series('hold', index=df.index)
        signals.iloc[0] = 'buy'
        return signals