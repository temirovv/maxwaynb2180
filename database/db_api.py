import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data


    def create_category_table(self):
        sql = """CREATE TABLE IF NOT EXISTS category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255)
        )"""
        self.execute(sql, commit=True)


    def create_products_table(self):
        sql = """CREATE TABLE IF NOT EXISTS product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            weight INTEGER,
            ingredients VARCHAR(255),
            photo VARCHAR(500),
            price REAL,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES category(id)

        )"""
        self.execute(sql, commit=True)

    def create_cart_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS cart (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                total_price REAL, 
                FOREIGN KEY (product_id) REFERENCES product(id)
            )
        """
        self.execute(sql, commit=True)

    def create_user_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS user (
                tg_id INTEGER PRIMARY KEY ,
                username VARCHAR(50),
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                phone_number VARCHAR(15)
            )
        '''
        self.execute(sql, commit=True)

    def create_order_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255),
                pickup_type VARCHAR(100),
                location VARCHAR(255),
                payment_type VARCHAR(30),
                detail TEXT,
                transaction_id VARCHAR(255),
                tg_id INTEGER,
                pickup_location VARCHAR(255),
                payment_status VARCHAR(255) DEFAULT "PENDING",
                created_at DATETIME
        )'''
        self.execute(sql, commit=True)

    # CATEGORY CRUD OPERATIONS
    def add_category(self, name: str) -> None:
        sql = """INSERT INTO category (name) VALUES (?)"""
        self.execute(sql, parameters=(name,), commit=True)
    
    def update_category(self, id: int, new_name: str) -> None:
        sql = '''UPDATE category SET name = ? WHERE id = ?'''
        self.execute(sql, parameters=(new_name, id))

    def delete_category(self, id: int) -> None:
        sql = """DELETE FROM category WHERE id = ?"""
        self.execute(sql, parameters=(id, ), commit=True)
    
    def select_categories(self):
        sql = """SELECT * FROM category"""
        return self.execute(sql, fetchall=True)
    
    def get_category_by_id(self, id: int) -> str:
        sql = "SELECT name FROM category WHERE id = ?"
        return self.execute(sql, parameters=(int(id), ), fetchone=True)

    def check_category(self, name: str) -> bool:
        sql = '''
            SELECT EXISTS(
                SELECT 1 FROM category WHERE name = ?
            );
        '''
        return self.execute(sql, parameters=(name,), fetchone=True)[0]

    # PRODUCT CRUD OPERATIONS
    def add_product(self, name, weight, ingredients, photo, price, category_id):
        sql = '''
        INSERT INTO product 
            (name, weight, ingredients, photo, price, category_id)
        VALUES
            (?, ?, ?, ?, ?, ?)
        '''
        self.execute(sql, (name, weight, ingredients, photo, price, category_id), commit=True)


    def delete_product(self, id):
        sql = """DELETE FROM product FROM id = ?"""
        self.execute(sql, commit=True)
    
    def select_product_by_category(self, category_name: str) -> list:
        sql = """
            SELECT id, name FROM product 
            WHERE category_id = (
                SELECT id FROM category WHERE name = ?
            )
        """
        return self.execute(sql, parameters=(category_name,), fetchall=True)
    
    def select_product_by_name(self, name: str) -> list:
        sql = '''SELECT * FROM product WHERE name = ?'''
        return self.execute(sql, parameters=(name, ), fetchone=True)
    

    def check_product(self, name: str) -> bool:
        sql = '''
            SELECT EXISTS(
                SELECT 1 FROM product WHERE name = ?
            );
        '''
        return self.execute(sql, parameters=(name,), fetchone=True)[0]

    # Cart operations
    def add_to_cart(self, user_id, product_id, total_price, quantity):
        sql = """
            INSERT INTO cart (user_id, product_id, total_price, quantity)
            VALUES (?, ?, ?, ?)
        """    
        self.execute(
            sql, 
            parameters=(
                user_id, product_id, 
                total_price, quantity
            ),
            commit=True
        )

    def select_user_cart(self, user_id: int):
        sql = """
            SELECT 
                cart.id, cart.total_price, 
                cart.quantity, product.name
            FROM cart INNER JOIN product
            ON cart.product_id = product.id
            WHERE cart.user_id = ?
        """
        return self.execute(sql, parameters=(user_id,), fetchall=True)

    def delete_cart_item(self, cart_id):
        sql = '''DELETE FROM cart WHERE id = ?'''
        self.execute(sql, parameters=(cart_id,), commit=True)

    def clear_user_cart(self, user_id):
        sql = '''DELETE FROM cart WHERE user_id = ?'''
        self.execute(sql, parameters=(user_id,), commit=True)

    # USER operations
    def add_user(self, tg_id, first_name, last_name, username):
        sql = '''INSERT INTO user (tg_id, first_name, last_name, username)
        VALUES (?, ?, ?, ?)'''
        self.execute(sql, parameters=(
            tg_id, first_name, last_name, username), 
            commit=True)

    def check_user(self, tg_id: int) -> bool:
        sql = '''
            SELECT EXISTS(
                SELECT 1 FROM user WHERE tg_id = ?
            );
        '''
        return self.execute(sql, parameters=(tg_id,), fetchone=True)[0]

    def select_users_tg_id(self):
        sql = '''SELECT tg_id FROM user'''
        return self.execute(sql, fetchall=True)


    # ORDER operations
    def add_order(self, tg_id, name, pickup_type, 
                  location, detail, payment_type,
                  pickup_location):
        sql = '''
        INSERT INTO orders 
            (tg_id, name, pickup_type, location, detail, 
            payment_type, pickup_location)
        VALUES 
            (?, ?, ?, ?, ?, ?, ?)
            '''
        self.execute(sql, 
                     parameters=(
                         tg_id, name, pickup_type, 
                         location, detail, 
                         payment_type, pickup_location),
                    commit=True)

    def update_order_status(self, status, order_id: int, tg_id, transaction_id: str = None):
        sql = '''UPDATE orders SET status = ?, transaction_id = ? 
        WHERE tg_id = ? AND id = ?'''
        self.execute(sql, 
                     parameters=(status, order_id, tg_id, transaction_id), 
                     commit=True)

    def select_user_orders(self, tg_id):
        sql = '''SELECT '''

def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
    
