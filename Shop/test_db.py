import sqlite3
import uuid
import traceback
from singleton_decorator import singleton


def check_response(response):
    if response:
        print(response)
        print('Nothing changed.\n')


def connect():
    connector = sqlite3.connect('database.sqlite')
    return connector.cursor(), connector


@singleton
class ShopDB:
    @staticmethod
    def update(field_name, field_value, id_name, id_value):
        cur, connector = connect()
        expr = f'UPDATE SHOPS SET {field_name}=? WHERE {id_name}={id_value}'

        try:
            cur.execute(expr, (field_value,))
        except sqlite3.OperationalError:
            full_traceback = traceback.format_exc()

            return full_traceback
        else:
            connector.commit()
            connector.close()

            return False #False - no errors

    @staticmethod
    def delete(field_name, field_value):
        cur, connector = connect()
        expr = f'DELETE FROM SHOPS WHERE {field_name}=?'

        try:
            cur.execute(expr, (field_value,))
        except sqlite3.OperationalError:
            full_traceback = traceback.format_exc()
            connector.close()

            return full_traceback
        else:
            connector.commit()
            connector.close()

            return False  # False - no errors

    @staticmethod
    def insert(name, address, longitude, latitude):
        cur, connector = connect()
        cur.execute('''INSERT INTO SHOPS(name, address, longitude, latitude) VALUES(?, ?, ?, ?)''',
                    (name, address, longitude, latitude))

        connector.commit()
        connector.close()

    @staticmethod
    def get_last_id():
        cur, connector = connect()
        last_id = cur.execute('''SELECT MAX(shop_id) FROM SHOPS''')

        last = [i for i in last_id]
        connector.close()

        return last[0][0]


@singleton
class GoodsDB:
    @staticmethod
    def update(field_name, field_value, id_name, id_value):
        cur, connector = connect()
        expr = f'UPDATE GOODS SET {field_name}=? WHERE {id_name}={id_value}'

        try:
            cur.execute(expr, (field_value,))
        except sqlite3.OperationalError:
            full_traceback = traceback.format_exc()
            connector.close()

            return full_traceback
        else:
            connector.commit()
            connector.close()

            return False #False - no errors

    @staticmethod
    def delete(field_name, field_value):
        cur, connector = connect()
        expr = f'DELETE FROM GOODS WHERE {field_name}=?'

        try:
            cur.execute(expr, (field_value,))
        except sqlite3.OperationalError:
            full_traceback = traceback.format_exc()
            connector.close()

            return full_traceback
        else:
            connector.commit()
            connector.close()

            return False #False - no errors

    @staticmethod
    def insert(name, barcode):
        cur, connector = connect()
        cur.execute('''INSERT INTO GOODS (name, barcode) VALUES(?, ?)''',
                         (name, barcode))

        connector.commit()
        connector.close()

    @staticmethod
    def get_last_id():
        cur, connector = connect()
        last_id = cur.execute('''SELECT MAX(good_id) FROM GOODS''')

        last = [i for i in last_id]
        connector.close()

        return last[0][0]


@singleton
class GoodsInShopDB:
    @staticmethod
    def update(field_name, field_value, id_name, id_value):
        cur, connector = connect()
        expr = f'UPDATE GoodsInShop SET {field_name}=? WHERE {id_name}={id_value}'

        try:
            cur.execute(expr, (field_value,))
        except sqlite3.OperationalError:
            full_traceback = traceback.format_exc()
            connector.close()

            return full_traceback
        else:
            connector.commit()
            connector.close()

            return False #False - no errors

    @staticmethod
    def delete(field_name, field_value):
        cur, connector = connect()
        expr = f'DELETE FROM GoodsInShop WHERE {field_name}=?'

        try:
            cur.execute(expr, (field_value,))
        except sqlite3.OperationalError:
            full_traceback = traceback.format_exc()
            connector.close()

            return full_traceback
        else:
            connector.commit()
            connector.close()

            return False  # False - no errors

    @staticmethod
    def insert(shop_id, good_id, amount):
        cur, connector = connect()
        cur.execute('''INSERT INTO GoodsInShop (shop_id, good_id, amount) VALUES(?, ?, ?)''',
                         (shop_id, good_id, amount))

        connector.commit()
        connector.close()

    @staticmethod
    def show_shop_info(shop_id):
        cur, connector = connect()
        cur.execute('''SELECT SHOPS.name, GOODS.name, GOODS.barcode, GoodsInShop.amount FROM GoodsInShop
                        JOIN GOODS on GoodsInShop.good_id = GOODS.good_id JOIN SHOPS on GoodsInShop.shop_id = SHOPS.shop_id
                        WHERE SHOPS.shop_id=?''', (shop_id,))

        info = cur.fetchall()
        connector.close()

        refund = []
        for row in info:
            refund.append(row)

        return refund


def shop_control():
    shops = ShopDB()
    shops.insert('male', 'NY', 236, 15)

    response = shops.update('name', 'check', 'shop_id', 1)
    check_response(response)

    response = shops.delete('name', 'vasilek')
    check_response(response)

    print(shops.get_last_id())


def goods_control():
    goods = GoodsDB()
    #goods.insert('nescafe', str(uuid.uuid4()))

    response = goods.delete('good_id', 2)
    check_response(response)

    response = goods.update('name', 'agwhwhg', 'good_id', 4)
    check_response(response)

    print(goods.get_last_id())


def gis_control():
    gis = GoodsInShopDB()
    gis.insert(shop_id=2, good_id=2, amount=15)

    response = gis.delete('amount', 15)
    check_response(response)

    #response = gis.update('good_id', 4, 'shop_id', 1)
    #check_response(response)

    print(gis.show_shop_info(2))


def recreate_tables():
    cur, connector = connect()
    cur.execute('''DROP TABLE SHOPS''')
    cur.execute('''DROP TABLE GOODS''')
    cur.execute('''DROP TABLE GoodsInShop''')

    cur.execute('''CREATE TABLE IF NOT EXISTS SHOPS (
            shop_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(32),
            address VARCHAR(32),
            longitude INTEGER,
            latitude INTEGER
            )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS GOODS (
            good_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(32),
            barcode VARCHAR(36)
            )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS GoodsInShop (
            shop_id INT,
            good_id INT,
            amount INT,
            FOREIGN KEY (shop_id) REFERENCES SHOPS (shop_id),
            FOREIGN KEY (good_id) REFERENCES GOODS (good_id)
            )''')

    connector.commit()
    connector.close()


if __name__ == '__main__':
    #shop_control()
    #goods_control()
    gis_control()
    pass
