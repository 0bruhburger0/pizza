#!/usr/bin/env python
# -*- coding: utf-8 -*-

import aiogram, apiai, json, btn, asyncio, texts, time, datetime, requests, poster
from aiogram import executor, Bot, Dispatcher, types, filters
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from db import update, new_user, get_order, insert_pizzes, insert_drinks, del_all, select_products, del_ord, del_drinks, del_pizzes
from telegram import ParseMode
from config import TOKEN_1, PAY_TOKEN, AI_TOKEN


URL = 'https://joinposter.com/api/menu.getProducts?token=542938:1788976df3f5ac2059cf3f310fc8d3f2&category_id=4'
URL_DRINKS = 'https://joinposter.com/api/menu.getProducts?token=542938:1788976df3f5ac2059cf3f310fc8d3f2&category_id=3'


dp = Bot(TOKEN_1)
bot = Dispatcher(dp)


@bot.message_handler(commands=['start'])
async def start(message: types.Message):
    tg_id = message.from_user.id
    await dp.send_message(tg_id, texts.hi, parse_mode=ParseMode.HTML)
    new_user(tg_id) # Добавляет юзера


@bot.message_handler(content_types=types.ContentType.CONTACT)
async def process_callbacks(message: types.Contact):
    tg_id = message.from_user.id
    await dp.send_message(tg_id, texts.time_ship, reply_markup=ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)
    await dp.send_message(tg_id, texts.time_example, reply_markup=btn.full, parse_mode=ParseMode.HTML)
    update('phone', message.contact.phone_number, tg_id)


new_pizza_o = []
dict_size = {}


@bot.callback_query_handler(lambda call: True)
async def process_callback_admin(call):
    tg_id = call.from_user.id
    msg = call.message.message_id
    order = get_order(tg_id) # Достает весь заказ
    

    if call.data == '1h':
        await dp.edit_message_text(chat_id=tg_id, message_id=msg, text=texts.way_of_pay, reply_markup=btn.pays, parse_mode=ParseMode.HTML)
        time_1h = int(time.time()) + 3600
        value = datetime.datetime.fromtimestamp(time_1h)
        update('time_ship_conf', 'Время доставки: '+value.strftime('%H:%M'), tg_id)
        update('time_ship', value.strftime('%H:%M'), tg_id)


    elif call.data == '2h':
        await dp.edit_message_text(chat_id=tg_id, message_id=msg, text=texts.way_of_pay, reply_markup=btn.pays, parse_mode=ParseMode.HTML)
        time_2h = int(time.time()) + 7200
        value_2 = datetime.datetime.fromtimestamp(time_2h)
        update('time_ship_conf', 'Время доставки: '+value_2.strftime('%H:%M'), tg_id)
        update('time_ship', value_2.strftime('%H:%M'), tg_id)


    elif call.data == '3h':
        await dp.edit_message_text(chat_id=tg_id, message_id=msg, text=texts.way_of_pay, reply_markup=btn.pays, parse_mode=ParseMode.HTML)
        time_3h = int(time.time()) + 10800
        value_3 = datetime.datetime.fromtimestamp(time_3h)
        update('time_ship_conf', 'Время доставки: '+value_3.strftime('%H:%M'), tg_id)
        update('time_ship', value_3.strftime('%H:%M'), tg_id)


    elif call.data == 'quickly':
        await dp.edit_message_text(chat_id=tg_id, message_id=msg, text=texts.way_of_pay, reply_markup=btn.pays, parse_mode=ParseMode.HTML)
        time_half_h = int(time.time()) + 1800
        value_4 = datetime.datetime.fromtimestamp(time_half_h)
        update('time_ship_conf', 'Время доставки: '+value_4.strftime('%H:%M'), tg_id)
        update('time_ship', value_4.strftime('%H:%M'), tg_id)


    elif call.data == 'offline':
        list_products = []
        try:
            pizzes_raw = eval(order['size'])
        except:
            print('БФГ')

        try:
            drink_raw = eval(order['drink_id'])
        except:
            pass
        
        try:
            for p in pizzes_raw:
                size = pizzes_raw[p][0]
                count = pizzes_raw[p][1]
                string = f'{p} ({size}) - {count}шт'
                list_products.append(string)
        except:
            pass
        
        try:
            for d in drink_raw:
                cnt = d['cnt']
                name = d['name']
                string_d = f'{name} - {cnt}шт'
                list_products.append(string_d)
        except:
            pass

        priсe_pizzes = 0
        try:
            db_pizzes = select_products('pizzes')
            for pr in pizzes_raw:
                for i in db_pizzes:
                    if pr == i[1]:
                        for i_2 in eval(i[3]):
                            if i_2==pizzes_raw[pr][0]:
                                priсe_pizzes += (eval(i[3])[i_2] * int(pizzes_raw[pr][1]))
        except:
            pass    
        
        try:
            db_drinks = select_products('drinks')
            for dr in drink_raw:
                for r in db_drinks:
                    if dr['name']==r[1]:
                        priсe_pizzes += (int(r[2]) * int(dr['cnt']))
        except:
            pass

        await dp.edit_message_text(chat_id=tg_id,
                                   message_id=msg,
                                   text=f'<b>Осталось подтвердить информацию</b>\n\n'
                                   f'Заказ:<code>\n'+'\n'.join(l for l in list_products)+'</code>\n'
                                   f'Адрес:<code> {order["address"]}</code>\n'
                                   f'Время доставки:<code> {order["time_ship"]}</code>\n'
                                   f'Телефон:<code> {order["phone"]}</code>\n'
                                   f'Оплата:<code> при получении</code>\n'
                                   f'Итоговая стоимость:<code> {priсe_pizzes}₽</code>\n',
                                   reply_markup=btn.info_for_ofline,
                                   parse_mode=ParseMode.HTML)
        dict_size.clear()


    elif call.data == 'online':
        list_products = []
        try:
            pizzes_raw = eval(order['size'])
        except:
            print('БФГ')

        try:
            drink_raw = eval(order['drink_id'])
        except:
            pass

        try:
            for p in pizzes_raw:
                size = pizzes_raw[p][0]
                count = pizzes_raw[p][1]
                string = f'{p} ({size}) - {count}шт'
                list_products.append(string)
        except:
            pass
        
        try:
            for d in drink_raw:
                cnt = d['cnt']
                name = d['name']
                string_d = f'{name} - {cnt}шт'
                list_products.append(string_d)
        except:
            pass

        priсe_pizzes = 0
        try:
            db_pizzes = select_products('pizzes')
            for pr in pizzes_raw:
                for i in db_pizzes:
                    if pr == i[1]:
                        for i_2 in eval(i[3]):
                            if i_2==pizzes_raw[pr][0]:
                                priсe_pizzes += (eval(i[3])[i_2] * int(pizzes_raw[pr][1]))
        except:
            pass    
        
        try:
            db_drinks = select_products('drinks')
            for dr in drink_raw:
                for r in db_drinks:
                    if dr['name']==r[1]:
                        priсe_pizzes += (int(r[2]) * int(dr['cnt']))
        except:
            pass

        await dp.edit_message_text(chat_id=tg_id,
                                   message_id=msg,
                                   text=f'<b>Осталось подтвердить информацию</b>\n\n'
                                   f'Заказ:<code>\n'+'\n'.join(l for l in list_products)+'</code>\n'
                                   f'Адрес:<code> {order["address"]}</code>\n'
                                   f'Время доставки:<code> {order["time_ship"]}</code>\n'
                                   f'Телефон:<code> {order["phone"]}</code>\n'
                                   f'Оплата:<code> онлайн</code>\n'
                                   f'Итоговая стоимость:<code> {priсe_pizzes}₽</code>\n',
                                   reply_markup=btn.info_for_online,
                                   parse_mode=ParseMode.HTML)
        dict_size.clear()


    elif call.data == 'cofirm':
        await dp.send_message(tg_id, texts.cofirm_success, parse_mode=ParseMode.HTML)
        update('status', 0, tg_id)
        poster.poster_pos(order['pizza_id'], order['drink_id'], order['address'], order['phone'], order['time_ship_conf'], order['status'])


    elif call.data == 'cofirm_on':
        price = [types.LabeledPrice(label='Оплата заказа', amount=int(order['sum'])*100)]
        await dp.send_invoice(tg_id,
                              title='Оплата заказа',
                              description='Заказ подтвержен!\nВот счет для оплаты.',
                              provider_token=PAY_TOKEN,
                              currency='rub',
                              photo_url='https://image.freepik.com/free-vector/flat-design-traditional-pizza-background_23-2147647462.jpg',
                              photo_height=626,  # !=0/None or picture won't be shown
                              photo_width=626,
                              photo_size=512,
                              prices=price,
                              start_parameter='time-machine-example',
                              payload='its payload')


    elif call.data == 'edit_on':
        await dp.edit_message_text(chat_id=tg_id, message_id=msg, text=texts.edit_on, parse_mode=ParseMode.HTML)
        del_ord(tg_id)


    elif call.data == 'edit':
        await dp.edit_message_text(chat_id=tg_id, message_id=msg, text=texts.edit, parse_mode=ParseMode.HTML)
        del_ord(tg_id)


    elif call.data[:4] == '40sm':
        pizza_name = call.data[5:]
        all_pizzes = select_products('pizzes')
        pizza_o = eval(order['pizza_id'])
        size = eval(order['size'])
        
        # dict_size = {}

        for po, al in zip(pizza_o, all_pizzes):
            if pizza_name==po['name']:
                new_prod = {}
                new_mods = {}
                new_prod['id'] = po['id']
                mods_db = eval(al[2])
                new_mods[str(mods_db['40см'])] = po['cnt']
                new_prod['mods'] = new_mods
                new_pizza_o.append(new_prod)
                
                s = []
                s.append('40см')
                s.append(po['cnt'])
                dict_size[po['name']] = s
        update('size', str(dict_size), tg_id)

        
        if len(new_pizza_o)==len(pizza_o):
            await dp.edit_message_text(chat_id=tg_id, message_id=msg, text=texts.size, parse_mode=ParseMode.HTML)
            update('pizza_id', str(new_pizza_o), tg_id)
            new_pizza_o.clear()
        else:
            await dp.edit_message_text(chat_id=tg_id, message_id=msg, text='Ок, понял.', parse_mode=ParseMode.HTML)


    elif call.data[:4] == '20sm':
        pizza_name = call.data[5:]
        all_pizzes = select_products('pizzes')
        pizza_o = eval(order['pizza_id'])
        size = eval(order['size'])
        # print(pizza_o, size)
        
        # dict_size = {}

        for po, al in zip(pizza_o, all_pizzes):
            if pizza_name==po['name']:
                new_prod = {}
                new_mods = {}
                new_prod['id'] = po['id']
                mods_db = eval(al[2])
                new_mods[str(mods_db['20см'])] = po['cnt']
                new_prod['mods'] = new_mods
                new_pizza_o.append(new_prod)

                s = []
                s.append('20см')
                s.append(po['cnt'])
                dict_size[po['name']] = s
        update('size', str(dict_size), tg_id)

        if len(new_pizza_o)==len(pizza_o):
            await dp.edit_message_text(chat_id=tg_id, message_id=msg, text=texts.size, parse_mode=ParseMode.HTML)
            update('pizza_id', str(new_pizza_o), tg_id)
            new_pizza_o.clear()
        else:
            await dp.edit_message_text(chat_id=tg_id, message_id=msg, text='Ок, понял.', parse_mode=ParseMode.HTML)


    else:
        await dp.send_message(tg_id, texts.error)


@bot.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await dp.answer_pre_checkout_query(pre_checkout_query.id, ok=True, error_message=texts.error_payment)


@bot.message_handler(content_types=types.ContentTypes.SUCCESSFUL_PAYMENT)
async def got_payment(message: types.Message):
    tg_id = message.from_user.id
    await dp.send_message(message.chat.id, texts.pay_success, parse_mode=ParseMode.HTML)
    order = get_order(tg_id)
    update('status', 1, tg_id)
    poster.poster_pos(order['pizza_id'], order['drink_id'], order['address'], order['phone'], order['time_ship_conf'], order['status'])


@bot.message_handler()
async def start2(message: types.Message):
    request = apiai.ApiAI(AI_TOKEN).text_request()
    request.lang = 'ru'
    request.session_id = 'BatlabAIBot'
    request.query = message.text
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']
    intent_name = responseJson['result']['metadata']['intentName']
    print(responseJson)
    tg_id = message.from_user.id

    try:
        photo = responseJson['result']['fulfillment']['messages'][0]['payload']['imageUrl']
        text = responseJson['result']['fulfillment']['messages'][0]['payload']['speech']
    except:
        pass


    if response:
        await dp.send_message(tg_id, response)

    else:
        # Составы
        if intent_name == 'Мясная':
            await dp.send_photo(tg_id, photo, text)
        elif intent_name == '4 сыра':
            await dp.send_photo(tg_id, photo, text)
        elif intent_name == 'Гавайская':
            await dp.send_photo(tg_id, photo, text)
        elif intent_name == 'Маргарита':
            await dp.send_photo(tg_id, photo, text)
        elif intent_name == 'Пепперони':
            await dp.send_photo(tg_id, photo, text)
        elif intent_name == 'Вегетарианская':
            await dp.send_photo(tg_id, photo, text)
        elif intent_name == 'Фреш':
            await dp.send_photo(tg_id, photo, text)
        elif intent_name == 'Кола':
            await dp.send_photo(tg_id, photo, text)
        elif intent_name == 'Пепси':
            await dp.send_photo(tg_id, photo, text)


        # Меню
        elif intent_name == 'Меню':
            session = requests.Session()
            formpostdata = session.get(url=URL)
            formpostdataj = formpostdata.json()
            raw = formpostdataj['response']

            session_drink = requests.Session()
            formpostdata_drink = session_drink.get(url=URL_DRINKS)
            formpostdataj_drink = formpostdata_drink.json()
            raw_drink = formpostdataj_drink['response']

            drinks = {}
            for d in raw_drink:
                name_drink = (d['product_name'])
                price = (d['spots'][0]['price'])
                drinks[name_drink] = '<code>'+str(price[0:-2])+'₽'+'</code>'

            drinks_clean = []
            for dc in drinks:
                i = f"{dc} - {drinks[dc]}"
                drinks_clean.append(i)

            pizzes = {}
            for i in raw:
                modifications = (i['group_modifications'][0]['modifications'])
                mods = {}
                for mod in modifications:
                    mods[mod['name']] = '<code>'+str(mod['price'])+'₽'+'</code>'
                    pizzes[i['product_name']] = mods

            pizzes_clean = []
            for p, k in zip(pizzes.values(), pizzes):
                i = f"{k}\n    {list(p.keys())[0]} - {list(p.values())[0]}\n    {list(p.keys())[1]} - {list(p.values())[1]}"
                pizzes_clean.append(i)
            
            del_all("pizzes")
            for r in raw:
                pizza = r['product_name']
                p_id = r['product_id']
                mod_p = {}
                prices = {}
                for pm in r['group_modifications']:
                    for pmr in pm['modifications']:
                        mod_p[pmr['name']] = pmr['dish_modification_id']
                        prices[pmr['name']] = pmr['price']
                insert_pizzes(p_id, pizza.lower(), str(mod_p), str(prices))
            
            del_all("drinks")

            for rd in raw_drink:
                drink = rd['product_name']
                d_id = rd['product_id']
                d_price = rd['spots'][0]['price']
                insert_drinks(d_id, drink.lower(), d_price[0:-2])

            await dp.send_message(message.from_user.id, text='<b>Наши пиццы:</b>\n• '+("\n• ".join(p for p in pizzes_clean))+'\n\n<b>Напитки:</b>\n• '+("\n• ".join(d for d in drinks_clean))+'\n\n\n<b>Пример заказа:</b> буду маргариту 40см, две мясных 20см и колу\n\nТак же ты можешь попросить у меня состав и фото продуктов.', 
                                parse_mode=ParseMode.HTML)
            

        # Телефон
        elif intent_name == 'Номер телефона':
            await dp.send_message(tg_id, texts.time_ship, reply_markup=ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)
            await dp.send_message(tg_id, texts.time_example, reply_markup=btn.full, parse_mode=ParseMode.HTML)
            update('phone', responseJson['result']['parameters']['phone'], tg_id)


        # Заказ
        elif intent_name == 'Прием заказа':
            pizza = responseJson['result']['parameters']['pizza_name']
            drink = responseJson['result']['parameters']['drink']
            size_pizza = responseJson['result']['parameters']['size']
            db_pizzes = select_products("pizzes")
            db_drinks = select_products("drinks")
            total = 0


            if drink != [] and pizza != []:
                count_pizza = responseJson['result']['parameters']['count_pizza']
                count_drink = responseJson['result']['parameters']['count_drink']
                if size_pizza != []:
                    pizzes_name = {}
                    if count_pizza==['1']:
                        for p, s in zip(pizza, size_pizza):
                            o = []
                            o.append(s)
                            o.append('1')
                            pizzes_name[p] = o
                    else:
                        for p, s, c in zip(pizza, size_pizza, count_pizza):
                            o = []
                            o.append(s)
                            o.append(c)
                            pizzes_name[p] = o
                    pizzes = []

                    for i in db_pizzes:
                        for pz in pizzes_name:
                            if i[1]==pz:
                                prod = {}
                                prod['id'] = str(i[0])
                                prod_2 = {}
                                size_db = eval(i[2])
                                prices_db = eval(i[3])
                                for s_db in size_db:
                                    for cnt in count_pizza:
                                        if s_db==pizzes_name.get(pz)[0]:
                                            prod_2[str(size_db.get(s_db))] = pizzes_name.get(pz)[1]
                                            for price in prices_db:
                                                if s_db==price:
                                                    total += (prices_db.get(price) * int(cnt))
                                prod['mods'] = prod_2
                                pizzes.append(prod)
                    update('pizza_id', str(pizzes), tg_id)
                    update('size', str(pizzes_name), tg_id)

                    drink_names = []
                    for r in db_drinks:
                        for d in drink:
                            for cd in count_drink:
                                if r[1]==d.lower():
                                    all_params = {}
                                    all_params['id'] = r[0]
                                    all_params['cnt'] = cd
                                    all_params['name'] = r[1]
                                    total += (int(r[2]) * int(cd))
                                    drink_names.append(all_params)
                    update('drink_id', str(drink_names), tg_id)

                    print(pizza, pizzes)
                    if len(drink)!=len(drink_names) and len(pizza)!=len(pizzes):
                        await dp.send_message(tg_id, texts.not_pizza, parse_mode=ParseMode.HTML)
                        await dp.send_message(tg_id, texts.not_drink, parse_mode=ParseMode.HTML)
                    elif len(pizza)!=len(pizzes):
                        await dp.send_message(tg_id, texts.not_pizza, parse_mode=ParseMode.HTML)
                    elif len(drink)!=len(drink_names):
                        await dp.send_message(tg_id, texts.not_drink, parse_mode=ParseMode.HTML)
                    else:
                        await dp.send_message(tg_id, texts.size, parse_mode=ParseMode.HTML)
                

                else:
                    pizzes_name = {}
                    if count_pizza==['1']:
                        for p in pizza:
                            o = []
                            o.append(0)
                            o.append('1')
                            pizzes_name[p] = o
                    else:
                        for p, c in zip(pizza, count_pizza):
                            o = []
                            o.append(0)
                            o.append(c)
                            pizzes_name[p] = o
                    print(pizzes_name)

                    pizzes = []
                    for i in db_pizzes:
                        for pz in pizzes_name:
                            if i[1]==pz:
                                prod = {}
                                prod['id'] = str(i[0])
                                prod['cnt'] = str(pizzes_name[pz][1])
                                prod['name'] = pz
                                prod_2 = {}
                                prod['mods'] = prod_2
                                pizzes.append(prod)
                    update('pizza_id', str(pizzes), tg_id)
                    update('size', str(pizzes_name), tg_id)

                    drink_names = []
                    for r in db_drinks:
                        for d in drink:
                            for cd in count_drink:
                                if r[1]==d.lower():
                                    all_params = {}
                                    all_params['id'] = r[0]
                                    all_params['cnt'] = cd
                                    all_params['name'] = r[1]
                                    total += (int(r[2]) * int(cd))
                                    drink_names.append(all_params)
                    update('drink_id', str(drink_names), tg_id)

                    print(pizza, pizzes)

                    if len(drink)!=len(drink_names) and len(pizza)!=len(pizzes):
                        await dp.send_message(tg_id, texts.not_pizza, parse_mode=ParseMode.HTML)
                        await dp.send_message(tg_id, texts.not_drink, parse_mode=ParseMode.HTML)
                    elif len(pizza)!=len(pizzes):
                        await dp.send_message(tg_id, texts.not_pizza, parse_mode=ParseMode.HTML)
                    elif len(drink)!=len(drink_names):
                        await dp.send_message(tg_id, texts.not_drink, parse_mode=ParseMode.HTML)
                    else:
                        for p_2 in pizza:
                            if p_2=='маргарита':
                                name_1 = 'маргариты'
                                size_20 = InlineKeyboardButton('40 см', callback_data=f'40sm {p_2}')
                                size_40 = InlineKeyboardButton('20 см', callback_data=f'20sm {p_2}')
                                all_size = InlineKeyboardMarkup(row_width=2).add(size_40, size_20)
                                await dp.send_message(tg_id, f"Какой размер для {name_1}", parse_mode=ParseMode.HTML, reply_markup=all_size)

                            elif p_2=='мясная':
                                name_2 = 'мясной'
                                size_20 = InlineKeyboardButton('40 см', callback_data=f'40sm {p_2}')
                                size_40 = InlineKeyboardButton('20 см', callback_data=f'20sm {p_2}')
                                all_size = InlineKeyboardMarkup(row_width=2).add(size_40, size_20)
                                await dp.send_message(tg_id, f"Какой размер для {name_2}", parse_mode=ParseMode.HTML, reply_markup=all_size)

                            elif p_2=='пепперони':
                                name_3 = 'пепперони'
                                size_20 = InlineKeyboardButton('40 см', callback_data=f'40sm {p_2}')
                                size_40 = InlineKeyboardButton('20 см', callback_data=f'20sm {p_2}')
                                all_size = InlineKeyboardMarkup(row_width=2).add(size_40, size_20)
                                await dp.send_message(tg_id, f"Какой размер для {name_3}", parse_mode=ParseMode.HTML, reply_markup=all_size)


            elif drink == []:
                del_drinks(tg_id)
                count_pizza = responseJson['result']['parameters']['count_pizza']
                if size_pizza != []:
                    pizzes_name = {}
                    if count_pizza==['1']:
                        for p, s in zip(pizza, size_pizza):
                            o = []
                            o.append(s)
                            o.append('1')
                            pizzes_name[p] = o
                    else:
                        for p, s, c in zip(pizza, size_pizza, count_pizza):
                            o = []
                            o.append(s)
                            o.append(c)
                            pizzes_name[p] = o
                    
                    pizzes = []
                    for i in db_pizzes:
                        for pz in pizzes_name:
                            if i[1]==pz:
                                prod = {}
                                prod['id'] = str(i[0])
                                prod_2 = {}
                                size_db = eval(i[2])
                                prices_db = eval(i[3])
                                for s_db in size_db:
                                    for cnt in count_pizza:
                                        if s_db==pizzes_name.get(pz)[0]:
                                            prod_2[str(size_db.get(s_db))] = pizzes_name.get(pz)[1]
                                            for price in prices_db:
                                                if s_db==price:
                                                    total += (prices_db.get(price) * int(cnt))
                                prod['mods'] = prod_2
                                pizzes.append(prod)
                    update('pizza_id', str(pizzes), tg_id)
                    update('size', str(pizzes_name), tg_id)

                    if len(pizza)!=len(pizzes):
                        await dp.send_message(tg_id, texts.not_pizza, parse_mode=ParseMode.HTML)
                    else:
                        await dp.send_message(tg_id, texts.size, parse_mode=ParseMode.HTML)
                

                else:
                    pizzes_name = {}
                    if count_pizza==['1']:
                        for p in pizza:
                            o = []
                            o.append(0)
                            o.append('1')
                            pizzes_name[p] = o
                    else:
                        for p, c in zip(pizza, count_pizza):
                            o = []
                            o.append(0)
                            o.append(c)
                            pizzes_name[p] = o

                    pizzes = []
                    for i in db_pizzes:
                        for pz in pizzes_name:
                            if i[1]==pz:
                                prod = {}
                                prod['id'] = str(i[0])
                                prod['cnt'] = str(pizzes_name[pz][1])
                                prod['name'] = pz
                                prod_2 = {}
                                prod['mods'] = prod_2
                                pizzes.append(prod)
                    update('pizza_id', str(pizzes), tg_id)
                    update('size', str(pizzes_name), tg_id)

                    if len(pizza)!=len(pizzes):
                        await dp.send_message(tg_id, texts.not_pizza, parse_mode=ParseMode.HTML)
                    else:
                        for p_2 in pizza:
                            if p_2=='маргарита':
                                name_1 = 'маргариты'
                                size_20 = InlineKeyboardButton('40 см', callback_data=f'40sm {p_2}')
                                size_40 = InlineKeyboardButton('20 см', callback_data=f'20sm {p_2}')
                                all_size = InlineKeyboardMarkup(row_width=2).add(size_40, size_20)
                                await dp.send_message(tg_id, f"Какой размер для {name_1}", parse_mode=ParseMode.HTML, reply_markup=all_size)

                            elif p_2=='мясная':
                                name_2 = 'мясной'
                                size_20 = InlineKeyboardButton('40 см', callback_data=f'40sm {p_2}')
                                size_40 = InlineKeyboardButton('20 см', callback_data=f'20sm {p_2}')
                                all_size = InlineKeyboardMarkup(row_width=2).add(size_40, size_20)
                                await dp.send_message(tg_id, f"Какой размер для {name_2}", parse_mode=ParseMode.HTML, reply_markup=all_size)
                            
                            elif p_2=='пепперони':
                                name_3 = 'пепперони'
                                size_20 = InlineKeyboardButton('40 см', callback_data=f'40sm {p_2}')
                                size_40 = InlineKeyboardButton('20 см', callback_data=f'20sm {p_2}')
                                all_size = InlineKeyboardMarkup(row_width=2).add(size_40, size_20)
                                await dp.send_message(tg_id, f"Какой размер для {name_3}", parse_mode=ParseMode.HTML, reply_markup=all_size)


            elif pizza == []:
                del_pizzes(tg_id)
                count_drink = responseJson['result']['parameters']['count_drink']
                drink_names = []
                for r in db_drinks:
                    for d in drink:
                        for cd in count_drink:
                            if r[1]==d.lower():
                                all_params = {}
                                all_params['id'] = r[0]
                                all_params['cnt'] = cd
                                all_params['name'] = r[1]
                                total += (int(r[2]) * int(cd))
                                drink_names.append(all_params)
                update('drink_id', str(drink_names), tg_id)

                if len(drink)!=len(drink_names):
                    await dp.send_message(tg_id, texts.not_drink, parse_mode=ParseMode.HTML)
                else:
                    await dp.send_message(tg_id, texts.size, parse_mode=ParseMode.HTML)
            else:
                await dp.send_message(tg_id, texts.not_pizza, parse_mode=ParseMode.HTML)


        # # Размер
        # elif intent_name == 'Размер':
        #     size_ai = responseJson['result']['parameters']['size']
        #     pizza_name = event.object.payload.get("type")[5:]
        #     all_pizzes = select_products('pizzes')
        #     pizza_o = eval(order['pizza_id'])
        #     size = eval(order['size'])

        #     dict_size = {}

        #     for po, al in zip(pizza_o, all_pizzes):
        #         if pizza_name==po['name']:
        #             new_prod = {}
        #             new_mods = {}
        #             new_prod['id'] = po['id']
        #             mods_db = eval(al[2])
        #             new_mods[str(mods_db[size_ai])] = po['cnt']
        #             new_prod['mods'] = new_mods
        #             new_pizza_o.append(new_prod)

        #             s = []
        #             s.append(size_ai)
        #             s.append(po['cnt'])
        #             dict_size[po['name']] = s
        #     update('size', str(dict_size), tg_id)

        #     if len(new_pizza_o)==len(pizza_o):
        #         session_api.messages.edit(peer_id=event.obj.peer_id, message=texts_vk.size, conversation_message_id=event.obj.conversation_message_id)
        #         update('pizza_id', str(new_pizza_o), tg_id)
        #         new_pizza_o.clear()
        #     else:
        #         session_api.messages.edit(peer_id=event.obj.peer_id, message='Ок, понял.', conversation_message_id=event.obj.conversation_message_id)


        # Адрес
        elif intent_name == 'Прием адреса':
            await dp.send_message(tg_id, texts.what_phone, reply_markup=btn.full_m, parse_mode=ParseMode.HTML)
            update('address', responseJson['result']['parameters']['adress'], tg_id)


        # Время
        elif intent_name == 'Время доставки':
            order = get_order(tg_id)
            time = responseJson['result']['parameters']['time_ship']

            if time=='как можно быстрее':
                time_half_h = int(time.time()) + 1800
                value_4 = datetime.datetime.fromtimestamp(time_half_h)
                update('time_ship', 'Время доставки: '+value_4.strftime('%H:%M'), tg_id)
                update('time_ship_conf', value_4.strftime('%H:%M'), tg_id)

            elif time=='через 1ч':
                time_1h = int(time.time()) + 3600
                value = datetime.datetime.fromtimestamp(time_1h)
                update('time_ship', 'Время доставки: '+value.strftime('%H:%M'), tg_id)
                update('time_ship_conf', value.strftime('%H:%M'), tg_id)

            elif time=='через 2ч':
                time_2h = int(time.time()) + 7200
                value_2 = datetime.datetime.fromtimestamp(time_2h)
                update('time_ship', 'Время доставки: '+value_2.strftime('%H:%M'), tg_id)
                update('time_ship_conf', value_2.strftime('%H:%M'), tg_id)

            elif time=='через 3ч':
                time_3h = int(time.time()) + 10800
                value_3 = datetime.datetime.fromtimestamp(time_3h)
                update('time_ship', 'Время доставки: '+value_3.strftime('%H:%M'), tg_id)
                update('time_ship_conf', value_3.strftime('%H:%M'), tg_id)

            elif time=='через 4ч':
                time_4h = int(time.time()) + 14400
                value_4 = datetime.datetime.fromtimestamp(time_4h)
                update('time_ship', 'Время доставки: '+value_4.strftime('%H:%M'), tg_id)
                update('time_ship_conf', value_4.strftime('%H:%M'), tg_id)

            else:
                print(responseJson['result']['resolvedQuery'])
                update('time_ship', responseJson['result']['resolvedQuery'], tg_id)
                update('time_ship_conf', f"Время доставки: {responseJson['result']['resolvedQuery']}", tg_id)

            await dp.send_message(tg_id, texts.way_of_pay, reply_markup=btn.pays, parse_mode=ParseMode.HTML)


        # Не понял
        else:
            await dp.send_message(tg_id, texts.not_understand, parse_mode=ParseMode.HTML)


if __name__ == '__main__':
    executor.start_polling(bot, skip_updates=True)
