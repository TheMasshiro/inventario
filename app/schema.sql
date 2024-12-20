CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    store_name TEXT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_inventory (
    inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS suppliers(
    supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    inventory_id INTEGER,
    company_name TEXT NOT NULL,
    supplier_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (inventory_id) REFERENCES user_inventory(inventory_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_id INTEGER NOT NULL,
    inventory_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    supplier_name TEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id) ON DELETE CASCADE,
    FOREIGN KEY (inventory_id) REFERENCES user_inventory(inventory_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS sales(
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    inventory_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    sold INTEGER NOT NULL,
    sale_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (inventory_id) REFERENCES user_inventory(inventory_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS customers(
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    inventory_id INTEGER NOT NULL,
    customer_name TEXT NOT NULL,
    FOREIGN KEY (inventory_id) REFERENCES user_inventory(inventory_id) ON DELETE CASCADE
);

CREATE INDEX idx_user_inventory_user_id ON user_inventory(user_id);
CREATE INDEX idx_product_inventory_id ON products(inventory_id);
CREATE INDEX idx_product_supplier_id ON products(supplier_id);

CREATE INDEX idx_suppliers_inventory_id ON suppliers(inventory_id);
CREATE INDEX idx_suppliers_email ON suppliers(email);
CREATE INDEX idx_suppliers_company_name ON suppliers(company_name);
CREATE INDEX idx_suppliers_status ON suppliers(status);

CREATE INDEX idx_products_product_name ON products(product_name);
CREATE INDEX idx_products_supplier_name ON products(supplier_name);
CREATE INDEX idx_products_last_updated ON products(last_updated);
CREATE INDEX idx_products_stock ON products(stock);

CREATE INDEX idx_sales_inventory_id ON sales(inventory_id);
CREATE INDEX idx_sales_product_id ON sales(product_id);
CREATE INDEX idx_sales_sale_date ON sales(sale_date);

CREATE INDEX idx_customers_inventory_id ON customers(inventory_id);
CREATE INDEX idx_customers_customer_name ON customers(customer_name);

CREATE INDEX idx_products_inv_supplier ON products(inventory_id, supplier_id);
CREATE INDEX idx_sales_inv_date ON sales(inventory_id, sale_date);
CREATE INDEX idx_products_inv_stock ON products(inventory_id, stock);
CREATE INDEX idx_suppliers_inv_status ON suppliers(inventory_id, status);
