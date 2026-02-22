-- =============================================
-- DUMMY DATA FOR E-COMMERCE APPLICATION - POSTGRESQL
-- =============================================

-- =============================================
-- 1. INSERT USERS
-- =============================================

INSERT INTO users (name, email, password, phone, role, created_at) VALUES
('John Admin', 'admin@example.com', '$2b$10$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVW', '9876543210', 'admin', NOW()),
('Jane Smith', 'jane@example.com', '$2b$10$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVW', '9876543211', 'user', NOW()),
('Robert Johnson', 'robert@example.com', '$2b$10$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVW', '9876543212', 'user', NOW()),
('Sarah Williams', 'sarah@example.com', '$2b$10$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVW', '9876543213', 'user', NOW()),
('Michael Brown', 'michael@example.com', '$2b$10$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVW', '9876543214', 'user', NOW());

-- =============================================
-- 2. INSERT PRODUCTS
-- =============================================

INSERT INTO products (name, description, price, stock, category, image_url, created_at) VALUES
-- Electronics Category
('Wireless Headphones', 'High-quality wireless headphones with noise cancellation and 30-hour battery life', 129.99, 50, 'Electronics', 'https://via.placeholder.com/300?text=Wireless+Headphones', NOW()),
('USB-C Cable (2m)', 'Durable USB-C charging and data transfer cable, supports fast charging', 15.99, 200, 'Electronics', 'https://via.placeholder.com/300?text=USB-C+Cable', NOW()),
('Portable Power Bank', '20000mAh power bank with dual USB ports and LED display', 39.99, 75, 'Electronics', 'https://via.placeholder.com/300?text=Power+Bank', NOW()),
('Bluetooth Speaker', 'Waterproof portable Bluetooth speaker with 12-hour battery', 59.99, 40, 'Electronics', 'https://via.placeholder.com/300?text=Bluetooth+Speaker', NOW()),
('USB Hub (7-in-1)', 'Multi-port USB hub with HDMI, SD card reader, and 100W power delivery', 49.99, 60, 'Electronics', 'https://via.placeholder.com/300?text=USB+Hub', NOW()),
-- Clothing Category
('Cotton T-Shirt', 'Premium quality 100% cotton t-shirt, comfortable and durable', 24.99, 150, 'Clothing', 'https://via.placeholder.com/300?text=Cotton+T-Shirt', NOW()),
('Denim Jeans', 'Classic blue denim jeans with stretch fit for comfort', 69.99, 100, 'Clothing', 'https://via.placeholder.com/300?text=Denim+Jeans', NOW()),
('Running Shoes', 'Lightweight running shoes with cushioned sole and breathable mesh', 89.99, 80, 'Clothing', 'https://via.placeholder.com/300?text=Running+Shoes', NOW()),
('Winter Jacket', 'Warm winter jacket with water-resistant and insulated lining', 149.99, 40, 'Clothing', 'https://via.placeholder.com/300?text=Winter+Jacket', NOW()),
('Cotton Socks Bundle', 'Pack of 5 pairs of premium cotton socks', 19.99, 200, 'Clothing', 'https://via.placeholder.com/300?text=Socks+Bundle', NOW()),
-- Books Category
('Python Programming Guide', 'Comprehensive guide to Python programming for beginners to advanced', 34.99, 120, 'Books', 'https://via.placeholder.com/300?text=Python+Guide', NOW()),
('Web Development Basics', 'Learn HTML, CSS, and JavaScript from scratch', 29.99, 90, 'Books', 'https://via.placeholder.com/300?text=Web+Dev+Basics', NOW()),
('Data Science Handbook', 'Complete handbook on data analysis, machine learning, and visualization', 44.99, 60, 'Books', 'https://via.placeholder.com/300?text=Data+Science', NOW()),
('Cloud Computing Essentials', 'AWS, Azure, and Google Cloud essentials for cloud engineers', 39.99, 70, 'Books', 'https://via.placeholder.com/300?text=Cloud+Computing', NOW()),
('Artificial Intelligence 101', 'Introduction to AI, machine learning, and neural networks', 49.99, 50, 'Books', 'https://via.placeholder.com/300?text=AI+101', NOW()),
-- Home Category
('LED Desk Lamp', 'Adjustable LED desk lamp with USB charging port and touch control', 35.99, 45, 'Home', 'https://via.placeholder.com/300?text=LED+Lamp', NOW()),
('Cushion Set (4pcs)', 'Decorative cushions set for sofa, waterproof and machine washable', 59.99, 30, 'Home', 'https://via.placeholder.com/300?text=Cushion+Set', NOW()),
('Wall Clock', 'Modern minimalist wall clock with silent movement mechanism', 24.99, 85, 'Home', 'https://via.placeholder.com/300?text=Wall+Clock', NOW()),
('Door Mat', 'Non-slip welcome door mat, durable and easy to clean', 14.99, 150, 'Home', 'https://via.placeholder.com/300?text=Door+Mat', NOW()),
('Storage Organizer', 'Multi-compartment storage organizer for home and office use', 29.99, 60, 'Home', 'https://via.placeholder.com/300?text=Storage+Organizer', NOW());

-- =============================================
-- 3. INSERT ORDERS
-- =============================================

INSERT INTO orders (user_id, total_amount, status, shipping_address, created_at) VALUES
(2, 229.97, 'delivered', '123 Main Street, New York, NY 10001', NOW() - INTERVAL '30 days'),
(3, 179.98, 'shipped', '456 Oak Avenue, Los Angeles, CA 90028', NOW() - INTERVAL '15 days'),
(4, 349.97, 'processing', '789 Pine Road, Chicago, IL 60601', NOW() - INTERVAL '7 days'),
(5, 89.98, 'pending', '321 Elm Street, Houston, TX 77001', NOW() - INTERVAL '2 days'),
(2, 139.98, 'delivered', '123 Main Street, New York, NY 10001', NOW() - INTERVAL '45 days'),
(3, 269.97, 'delivered', '456 Oak Avenue, Los Angeles, CA 90028', NOW() - INTERVAL '60 days');

-- =============================================
-- 4. INSERT ORDER ITEMS
-- =============================================

INSERT INTO order_items (order_id, product_id, quantity, price, created_at) VALUES
-- Order 1 (Jane Smith)
(1, 1, 1, 129.99, NOW() - INTERVAL '30 days'),
(1, 3, 1, 39.99, NOW() - INTERVAL '30 days'),
(1, 2, 1, 15.99, NOW() - INTERVAL '30 days'),

-- Order 2 (Robert Johnson)
(2, 6, 2, 24.99, NOW() - INTERVAL '15 days'),
(2, 10, 1, 19.99, NOW() - INTERVAL '15 days'),
(2, 15, 1, 34.99, NOW() - INTERVAL '15 days'),

-- Order 3 (Sarah Williams)
(3, 8, 1, 89.99, NOW() - INTERVAL '7 days'),
(3, 9, 1, 149.99, NOW() - INTERVAL '7 days'),
(3, 4, 1, 59.99, NOW() - INTERVAL '7 days'),

-- Order 4 (Michael Brown)
(4, 16, 1, 24.99, NOW() - INTERVAL '2 days'),
(4, 15, 1, 29.99, NOW() - INTERVAL '2 days'),
(4, 2, 1, 15.99, NOW() - INTERVAL '2 days'),

-- Order 5 (Jane Smith)
(5, 7, 1, 69.99, NOW() - INTERVAL '45 days'),
(5, 12, 1, 29.99, NOW() - INTERVAL '45 days'),
(5, 2, 1, 15.99, NOW() - INTERVAL '45 days'),
(5, 3, 1, 24.01, NOW() - INTERVAL '45 days'),

-- Order 6 (Robert Johnson)
(6, 7, 1, 69.99, NOW() - INTERVAL '60 days'),
(6, 13, 1, 44.99, NOW() - INTERVAL '60 days'),
(6, 16, 1, 35.99, NOW() - INTERVAL '60 days'),
(6, 19, 1, 14.99, NOW() - INTERVAL '60 days'),
(6, 5, 1, 49.99, NOW() - INTERVAL '60 days');
