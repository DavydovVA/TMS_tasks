from classes import *
from test_db import recreate_tables
	
if __name__ == '__main__':
	recreate_tables()

	shop_1 = Shop('c. Mushroom, st. Circle_8, № 667', 'Vasilek')
	shop_2 = Shop('c. Bread, st. Sand, № 665', 'Brick')
	shop_3 = Shop('c. Snake, st. Mega_Large, № 1337', 'Happines')
	
	tea = Tea('chacha')
	tea.set_price(3.50)

	shop_1.add_product(tea, 15)
	shop_2.add_product(tea, 101)
	shop_3.add_product(tea, 5)

	shop_1.sale_product('chacha', 8)
	shop_2.sale_product('chacha', 66)
	shop_3.sale_product('chacha', 1)

	print('Shop 1: ', shop_1.goods)
	print('Shop 2: ', shop_2.goods)
	print('Shop 3: ', shop_3.goods)

	print('\nEarnings:')
	Shop.print_earnings(0)
	Shop.print_earnings(1)
	
	#Shop.show_map()
