import asyncio
import datetime
import aiohttp
import re
import aiofile




CURRENCY=['EUR', 'USD']

async def exchange(date):
    final_result = []
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}') as request:
                    result = await request.json()
                    day_result={date:{}}
                    for currency in result["exchangeRate"]:
                        if currency["currency"] in CURRENCY:
                            res={currency['currency']: {'sale': currency['saleRate'], 'purchase': currency['purchaseRate']}}
                            day_result[date].update(res)
                    final_result.append(day_result)
        except aiohttp.ClientConnectionError as error:
            print(error)
    final_result = pretty_view(final_result)
    return final_result


async def excange2(lst: list):
    tasks = []
    for i in lst:
        tasks.append(exchange(i))
    results = await asyncio.gather(*tasks)
    return ''.join(results)

def how_much_days(days):
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

def message_handler(message):
    res_list = []
    command = None
    message=message.lower()
    if 'exchange' in message:
        command='exchange'
        res_list.append(command)
    if command:
        res = re.findall(r'\b\d+\b', message)
        if res:
            res_list.append(res[0])
    return res_list

async def aiologger(message):
    async with aiofile.async_open('logs.log', 'a') as file:
        await file.write(f'{str(datetime.datetime.now())}: Was used function {message}\n')

def pretty_view(lst: list):
    str_view = ''
    for dct in lst:
        for key, val in dct.items():
            str_view+=f"Date: {key}\n"
            for i in val:
                str_view += f"{i}: {val[i]}\n"
    return str_view

