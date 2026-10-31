CREATE SCHEMA lab;
CREATE TABLE lab.customers (
  customer_id INTEGER PRIMARY KEY,
  email TEXT NOT NULL UNIQUE
);
CREATE TABLE lab.orders (
  order_id BIGINT PRIMARY KEY,
  customer_id INTEGER NOT NULL REFERENCES lab.customers(customer_id),
  ordered_at TIMESTAMP NOT NULL,
  total_amount NUMERIC(12, 2) NOT NULL CHECK (total_amount >= 0),
  status TEXT NOT NULL CHECK (status IN ('paid', 'pending', 'refunded'))
);
