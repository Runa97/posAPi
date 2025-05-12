-- Users Table
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    password VARCHAR(120) NOT NULL,
    role VARCHAR(20) NOT NULL
);

-- Product Categories Table
CREATE TABLE product_category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(80) UNIQUE NOT NULL
);

-- Products Table
CREATE TABLE product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    category_id INTEGER NOT NULL,
    stock INTEGER DEFAULT 0,
    price FLOAT NOT NULL,
    seller_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES product_category(id),
    FOREIGN KEY (seller_id) REFERENCES user(id)
);

-- Orders Table
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    paid BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (customer_id) REFERENCES user(id)
);

-- Order Items Table
CREATE TABLE order_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price FLOAT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES product(id)
);

-- Reviews Table
CREATE TABLE review (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    content VARCHAR(200),
    FOREIGN KEY (product_id) REFERENCES product(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- Inventory Table
CREATE TABLE inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    quantity_change INTEGER NOT NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES product(id)
);

-- Example Data Insertions (Optional)
-- Insert Users
INSERT INTO user (username, password, role) VALUES
('admin_user', 'hashed_password_1', 'admin'),
('seller_user', 'hashed_password_2', 'seller'),
('customer_user', 'hashed_password_3', 'customer');

-- Insert Product Categories
INSERT INTO product_category (name) VALUES
('Electronics'),
('Clothing'),
('Books'),
('Furniture'),
('Toys');

-- Insert Products
INSERT INTO product (name, category_id, stock, price, seller_id) VALUES
('Smartphone', 1, 100, 299.99, 1),
('Laptop', 1, 50, 999.99, 1),
('T-Shirt', 2, 200, 19.99, 2),
('Sofa', 4, 10, 499.99, 2),
('Action Figure', 5, 150, 14.99, 2);
