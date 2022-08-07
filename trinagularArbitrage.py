import ccxt
import telebot
exchange = ccxt.binance()
bot = telebot.TeleBot('') #your bot token that you get from https://t.me/BotFather
sum = 100 #trade amount 
telegramId = 501179740 #your telegram id
def getCombinations(marketSymbols, base):
    combinations = []
    for sym1 in marketSymbols:   
        sym1Token1 = sym1.split('/')[0]
        sym1Token2 = sym1.split('/')[1]   
        if (sym1Token2 == base):
            for sym2 in marketSymbols:
                sym2Token1 = sym2.split('/')[0]
                sym2Token2 = sym2.split('/')[1]
                if (sym1Token1 == sym2Token2):
                    for sym3 in marketSymbols:
                        sym3Token1 = sym3.split('/')[0]
                        sym3Token2 = sym3.split('/')[1]
                        if((sym2Token1 == sym3Token1) and (sym3Token2 == sym1Token2)):
                            combination = {
                                'base':sym1Token2,
                                'intermediate':sym1Token1,
                                'ticker':sym2Token1,
                            }
                            combinations.append(combination)
    return combinations
while True:
    markets = exchange.fetchMarkets()
    marketSymbols = [market['symbol'] for market in markets]
    combinationsUsdt = getCombinations(marketSymbols, 'USDT')
    for item in combinationsUsdt:
        try:
            res1 = exchange.fetch_ticker(f'{item["intermediate"]}{item["base"]}')
            res2 = exchange.fetch_ticker(f'{item["ticker"]}{item["intermediate"]}')
            res3 = exchange.fetch_ticker(f'{item["ticker"]}{item["base"]}')
            print((sum/res1["ask"]/res2["ask"]*res3["bid"]-sum)/sum*100)
            print((sum/res3["ask"]*res2["bid"]*res1["bid"]-sum)/sum*100)
            if (sum/res1["ask"]/res2["ask"]*res3["bid"]-sum)/sum*100 > 1:
                bot.send_message(telegramId, f'✅New triangular arbitrage✅\n\n📍Route: {item["base"]} ==> {item["intermediate"]} ==> {item["ticker"]} ==> {item["base"]}\n\n💵Profit: {round((sum/res1["ask"]/res2["ask"]*res3["bid"]-sum)/sum*100, 3)} %')
            if (sum/res3["ask"]*res2["bid"]*res1["bid"]-sum)/sum*100 > 1:
                bot.send_message(telegramId, f'✅New triangular arbitrage✅\n\n📍Route: {item["base"]} ==> {item["ticker"]} ==> {item["intermediate"]} ==> {item["base"]}\n\n💵Profit: {round((sum/res3["ask"]*res2["bid"]*res1["bid"]-sum)/sum*100, 3)} %')
        except:
            continue
