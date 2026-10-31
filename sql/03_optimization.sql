CREATE INDEX idx_orders_customer_recent
  ON lab.orders (customer_id, ordered_at DESC, order_id DESC)
  INCLUDE (total_amount);
ANALYZE lab.orders;
