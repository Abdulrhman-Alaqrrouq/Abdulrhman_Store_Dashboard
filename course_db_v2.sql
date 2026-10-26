-- ======================================
-- Data Analysis Diploma - SQL Course
-- course_db  (version 2)
-- MySQL 8.0
--
-- Run the whole file once (Ctrl+Shift+Enter in MySQL Workbench),
-- then press the refresh icon in the SCHEMAS panel.
--
-- Same 6 tables and columns as version 1. Added rows only:
--   - 2 customers with no sales (one has a NULL signup_date)
--   - 1 product that was never sold (Monitor)
--   - 1 new Sales employee with no sales yet
--   - 13 extra sales so the data covers Feb 2024 - Mar 2025
-- ======================================

DROP DATABASE IF EXISTS course_db;
CREATE DATABASE course_db;
USE course_db;

-- ======================================
-- COUNTRY TABLE
-- ======================================
CREATE TABLE country (
    country_id INT PRIMARY KEY,
    country_name VARCHAR(50)
);

INSERT INTO country VALUES
(1, 'Jordan'),
(2, 'Saudi Arabia'),
(3, 'UAE'),
(4, 'Egypt'),
(5, 'Qatar');

-- ======================================
-- CITY TABLE
-- ======================================
CREATE TABLE city (
    city_id INT PRIMARY KEY,
    city_name VARCHAR(50),
    country_id INT,
    FOREIGN KEY (country_id) REFERENCES country(country_id)
);

INSERT INTO city VALUES
(1, 'Amman', 1),
(2, 'Irbid', 1),
(3, 'Riyadh', 2),
(4, 'Jeddah', 2),
(5, 'Dubai', 3),
(6, 'Cairo', 4),
(7, 'Alexandria', 4),
(8, 'Doha', 5);

-- ======================================
-- CUSTOMER TABLE
-- ======================================
CREATE TABLE customer (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    gender VARCHAR(10),
    city_id INT,
    signup_date DATE,
    FOREIGN KEY (city_id) REFERENCES city(city_id)
);

INSERT INTO customer VALUES
(1, 'Ahmad Ali', 'Male', 1, '2024-01-15'),
(2, 'Sara Khaled', 'Female', 2, '2024-02-10'),
(3, 'Mohammad Saleh', 'Male', 3, '2024-03-05'),
(4, 'Lina Hassan', 'Female', 5, '2024-03-20'),
(5, 'Omar Nasser', 'Male', 1, '2024-04-01'),
(6, 'Hassan Mahmoud', 'Male', 6, '2024-04-10'),
(7, 'Reem Fawzi', 'Female', 7, '2024-05-02'),
(8, 'Abdullah Saeed', 'Male', 8, '2024-05-18'),
(9, 'Dana Yazan', 'Female', 3, '2024-06-05'),
(10, 'Tariq Adel', 'Male', 4, '2024-06-20'),
(11, 'Yara Sami', 'Female', 2, '2024-07-12'),   -- registered, never bought
(12, 'Fadi Nabil', 'Male', 5, NULL);            -- signup date missing (NULL)

-- ======================================
-- PRODUCT TABLE
-- ======================================
CREATE TABLE product (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2)
);

INSERT INTO product VALUES
(1, 'Laptop', 'Electronics', 900.00),
(2, 'Mobile Phone', 'Electronics', 600.00),
(3, 'Headphones', 'Accessories', 80.00),
(4, 'Office Chair', 'Furniture', 150.00),
(5, 'Wireless Mouse', 'Accessories', 35.00),
(6, 'Desk Lamp', 'Furniture', 45.00),
(7, 'Tablet', 'Electronics', 400.00),
(8, 'Monitor', 'Electronics', 250.00),          -- never sold
(9, 'Keyboard', 'Accessories', 25.00);

-- ======================================
-- EMPLOYEE TABLE
-- ======================================
CREATE TABLE employee (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100),
    department VARCHAR(50),
    hire_date DATE
);

INSERT INTO employee VALUES
(1, 'Khaled Ahmad', 'Sales', '2022-01-01'),
(2, 'Noor Samir', 'Sales', '2023-05-10'),
(3, 'Yousef Omar', 'Support', '2021-09-15'),
(4, 'Maha Zaid', 'Sales', '2022-11-01'),
(5, 'Ali Rami', 'Support', '2023-02-20'),
(6, 'Salma Hani', 'Logistics', '2024-01-15'),
(7, 'Rania Tarek', 'Sales', '2024-06-01');      -- new hire, no sales yet

-- ======================================
-- SALES TABLE   (total_amount = quantity * product price)
-- ======================================
CREATE TABLE sales (
    sale_id INT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    employee_id INT,
    sale_date DATE,
    quantity INT,
    total_amount DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

INSERT INTO sales VALUES
(1, 1, 1, 1, '2024-05-01', 1, 900.00),
(2, 2, 2, 2, '2024-05-03', 1, 600.00),
(3, 3, 3, 1, '2024-05-10', 2, 160.00),
(4, 4, 4, 2, '2024-06-01', 1, 150.00),
(5, 1, 2, 1, '2024-06-15', 1, 600.00),
(6, 5, 1, 2, '2024-07-01', 1, 900.00),
(7, 6, 5, 1, '2024-07-05', 2, 70.00),
(8, 7, 6, 4, '2024-07-10', 1, 45.00),
(9, 8, 7, 2, '2024-07-15', 1, 400.00),
(10, 9, 3, 1, '2024-08-01', 3, 240.00),
(11, 10, 1, 4, '2024-08-05', 1, 900.00),
(12, 2, 5, 2, '2024-08-10', 2, 70.00),
(13, 3, 2, 4, '2024-08-18', 1, 600.00),
(14, 4, 7, 1, '2024-09-01', 1, 400.00),
(15, 5, 6, 6, '2024-09-10', 2, 90.00),
(16, 1, 3, 1, '2024-02-05', 1, 80.00),
(17, 2, 4, 2, '2024-03-12', 1, 150.00),
(18, 3, 9, 4, '2024-04-20', 2, 50.00),
(19, 4, 1, 2, '2024-10-03', 1, 900.00),
(20, 7, 2, 1, '2024-10-21', 1, 600.00),
(21, 9, 5, 4, '2024-11-08', 3, 105.00),
(22, 4, 6, 6, '2024-11-25', 1, 45.00),
(23, 9, 7, 1, '2024-12-02', 1, 400.00),
(24, 5, 3, 2, '2024-12-18', 2, 160.00),
(25, 1, 9, 4, '2025-01-09', 4, 100.00),
(26, 5, 2, 1, '2025-01-27', 1, 600.00),
(27, 3, 7, 2, '2025-02-14', 1, 400.00),
(28, 2, 1, 4, '2025-03-06', 1, 900.00);
