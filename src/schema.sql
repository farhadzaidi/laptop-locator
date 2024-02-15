/*

Enter NULL for unspecified fields.

*/

CREATE TABLE Laptop (
    laptop_id INT PRIMARY KEY,
    cpu_brand VARCHAR(255),
    cpu_name VARCHAR(255),
    cpu_core_ct INT,
    cpu_core_clock DECIMAL(2, 1),
    gpu_brand VARCHAR(255),
    gpu_name VARCHAR(255),
    gpu_mem INT,
    ram_size INT,
    ram_type VARCHAR(255),
    storage_size INT,
    storage_type VARCHAR(255),
    screen_res VARCHAR(255),
    screen_refresh_rate INT,
    screen_size DECIMAL(3, 1),
    screen_type VARCHAR(255),
    has_webcam INT,
    operating_system VARCHAR(255),
);