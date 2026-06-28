-- ===================================================================
-- Advanced Analytics Queries
-- Complex SQL for Strategic Decision-Making
-- ===================================================================

-- 1. CHURN ANALYSIS - At-Risk Customers
SELECT 
    c.customer_id,
    c.customer_name,
    c.country,
    MAX(o.order_date) as last_purchase_date,
    DATEDIFF(day, MAX(o.order_date), CURDATE()) as days_since_purchase,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as lifetime_value,
    CASE 
        WHEN DATEDIFF(day, MAX(o.order_date), CURDATE()) > 180 THEN 'Churned'
        WHEN DATEDIFF(day, MAX(o.order_date), CURDATE()) > 120 THEN 'At Risk'
        ELSE 'Active'
    END as status
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.order_status IN ('Completed', 'Shipped')
GROUP BY c.customer_id, c.customer_name, c.country
ORDER BY days_since_purchase DESC;

-- 2. CUSTOMER LIFETIME VALUE DISTRIBUTION
WITH customer_clv AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        SUM(o.total_amount) as clv
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.order_status IN ('Completed', 'Shipped')
    GROUP BY c.customer_id, c.customer_name
)
SELECT 
    CASE 
        WHEN clv >= 2000 THEN 'High Value (2000+)'
        WHEN clv >= 1000 THEN 'Medium Value (1000-2000)'
        WHEN clv >= 500 THEN 'Low-Medium Value (500-1000)'
        ELSE 'Low Value (<500)'
    END as clv_segment,
    COUNT(*) as num_customers,
    ROUND(AVG(clv), 2) as avg_clv,
    ROUND(SUM(clv), 2) as segment_revenue
FROM customer_clv
GROUP BY clv_segment
ORDER BY avg_clv DESC;

-- 3. PRODUCT AFFINITY - What Products Are Bought Together
SELECT 
    p1.product_name as product_1,
    p2.product_name as product_2,
    COUNT(*) as co_purchase_count
FROM orders o1
JOIN products p1 ON o1.product_id = p1.product_id
JOIN orders o2 ON o1.customer_id = o2.customer_id 
    AND o1.order_date = o2.order_date 
    AND o1.order_id < o2.order_id
JOIN products p2 ON o2.product_id = p2.product_id
WHERE o1.order_status IN ('Completed', 'Shipped') 
    AND o2.order_status IN ('Completed', 'Shipped')
GROUP BY p1.product_id, p1.product_name, p2.product_id, p2.product_name
ORDER BY co_purchase_count DESC
LIMIT 15;

-- 4. AOV PROGRESSION - Average Order Value Over Time
SELECT 
    DATE_TRUNC('month', o.order_date)::DATE as month,
    ROUND(AVG(o.total_amount), 2) as avg_order_value,
    ROUND(STDDEV(o.total_amount), 2) as stddev_order_value,
    MIN(o.total_amount) as min_order,
    MAX(o.total_amount) as max_order,
    COUNT(o.order_id) as orders_count
FROM orders o
WHERE o.order_status IN ('Completed', 'Shipped')
GROUP BY DATE_TRUNC('month', o.order_date)
ORDER BY month DESC;
