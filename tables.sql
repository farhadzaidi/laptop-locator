CREATE TABLE laptop_T (
    laptop_id INT PRIMARY KEY,
    model_number VARCHAR(255),
    brand VARCHAR(50),
    screen_size DECIMAL(4,2),
    cpu_brand VARCHAR(255),
    cpu VARCHAR(50),
    gpu VARCHAR(50),
    storage_type VARCHAR(50),
    storage_amount INT,
    ram_type VARCHAR(50),
    ram_amount INT,
    battery_life DECIMAL(5,2)
);
CREATE TABLE retailer_T (
    retailer_id INT PRIMARY KEY,
    name VARCHAR(255),
    website VARCHAR(255)
);
CREATE TABLE price_T (
    price_id INT PRIMARY KEY,
    laptop_id INT,
    retailer_id INT,
    price DECIMAL(10, 2),
    recorded_date DATE,
    FOREIGN KEY (laptop_id) REFERENCES laptop_T(laptop_id),
    FOREIGN KEY (retailer_id) REFERENCES retailer_T(retailer_id)
);

drop table laptop_T;

-- Inserting data into the laptop_T table
INSERT INTO laptop_T VALUES
(1, 'ABC123', 'Dell', 15.6, 'Intel', 'i5', 'Nvidia GTX 1050', 'SSD', 256, 'DDR4', 8, 6.5, 'BestBuy'),
(2, 'XYZ789', 'HP', 14.0, 'AMD', 'Ryzen 7', 'AMD Radeon RX Vega 10', 'HDD', 1, 'DDR4', 16, 8.0, 'Amazon'),
(3, 'LPT456', 'Lenovo', 13.3, 'Intel', 'i7', 'Intel UHD Graphics 620', 'SSD', 512, 'DDR4', 16, 10.0, 'Newegg'),
(3, 'LPT456', 'Lenovo', 13.3, 'Intel', 'i7', 'Intel UHD Graphics 620', 'SSD', 512, 'DDR4', 16, 10.0, 'BestBuy');

-- Inserting data into the retailer_T table
INSERT INTO retailer_T VALUES
(1, 'BestBuy', 'https://www.bestbuy.com'),
(2, 'Amazon', 'https://www.amazon.com'),
(3, 'Newegg', 'https://www.newegg.com');

-- Inserting data into the price_T table
INSERT INTO price_T VALUES
(1, 1, 1, 799.99, '2024-02-11'),
(2, 1, 2, 749.99, '2024-02-11'),
(3, 2, 2, 899.99, '2024-02-11'),
(4, 2, 3, 789.99, '2024-02-11'),
(5, 3, 1, 1099.99, '2024-02-11'),
(6, 3, 3, 999.99, '2024-02-11');
