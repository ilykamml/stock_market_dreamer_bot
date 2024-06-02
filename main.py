import yfinance as yf
import datetime


def get_stock_price(symbol, date):
    stock = yf.Ticker(symbol)
    hist = stock.history(start=date, actions=False)
    if len(hist) == 0:
        return None
    # return hist['Open'][0]
    return hist.iloc[0]['Close']


def calculate_profit(symbol, investment, investment_date):
    current_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    investment_price = get_stock_price(symbol, investment_date)
    current_price = get_stock_price(symbol, current_date)

    if investment_price is None or current_price is None:
        print("Не удалось получить данные о цене акции. Пожалуйста, попробуйте другую дату или компанию.")
        return None, None, None, None

    shares_bought = int(investment / investment_price)  # Buy as many whole shares as possible
    remaining_money = investment - (shares_bought * investment_price)
    current_value = shares_bought * current_price

    profit = current_value - (shares_bought * investment_price)
    profit_percentage = ((current_value / (shares_bought * investment_price)) - 1) * 100

    return shares_bought, remaining_money, profit, profit_percentage, current_value, investment_price


def main():
    # symbol = input("Введите название компании: ")
    # investment = float(input("Сколько денег вы хотели бы вложить? "))
    # investment_date = input("Введите дату вложения (в формате YYYY-MM-DD): ")
    symbol = "AAPL"
    investment = 200.00
    investment_date = "2020-03-12"

    shares_bought, remaining_money, profit, profit_percentage, current_value, investment_price = [round(i, 2) for i in
                                                                                                  calculate_profit(
                                                                                                      symbol,
                                                                                                      investment,
                                                                                                      investment_date)]

    if shares_bought is None or remaining_money is None or profit is None or profit_percentage is None:
        return
    print(f"Вы могли купить {shares_bought} акций по цене {investment_price}$ и у вас осталось бы {remaining_money}$.")
    print(f"Вы могли бы заработать {profit}$ и ваш процент прибыли составил бы {profit_percentage}%.")
    print(f"Стоимость ваших акций на текущий момент составила бы {current_value}$.")


if __name__ == "__main__":
    main()
