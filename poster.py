import json, requests


URL_POST = 'https://joinposter.com/api/incomingOrders.createIncomingOrder?token=542938:1788976df3f5ac2059cf3f310fc8d3f2'


def poster_pos(pizza, drink, address, phone, time_ship, status):
	pizza_clean = eval(pizza)
	drink_clean = eval(drink)

	products = []
	for p in pizza_clean:
		product = {}
		modifications = []
		mod = {}
		product['product_id'] = p['id']
		count = p.get('mods')
		product['count'] = count[list(count)[0]]
		mod['m'] = list(count)[0]
		mod['a'] = '1'
		modifications.append(mod)
		product['modification'] = modifications
		products.append(product)

	for d in drink_clean:
		product_d = {}
		product_d['product_id'] = d['id']
		product_d['count'] = d['cnt']
		products.append(product_d)


	DATA = {'spot_id': 1,
	'phone': f'{phone}',
	'address': f'{address}', 
	'comment': f'{time_ship}',
	'products': products}

	session = requests.Session()
	formpostdata = session.post(url=URL_POST, json=DATA)
	formpostdataj = formpostdata.json()
	print('Ответ от API:')
	print(formpostdataj)

