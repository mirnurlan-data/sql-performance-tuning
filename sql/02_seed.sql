-- Fully synthetic and deterministic. BIGINT multiplication avoids integer overflow.
INSERT INTO lab.customers (customer_id, email)
SELECT n, 'customer' || n::text || '@example.test'
FROM generate_series(1, 25000) AS n;

INSERT INTO lab.orders (order_id, customer_id, ordered_at, total_amount, status)
SELECT n::bigint,
       (((n::bigint * 7919) % 25000) + 1)::integer,
       TIMESTAMP '2025-01-01' + (n % 360) * INTERVAL '1 day'
         + ((n::bigint * 13) % 1440) * INTERVAL '1 minute',
       ((n::bigint * 137) % 200000)::numeric / 100,
       CASE WHEN n % 20 = 0 THEN 'refunded'
            WHEN n % 7 = 0 THEN 'pending'
            ELSE 'paid' END
FROM generate_series(1, 400000) AS n;

ANALYZE lab.customers;
ANALYZE lab.orders;
