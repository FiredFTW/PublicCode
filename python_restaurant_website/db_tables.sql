DROP TABLE IF EXISTS waiter; 

DROP TABLE IF EXISTS tables; 
DROP TABLE IF EXISTS mains; 
DROP TABLE IF EXISTS appertizers; 
DROP TABLE IF EXISTS desserts; 
DROP TABLE IF EXISTS sides;
DROP TABLE IF EXISTS drinks;
DROP TABLE IF EXISTS orders; 

/* Mo's authentication/registration tables.*/
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);


CREATE TABLE waiter (
    id INTEGER PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    password VARCHAR(50) NOT NULL
);


/* Table for the tables number with waiter assigned to table and a VACHAR(5) if it is occupied or not. */
CREATE TABLE tables (
    table_num INTEGER PRIMARY KEY NOT NULL,
    waiter_id INTEGER,
    is_occupied VARCHAR(5) NOT NULL,
    FOREIGN KEY (waiter_id) REFERENCES waiter (waiter_id)
);

/* Table for the mains which have title, allergies and cost */ 
CREATE TABLE mains (
    title VARCHAR(40) PRIMARY KEY NOT NULL,
    vegan VARCHAR(5) NOT NULL, 
    gluten_free VARCHAR(5) NOT NULL,
    vegetarian VARCHAR(5) NOT NULL,
    nuts_free VARCHAR(5) NOT NULL,
    cost INTEGER NOT NULL
);

/* Table for the appertizers. */
CREATE TABLE appertizers (
    title VARCHAR(40) PRIMARY KEY NOT NULL,
    vegan VARCHAR(5) NOT NULL,
    gluten_free VARCHAR(5) NOT NULL,
    vegetarian VARCHAR(5) NOT NULL,
    nuts_free VARCHAR(5) NOT NULL,
    cost INTEGER NOT NULL
);

/* Table for the desserts. */
CREATE TABLE desserts (
    title VARCHAR(40) PRIMARY KEY NOT NULL,
    vegan VARCHAR(5) NOT NULL,
    gluten_free VARCHAR(5) NOT NULL,
    vegetarian VARCHAR(5) NOT NULL,
    nuts_free VARCHAR(5) NOT NULL,
    cost INTEGER NOT NULL
);

CREATE TABLE sides (
    title VARCHAR(40) PRIMARY KEY NOT NULL,
    vegan VARCHAR(5) NOT NULL,
    gluten_free VARCHAR(5) NOT NULL,
    vegetarian VARCHAR(5) NOT NULL,
    nuts_free VARCHAR(5) NOT NULL,
    cost INTEGER NOT NULL
);

/* Table for the drinks. */
CREATE TABLE drinks (
    title VARCHAR(40) PRIMARY KEY NOT NULL,
    cost INTEGER NOT NULL
);

/* Table for the mains where you insert the orders from a table.
There will be multiple rows for the same order this is just a table to store all information for the order.
So if you wanted to know a order you will search the table id and it will show all that was added with relevant table num.
*/
CREATE TABLE orders (
    table_num INTEGER NOT NULL, 
    waiter_id INTEGER NOT NULL,
    appertizers VARCHAR(40),
    mains VARCHAR(40),
    desserts VARCHAR(40),
    sides VARCHAR(40),
    drinks VARCHAR(40),
    notes VARCHAR(100),
    FOREIGN KEY (table_num) REFERENCES tables (table_num),
    FOREIGN KEY (waiter_id) REFERENCES waiter (waiter_id),
    FOREIGN KEY (appertizers) REFERENCES appertizers (title),
    FOREIGN KEY (mains) REFERENCES mains (title),
    FOREIGN KEY (desserts) REFERENCES desserts (title),
    FOREIGN KEY (sides) REFERENCES sides (title),
    FOREIGN KEY (drinks) REFERENCES drinks (title),
    PRIMARY KEY (table_num, waiter_id, appertizers, mains, desserts, sides, drinks)
);

INSERT INTO sides (title, cost, vegan, 
    gluten_free,
    vegetarian,
    nuts_free ) VALUES ('Carne Asada Tacos', 9.95, 'Yes', 'Yes', 'Yes', 'Yes') ; 

INSERT INTO sides (title, cost, vegan, 
    gluten_free,
    vegetarian,
    nuts_free ) VALUES ('Taco Salad', 10.95, 'Yes', 'Yes', 'Yes', 'Yes');

INSERT INTO sides (title, cost, vegan, 
    gluten_free,
    vegetarian,
    nuts_free ) VALUES ('Chicken Fajitas', 13.95, 'Yes', 'Yes', 'Yes', 'Yes') ; 

INSERT INTO sides (title, cost, vegan, 
    gluten_free,
    vegetarian,
    nuts_free ) VALUES ('Sweet Potato Wedges', 5, 'Yes', 'Yes', 'Yes', 'Yes');

INSERT INTO appertizers (title, cost, vegan, 
    gluten_free,
    vegetarian,
    nuts_free ) VALUES ('Cheese Quesadilla', 7.95, 'Yes', 'Yes', 'Yes', 'Yes') ;

INSERT INTO appertizers (title, cost, vegan, 
    gluten_free,
    vegetarian,
    nuts_free ) VALUES ('Loaded Nachos', 8.95, 'Yes', 'Yes', 'Yes', 'Yes');   

INSERT INTO appertizers (title, cost, vegan, 
    gluten_free,
    vegetarian,
    nuts_free ) VALUES ('Grilled Elote', 4.95, 'Yes', 'Yes', 'Yes', 'Yes'); 

INSERT INTO mains (title, cost, vegan, 
    gluten_free,
    vegetarian,
    nuts_free) VALUES ('Chile Relleno', 11.95, 'Yes', 'Yes', 'Yes', 'Yes') ; 

INSERT INTO mains (title, cost,  vegan, 
    gluten_free,
    vegetarian,
    nuts_free) VALUES ('Polo Asado', 13.95, 'Yes', 'Yes', 'Yes', 'Yes'); 

INSERT INTO mains (title, cost,  vegan, 
    gluten_free,
    vegetarian,
    nuts_free) VALUES ('Carnitas', 14.95, 'Yes', 'Yes', 'Yes', 'Yes'); 

INSERT INTO mains (title, cost,  vegan, 
    gluten_free,
    vegetarian,
    nuts_free) VALUES ('Lasagne', 12, 'Yes', 'Yes', 'Yes', 'Yes');

INSERT INTO desserts (title, cost, vegan, 
    gluten_free,
    vegetarian,
    nuts_free ) VALUES ('Ice Cream', 5, 'Yes', 'Yes', 'Yes', 'Yes') ; 

INSERT INTO desserts (title, cost, vegan, 
    gluten_free,
    vegetarian,
    nuts_free ) VALUES ('Chocolate Cake', 2, 'Yes', 'Yes', 'Yes', 'Yes'); 

INSERT INTO desserts (title, cost, vegan, 
    gluten_free,
    vegetarian,
    nuts_free ) VALUES ('Cheese Cake', 2, 'Yes', 'Yes', 'Yes', 'Yes'); 

INSERT INTO drinks (title, cost ) VALUES ('Beer', 2);

INSERT INTO mains (title, cost, vegan, 
    gluten_free,
    vegetarian,
    nuts_free) VALUES 
                ('Beef Taco', 5.99, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Chicken Taco', 5.99, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Veggie Veef Taco', 6.49, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Black Bean Taco', 5.49, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Plain Nachos', 4.99, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Cheesy Nachos', 5.49, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Chilli Nachos', 5.99, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Cheesy Chilli Nachos', 6.49, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Beef Burritos', 7.99, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Chicken Burritos', 7.99, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Veggie Beef Burritos', 8.49, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Breadsticks and Salsa', 3.99, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Avocado Salsa', 4.49, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Sopes', 4.99, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Bean Empanadas', 5.49, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Chicken Flautas', 5.99, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Mixed Bean Chimichangas', 6.99, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Veggie Beef Chilli', 7.49, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Black Bean Chilli', 6.49, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Bean Chilli Nachos', 6.49, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Vegan Chicken Tacos ', 6.49, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Vegan Cheesy Nachos', 5.99, 'Yes', 'Yes', 'Yes', 'Yes'); 

INSERT INTO appertizers (title, cost, vegan, 
    gluten_free,
    vegetarian,
    nuts_free ) VALUES 
                ('Chicken Soup', 4.99, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Mushroom Soup', 4.99, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Tomato Soup', 4.99, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Potato and Leek Soup', 4.99, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Chicken Caeser Salad', 6.99, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Avocado Salad', 5.99, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Mixed Salad', 5.49, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Breadsticks', 2.99, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Black Beans', 3.49, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Red Lentils', 3.49, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Mozerella sticks', 4.49, 'Yes', 'Yes', 'Yes', 'Yes') ; 

INSERT INTO desserts (title, cost, vegan, 
    gluten_free,
    vegetarian,
    nuts_free ) VALUES 
                ('Dulce de Leche', 2.99, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Trro of Ice Cream', 2.99, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Mangonada Sorbet', 2.99, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Vanilla Cheesecake', 2.99, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Chocoflan', 2.99, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Churros', 2.99, 'Yes', 'Yes', 'Yes', 'Yes'),
                ('Champurrado', 2.99, 'Yes', 'Yes', 'Yes', 'Yes') ; 

INSERT INTO drinks (title, cost ) VALUES 
                ('White wine', 2.99), 
                ('Red wine', 2.99), 
                ('Lager', 2.99), 
                ('Mohito', 2.99),
                ('Coca cola', 2.99),  
                ('Diet coke', 2.99),
                ('Lemonade', 2.99),
                ('Still water', 2.99) ;