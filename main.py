# -*- coding: utf-8 -*-
import asyncio
import platform

from httpx import AsyncClient
from config import *

from aiogram import Bot

bot = Bot(API_TOKEN, parse_mode='html')

headers = {'Authorization': f'Bearer {LOLZ_KEY}'}
session = AsyncClient(base_url='https://api.lolz.guru/market', headers=headers)

SAVED = []


async def main():
    while True:
        for page_ in range(max_page):
            total = await session.get(f'/telegram?page={str(page_ + 1)}', params=FILTERS)
            if not total.status_code == 200:
                await asyncio.sleep(5)
                total = await session.get(f'/telegram?page={str(page_ + 1)}', params=FILTERS)

            for item in total.json()['items']:
                if not item['item_id'] in SAVED:
                    if item.get('telegram_admin_groups'):
                        patr = max([pp['participants_count'] for pp in item.get('telegram_admin_groups')])
                        if patr >= subs_need and item['price'] <= max_price:
                            SAVED.append(item['item_id'])
                            await asyncio.sleep(3)
                            await session.post(f'/{str(item["item_id"])}/reserve', data={'price': item["price"]})
                            await asyncio.sleep(3)
                            x = await session.post(f'/{str(item["item_id"])}/check-account')

                            if buy_account:
                                await asyncio.sleep(3)
                                x = await session.post(f'/{str(item["item_id"])}/confirm-buy')
                                if x.json().get('status'):
                                    await bot.send_message(admin_id, '✅ Аккаунт успешно куплен\n\n'
                                                                     f'🔗 Ссылка: https://lolz.guru/market/{str(item["item_id"])}/\n'
                                                                     f'💎 Цена: {str(item["price"])} рублей\n'
                                                                     f'❤️ Подписчиков: {str(patr)}'
                                                                      
                                                                     f'by @soblazncc'
                                                                     f'v1.0'
                                                                     '')

                            else:

                                if x.json().get('status'):
                                    # await session.get(f'/{str(item["item_id"])}/reserve?price={str(item["price"])}')
                                    await bot.send_message(admin_id, '✅ Аккаунт успешно забронирован\n\n'
                                                                     f'🔗 Ссылка: https://lolz.guru/market/{str(item["item_id"])}/\n'
                                                                     f'💎 Цена: {str(item["price"])} рублей\n'
                                                                     f'❤️ Подписчиков: {str(patr)}'
                                                                      
                                                                     f'by @soblazncc'
                                                                     f'v1.0'
                                                                     '')

            await asyncio.sleep(5)


if __name__ == '__main__':
    print('Bot Started')
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(main())
    except:
        print('Бот не может обработать ваш запрос')
