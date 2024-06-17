-- Create master_market_db database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS master_market_db;

-- Use the newly created database
USE master_market_db;

-- Create the 'master_user' user with the password 'master_market_pwd'
CREATE USER IF NOT EXISTS 'master_user'@'localhost' IDENTIFIED BY 'master_market_pwd';

-- Grant all privileges on the 'master_market_db' database to the 'master_user' user
GRANT ALL PRIVILEGES ON master_market_db.* TO 'master_user'@'localhost';

-- Flush the privileges to apply the changes
FLUSH PRIVILEGES;

-- Example table creation (if needed)
-- Create a sample table called 'products'
---------------------------------------------
-- CREATE TABLE IF NOT EXISTS products (
--     product_id INT AUTO_INCREMENT PRIMARY KEY,
--     name VARCHAR(255) NOT NULL,
--     description TEXT,
--     price DECIMAL(10, 2) NOT NULL,
--     currency TEXT,
--     stock INT,
--     category TEXT,
--     brand TEXT,
--     images TEXT,
--     attributes TEXT
-- );

-- Create a sample table called 'users'
---------------------------------------------
-- CREATE TABLE IF NOT EXISTS users (
--     user_id INT AUTO_INCREMENT PRIMARY KEY,
--     username VARCHAR(255) UNIQUE NOT NULL,
--     fullname VARCHAR(255) NOT NULL,
--     email VARCHAR(255) UNIQUE NOT NULL,
--     password VARCHAR(255) NOT NULL,
--     image TEXT,
--     cart TEXT,
--     products_added TEXT,
--     favorite TEXT
-- );