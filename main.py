import datetime
import aiohttp
import asyncio
import platform
import sys


CURRENCY=['EUR', 'USD']


def how_much_days():
    days = sys.argv[1]
    try:
        new_value = sys.argv[2]
        global CURRENCY
        CURRENCY.append(new_value)
    except IndexError:
        pass
    result=[]
    current_date = datetime.datetime.now().date()
    if int(days)<0 or None:
        return ('Uncorrect call')
    elif int(days)>10:
        days = 10
    for i in range(int(days)):
        day = current_date - datetime.timedelta(days=i)
        result.append(day.strftime('%d.%m.%Y'))
    return result



async def exchange(lst):
    final_result = []
    async with aiohttp.ClientSession() as session:
        try:
            for i in lst:
               async with session.get(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={i}') as request:
                    result = await request.json()
                    day_result={i:{}}
                    for currency in result["exchangeRate"]:
                        if currency["currency"] in CURRENCY:
                            res={currency['currency']: {'sale': currency['saleRate'], 'purchase': currency['purchaseRate']}}
                            day_result[i].update(res)
                    final_result.append(day_result)
            print(final_result)
        except aiohttp.ClientConnectionError as error:
            print(error)



if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(exchange(how_much_days()))