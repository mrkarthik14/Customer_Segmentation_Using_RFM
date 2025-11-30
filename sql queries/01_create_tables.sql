-- create customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(32) PRIMARY KEY,  -- Fixed: TEXT -> VARCHAR(32)
    customer_unique_id VARCHAR(32),       -- Best practice: Limit this as well
    customer_zip_code_prefix VARCHAR(10), -- Zip codes are short
    customer_city VARCHAR(100),
    customer_state VARCHAR(2)             -- States are usually 2 chars (e.g., 'SP')
);

SHOW TABLES;

-- DROP TABLE IF EXISTS orders;

-- create geolocation table
CREATE TABLE IF NOT EXISTS geolocation (
    geolocation_zip_code_prefix VARCHAR(5), -- Olist zip prefixes are 5 digits
    geolocation_lat DECIMAL(18, 15),        -- High precision for coordinates
    geolocation_lng DECIMAL(18, 15),        -- High precision for coordinates
    geolocation_city VARCHAR(100),
    geolocation_state VARCHAR(2)            -- States are 2 chars (e.g., 'SP')
);

-- create orders table , linked with customers table with customer_id
CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(32) PRIMARY KEY,
    customer_id VARCHAR(32),              -- <--- NEEDS COMMA HERE
    order_status VARCHAR(15),
    order_purchase_timestamp DATETIME,
    order_approved_at DATETIME,
    order_delivered_carrier_date DATETIME,
    order_delivered_customer_date DATETIME,
    order_estimated_delivery_date DATETIME, -- <--- NEEDS COMMA HERE

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- create products table
CREATE TABLE IF NOT EXISTS products(
    product_id VARCHAR(32) PRIMARY KEY,
    product_category_name VARCHAR(100),
    product_name_lenght INT,
    product_description_lenght INT,
    product_photos_qty INT,
    product_weight_g INT,
    product_length_cm INT,
    product_height_cm INT,
    product_width_cm INT
);


-- create sellers table
CREATE TABLE IF NOT EXISTS sellers(
    seller_id VARCHAR(32) PRIMARY KEY,
    seller_zip_code_prefix VARCHAR(10),
    seller_city VARCHAR(100),
    seller_state VARCHAR(2)
);

-- create order_items table , linked with orders table with order_id
CREATE TABLE IF NOT EXISTS order_items(
    order_id VARCHAR(32),
    order_item_id INT,
    product_id VARCHAR(32),
    seller_id VARCHAR(32),
    shipping_limit_date DATETIME,
    price DECIMAL(10, 2),
    freight_value DECIMAL(10, 2),
    
    PRIMARY KEY(order_id, order_item_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
);

SHOW TABLES;

-- create order_payments table
CREATE TABLE IF NOT EXISTS order_payments(
    order_id VARCHAR(32),
    payment_sequential INT,
    payment_type VARCHAR(15),
    payment_installments INT,
    payment_value DECIMAL(10, 2),
    
    PRIMARY KEY(order_id, payment_sequential),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
)



-- create order_reviews table
CREATE TABLE IF NOT EXISTS order_reviews(
    order_id VARCHAR(32),
    review_id VARCHAR(32),
    review_score INT,
    review_comment_title VARCHAR(100),
    review_comment_message TEXT,
    review_creation_date DATETIME,
    review_answer_timestamp DATETIME,
    
    PRIMARY KEY(order_id, review_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
)


-- create products_translation table
CREATE TABLE IF NOT EXISTS product_category_name_translation (
    product_category_name VARCHAR(64),
    product_category_name_english VARCHAR(64),

    -- The "Link" is the Portuguese name, not an ID
    PRIMARY KEY (product_category_name)
);