SELECT order_id, ordered_at, total_amount
FROM lab.orders
WHERE customer_id = 4242
  AND ordered_at >= TIMESTAMP '2025-06-01'
ORDER BY ordered_at DESC, order_id DESC
LIMIT 20;
