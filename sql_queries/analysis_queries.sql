-- ===================================================================
-- E-Commerce Sales Analytics SQL Queries
-- Professional Business Intelligence Queries
-- ===================================================================

-- 1. TOP 10 CUSTOMERS BY REVENUE
SELECT 
    c.customer_id,
    c.customer_name,
    c.country,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as total_revenue,
    AVG(o.total_amount) as avg_order_value,
    MAX(o.order_date) as last_purchase_date
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status IN ('Completed', 'Shipped')
GROUP BY c.customer_id, c.customer_name, c.country
ORDER BY total_revenue DESC
LIMIT 10;

-- 2. MONTHLY SALES TREND
SELECT 
    DATE_TRUNC('month', o.order_date)::DATE as month,
    COUNT(o.order_id) as num_orders,
    COUNT(DISTINCT o.customer_id) as unique_customers,
    SUM(o.total_amount) as total_revenue,
    ROUND(AVG(o.total_amount), 2) as avg_order_value
FROM orders o
WHERE o.order_status IN ('Completed', 'Shipped')
GROUP BY DATE_TRUNC('month', o.order_date)
ORDER BY month ASC;

-- 3. TOP 10 PRODUCTS BY SALES
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    COUNT(o.order_id) as times_purchased,
    SUM(o.quantity) as total_quantity,
    SUM(o.total_amount) as total_revenue,
    ROUND(AVG(o.total_amount), 2) as avg_order_value
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.order_status IN ('Completed', 'Shipped')
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_revenue DESC
LIMIT 10;

-- 4. PRODUCT CATEGORY PERFORMANCE
SELECT 
    p.category,
    COUNT(o.order_id) as num_orders,
    SUM(o.total_amount) as total_revenue,
    ROUND(AVG(o.total_amount), 2) as avg_order_value,
    COUNT(DISTINCT o.customer_id) as unique_customers,
    ROUND(100.0 * SUM(o.total_amount) / 
        (SELECT SUM(total_amount) FROM orders WHERE order_status IN ('Completed', 'Shipped')), 2) as revenue_percentage
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.order_status IN ('Completed', 'Shipped')
GROUP BY p.category
ORDER BY total_revenue DESC;

-- 5. RFM ANALYSIS - CUSTOMER SEGMENTATION
SELECT 
    c.customer_id,
    c.customer_name,
    c.country,
    DATEDIFF(day, MAX(o.order_date), CURDATE()) as recency_days,
    COUNT(o.order_id) as frequency,
    SUM(o.total_amount) as monetary_value,
    CASE 
        WHEN DATEDIFF(day, MAX(o.order_date), CURDATE()) <= 30 AND 
             COUNT(o.order_id) >= 3 AND 
             SUM(o.total_amount) >= 500 THEN 'Champions'
        WHEN DATEDIFF(day, MAX(o.order_date), CURDATE()) <= 90 AND 
             COUNT(o.order_id) >= 2 THEN 'Loyal'
        WHEN COUNT(o.order_id) = 1 THEN 'Potential'
        WHEN DATEDIFF(day, MAX(o.order_date), CURDATE()) > 180 THEN 'At-Risk'
        ELSE 'Moderate'
    END as customer_segment
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.order_status IN ('Completed', 'Shipped')
GROUP BY c.customer_id, c.customer_name, c.country
ORDER BY monetary_value DESC;

-- 6. GEOGRAPHIC ANALYSIS
SELECT 
    c.country,
    c.city,
    COUNT(DISTINCT c.customer_id) as num_customers,
    COUNT(o.order_id) as num_orders,
    SUM(o.total_amount) as total_revenue,
    ROUND(AVG(o.total_amount), 2) as avg_order_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.order_status IN ('Completed', 'Shipped')
GROUP BY c.country, c.city
ORDER BY total_revenue DESC;

-- 7. ORDER STATUS DISTRIBUTION
SELECT 
    o.order_status,
    COUNT(o.order_id) as order_count,
    ROUND(100.0 * COUNT(o.order_id) / (SELECT COUNT(*) FROM orders), 2) as percentage,
    SUM(o.total_amount) as total_amount,
    ROUND(AVG(o.total_amount), 2) as avg_order_value
FROM orders o
GROUP BY o.order_status
ORDER BY order_count DESC;

-- 8. CUSTOMER REPEAT PURCHASE RATE
WITH customer_purchases AS (
    SELECT customer_id, COUNT(*) as purchase_count
    FROM orders
    WHERE order_status IN ('Completed', 'Shipped')
    GROUP BY customer_id
)
SELECT 
    'Repeat Customers' as type,
    COUNT(*) as count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM customer_purchases), 2) as percentage
FROM customer_purchases
WHERE purchase_count > 1
UNION ALL
SELECT 
    'One-Time Customers' as type,
    COUNT(*) as count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM customer_purchases), 2) as percentage
FROM customer_purchases
WHERE purchase_count = 1;
