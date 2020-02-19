CREATE TABLE IF NOT EXISTS SHOPS (
    shop_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(32),
    address VARCHAR(32),
    longitude INTEGER,
    latitude INTEGER
);

INSERT INTO SHOPS (name, address, longitude, latitude) VALUES
    ('vasilek', 'Minsk', 255, 134),
    ('vasilek', 'Minsk', 18, 137),
    ('vasilek', 'Minsk', 200, 276),
    ('vasilek', 'Minsk', 333, 222);

SELECT * FROM SHOPS;
UPDATE SHOPS SET longitude=0 WHERE shop_id=1;


CREATE TABLE IF NOT EXISTS GOODS (
    good_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(32),
    barcode VARCHAR(36)
);

INSERT INTO GOODS (name, barcode) VALUES
    ('lipton', '1245-qgqq-1245-qwrtgqqgg');

SELECT * FROM GOODS;

CREATE TABLE IF NOT EXISTS GoodsInShop (
    shop_id INT,
    good_id INT,
    amount INT,
    FOREIGN KEY (shop_id) REFERENCES SHOPS (shop_id),
    FOREIGN KEY (good_id) REFERENCES GOODS (good_id)
);

INSERT INTO GoodsInShop (shop_id, good_id, amount) VALUES
    (3, 4, 25),
    (1, 2, 10);

SELECT * FROM GoodsInShop;

SELECT SHOPS.name, GOODS.name, GOODS.barcode, GoodsInShop.amount FROM GoodsInShop
    JOIN GOODS on GoodsInShop.good_id = GOODS.good_id JOIN SHOPS on GoodsInShop.shop_id = SHOPS.shop_id
    WHERE SHOPS.shop_id = 1;