import requests


def get_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 250,
        "page": 1
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        print(" Network or API error while fetching crypto data.")
        return []


def get_exchange_rate(target_currency):
    url = "https://api.exchangerate.host/latest?base=USD&symbols=" + target_currency

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data["rates"][target_currency]
    except:
        print(" Failed to retrieve exchange rate. Using USD.")
        return 1


def get_price(coin):
    return coin["current_price"]


def process_data(crypto_list, min_market_cap, limit):
    filtered = []

    for coin in crypto_list:
        if coin["market_cap"] and coin["market_cap"] >= min_market_cap:
            filtered.append(coin)

    sorted_coins = sorted(
        filtered,
        key=get_price,
        reverse=True
    )

    return sorted_coins[:limit]


def display_results(coins, rate, currency):
    if not coins:
        print("No results found.")
        return

    print("\n📊 Top Cryptocurrencies\n")

    for coin in coins:
        price = coin["current_price"] * rate
        print(coin["name"], "(" + coin["symbol"].upper() + ")")
        print("  Price:", format(price, ".2f"), currency)
        print("  Market Cap:", format(coin["market_cap"], ","), "USD\n")


def save_to_file(coins, rate, currency):
    file = open("crypto_results.txt", "w")

    for coin in coins:
        price = coin["current_price"] * rate
        file.write(
            coin["name"] + " - " + format(price, ".2f") + " " + currency + "\n"
        )

    file.close()


def main():
    try:
        currency = input("Enter currency (USD, EUR, UZS): ").upper()
        min_market_cap = int(input("Minimum market cap (USD): "))
        limit = int(input("How many coins to display?: "))
    except ValueError:
        print(" Invalid input. Please enter numbers only.")
        return

    crypto_data = get_crypto_data()
    exchange_rate = get_exchange_rate(currency)

    processed_data = process_data(
        crypto_data,
        min_market_cap,
        limit
    )

    display_results(processed_data, exchange_rate, currency)
    save_to_file(processed_data, exchange_rate, currency)

    print(" Results saved to crypto_results.txt")



main()
