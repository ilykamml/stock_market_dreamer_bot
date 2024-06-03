import yfinance as yf
import datetime


class SharesInfo:
    def __init__(self, profit: float or None, profit_percentage: float, current_value: float,
                 shares_bought: int, remaining_money: float, old_value: float,
                 price_at_investment_date: float, current_price: float):
        self.profit = profit
        self.profit_perc = profit_percentage
        self.current_value = current_value
        self.shares_bought = shares_bought
        self.remaining_money = remaining_money
        self.old_value = old_value
        self.price_at_investment_date = price_at_investment_date
        self.current_price = current_price

    def __str__(self):
        if self.profit is None:
            text = 'Мы не смогли получить данные по вашему запросу, попробуйте другой запрос'
        else:
            text = (f'Вы могли купить {self.shares_bought} акций по цене {self.price_at_investment_date:.2f}$ '
                    f'на сумму {self.old_value:.2f}$ и у вас осталось бы {self.remaining_money:.2f}$\n'
                    f'Вы могли бы заработать {self.profit:.2f}$ и ваш процент прибыли составил бы {self.profit_perc:.2f}%\n'
                    f'Стоимость ваших акций на текущий момент составила бы {self.current_value:.2f}$ '
                    f'по {self.current_price:.2f}$ за акцию')
            if self.profit_perc <= 0.1:
                text = text.replace('%', '%📉')
            else:
                text = text.replace('%', '%📈')
        return text


def get_stock_prices(symbol):
    stock = yf.Ticker(symbol)
    hist = stock.history(start='1700-01-01')

    if len(hist) == 0:
        return None

    return hist


def calculate_profit(symbol: str, investment: float, investment_date: str):
    hist = get_stock_prices(symbol)

    if hist is None:
        return SharesInfo(None, [-1 for _ in range(7)])

    try:
        price_at_investment_date = hist[investment_date:investment_date].iloc[0]['Close']
        current_price = hist.iloc[-1]['Close']
    except Exception as exp:
        print(exp)
        return SharesInfo(None, *[-1 for _ in range(7)])

    shares_bought = int(investment / price_at_investment_date)
    shares_price_at_investment_date = shares_bought * price_at_investment_date
    remaining_money = investment - shares_price_at_investment_date
    current_value = shares_bought * current_price

    profit = current_value - shares_price_at_investment_date
    profit_percentage = ((current_value / shares_price_at_investment_date) - 1) * 100 if shares_bought != 0 else 0

    return SharesInfo(profit, profit_percentage, current_value,
                      shares_bought, remaining_money, shares_price_at_investment_date,
                      price_at_investment_date, current_price)


print(calculate_profit('AAPL', 1000, '2023-06-02'))
