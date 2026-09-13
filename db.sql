CREATE DATABASE IF NOT EXISTS campus_food;
USE campus_food;

CREATE TABLE IF NOT EXISTS food_menu (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description VARCHAR(255),
    price DECIMAL(10,2) NOT NULL,
    available TINYINT(1) DEFAULT 1
);

INSERT INTO food_menu (name, category, description, price) VALUES
('Chicken Rice', 'Main Meal', 'Chicken rice with vegetables', 6.00),
('Nasi Lemak', 'Main Meal', 'Nasi lemak with egg and sambal', 5.00),
('Fried Noodles', 'Main Meal', 'Fried noodles with vegetables', 5.50),
('Iced Milo', 'Beverage', 'Cold Milo drink', 2.50),
('Mineral Water', 'Beverage', 'Bottled mineral water', 1.50);