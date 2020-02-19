from matplotlib import pyplot as plt
from random import randint
from math import sqrt
from abc import ABC
import uuid
import re
from singleton_decorator import singleton
from test_db import ShopDB, GoodsDB, GoodsInShopDB


shopDB = ShopDB()
goodsDB = GoodsDB()
gis = GoodsInShopDB()


class StrValue(Exception):
	pass

	
class NegativeValue(Exception):
	pass


class NegativeLimit(Exception):
	pass


class Address:
		def __init__(self, address):
			regex = re.compile(r'c\. ([\w]+), st\. ([\w]+), \№ ([0-9]+)')
			string = regex.findall(address)
			
			self.city = string[0][0]
			self.street = string[0][1]
			self.building = string[0][2]
			
			self.x = randint(0, 250)
			self.y = randint(0, 250)

		def __lt__(self, other):
			if isinstance(other, Address):
				return self.distance() < other.distance()
			
		def distance(self):
			return sqrt(self.x**2 + self.y**2)
			
		def get_coord(self):
			return [self.x, self.y]
			
		def show(self):
			print(self.city)
			print(self.street)
			print(self.building)


class Money:
	def __init__(self):
		self.total_money = 0
		self.shops_money = dict()
		
	def increase(self, shop, value):
		self.total_money += value
		if shop in self.shops_money.keys():
			self.shops_money[shop] += value
		else:
			self.shops_money[shop] = 0
			self.shops_money[shop] += value
			

class Shop(Address):
	_shops = []
	_money = Money()

	def __init__(self, address, name):
		super().__init__(address)
		
		self.name = name.lower()
		self.full_address = address.lower()
		self.goods = dict()

		shopDB.insert(self.name, self.full_address, self.x, self.y)
		self.shop_id = shopDB.get_last_id()

		self.__class__._shops.append(self)

	def add_product(self, product, amount):
		if amount < 0:
			raise NegativeValue('An amount value of added must be positive.')
		if type(amount) == str:
			raise StrValue('Amount value must be a number, not string.')
			
		product + amount
		if product.name not in self.goods:
			self.goods[product.name] = [product, amount]
			gis.insert(self.shop_id, product.good_id, amount)
		else:
			value = self.goods[product.name][1]
			total = value + amount
			self.goods[product.name] = [product, total]
			gis.update('amount', total, 'shop_id', self.shop_id)
	
	def sale_product(self, name, amount):
		name = name.lower()
		if name in self.goods.keys() and self.goods[name][1] != 0:
			if amount > self.goods[name][1]:
				self._calculate(self.goods[name][1], name)
			else:
				self._calculate(amount, name)
			gis.update('amount', self.goods[name][1], 'shop_id', self.shop_id)
		else:
			return self._search_nearest(name)
	
	#Lesson 11
	@staticmethod
	def show_map():
		names, x, y = [], [], []
		for shop in __class__._shops:
			names.append(shop.name)
			coord = shop.get_coord()
			x.append(coord[0])
			y.append(coord[1])
			
		borders = [0, 255]
		
		for i in range(len(names)):
			plt.annotate(f'{names[i].title()}\n({x[i]},{y[i]})',(x[i]-5, y[i]+5), fontsize=10)
			
		plt.scatter(x, y, c='red') #разный цвет сделать
		plt.scatter(borders, borders, c='white') #задает границы области, чтоб красивее было
		plt.scatter(0, 0, c='blue')
		plt.annotate(f'You\n({0},{0})', (0-3, 0+5), fontsize=10)
		plt.axis('off')
		plt.show()

	def _search_nearest(self, name):
		shops_with = [shop for shop in self.__class__._shops 
				if name in shop.goods.keys() and shop.goods[name][1] != 0]
		if shops_with:
			print(f"Nearest shop with {name.title()} is {min(shops_with).name.title()}")
			return min(shops_with)
		else:
			print(f'There are no shops with {name.title()}')
			return 0
			
	def _calculate(self, value, name):
		self.goods[name][0] - value
		self.__class__._money.increase(self, value * self.goods[name][0].get_price())
		self.goods[name][1] -= value
	
	@staticmethod
	def print_earnings(arg):
		'''0 - by shops, 1 - total'''
		if arg == 0 and __class__._money.shops_money:
			[print(f'{shop.name.title()}: {money} points')
					for shop, money in __class__._money.shops_money.items()]
		elif arg == 1:
			print(f'Total: {__class__._money.total_money} points')
		elif type(arg) == Shop and arg in __class__._money.shops_money:
			name = arg.name
			print(f'{name.title()}: {__class__._money.shops_money[arg]} points')
		else:
			print('The shop you are interested in has no sales history.')


class Goods(ABC):
	_price = 0
	_count = 0

	def get_price(self):
		return self._price

	def set_price(self, value):
		if type(value) == str:
			raise StrValue("Price value must be a number, not string.")
		if value <= 0:
			raise NegativeValue("Price value must be positive.")
			
		setattr(self, '_price', value)
		
	def get_count(self):
		return self._count

	def __add__(self, value):
		if type(value) == str:
			raise StrValue("Quantity value must be a number, not string.")	
		if self._count + value < 0:
			raise NegativeLimit('Out of range.')
		
		self._count += value
		
	def __sub__(self, value):
		self._count -= value


@singleton
class Tea(Goods):
	def __init__(self, name):
		self.name = name
		self.barcode = str(uuid.uuid4())

		goodsDB.insert(self.name, self.barcode)

		self.good_id = goodsDB.get_last_id()
		
	def __str__(self):
		return self.name


if __name__ == '__main__':
	tea1 = Tea('lipton')

	shop1 = Shop('c. Bread, st. Sand, № 665', 'Frish')
	shop1.add_product(tea1, 25)
	shop1.sale_product('lipton', 13)

	shop2 = Shop('c. Mem, st. Sad_cat, № 768', 'Kektus')
	shop2.add_product(tea1, 134)
	shop2.sale_product('lipton', 100)
