import yfinance as yf
import pandas as pd


class TradingStrategy:
    def __init__(self, symbol, start_date, end_date, capital=5000):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.capital = capital

        self.cash = capital
        self.position = 0
        self.trades = []

    def download_data(self):
        df = yf.download(
            self.symbol,
            start=self.start_date,
            end=self.end_date,
            progress=False
        )
        return df

    def clean_data(self, df):
        # Remove duplicate rows
        df = df[~df.index.duplicated(keep="first")]

        # Handle NaN values
        df = df.ffill()

        return df

    def add_moving_averages(self, df):
        df["MA50"] = df["Close"].rolling(window=50).mean()
        df["MA200"] = df["Close"].rolling(window=200).mean()
        return df

    def run_strategy(self):
        df = self.download_data()
        df = self.clean_data(df)
        df = self.add_moving_averages(df)

        for i in range(1, len(df)):
            # BUY condition (Golden Cross)
            if (
                df["MA50"].iloc[i] > df["MA200"].iloc[i]
                and df["MA50"].iloc[i - 1] <= df["MA200"].iloc[i - 1]
                and self.position == 0
            ):
                buy_price = df["Close"].iloc[i]
                self.position = int(self.cash // buy_price)

                if self.position > 0:
                    self.cash -= self.position * buy_price
                    self.trades.append(
                        ("BUY", df.index[i].date(), round(buy_price, 2))
                    )

            # SELL condition (Death Cross)
            elif (
                df["MA50"].iloc[i] < df["MA200"].iloc[i]
                and df["MA50"].iloc[i - 1] >= df["MA200"].iloc[i - 1]
                and self.position > 0
            ):
                sell_price = df["Close"].iloc[i]
                self.cash += self.position * sell_price
                self.trades.append(
                    ("SELL", df.index[i].date(), round(sell_price, 2))
                )
                self.position = 0

        # Force close on last day
        if self.position > 0:
            final_price = df["Close"].iloc[-1]
            self.cash += self.position * final_price
            self.trades.append(
                ("FORCE SELL", df.index[-1].date(), round(final_price, 2))
            )
            self.position = 0

        profit = round(self.cash - self.capital, 2)
        return profit

    def summary(self):
        profit = self.run_strategy()

        print("\n📊 Trade History")
        print("-" * 30)
        for trade in self.trades:
            print(trade)

        print("\n💰 Result Summary")
        print("-" * 30)
        print(f"Initial Capital : ${self.capital}")
        print(f"Final Capital   : ${round(self.cash, 2)}")
        print(f"Profit / Loss   : ${profit}")


if __name__ == "__main__":
    trader = TradingStrategy(
        symbol="AAPL",
        start_date="2018-01-01",
        end_date="2023-12-31"
    )
    trader.summary()
