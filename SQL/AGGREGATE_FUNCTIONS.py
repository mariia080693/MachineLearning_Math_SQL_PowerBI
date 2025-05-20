
"""
Created on Tue Sep  3 20:54:51 2024

@author: timofeevam
"""

Task_15. Write a solution to report the movies with an odd-numbered ID and a description that is not "boring".
Return the result table ordered by rating in descending order.

Table: Cinema

+----------------+----------+
| Column Name    | Type     |
+----------------+----------+
| id             | int      |
| movie          | varchar  |
| description    | varchar  |
| rating         | float    |
+----------------+----------+

SELECT *
FROM Cinema
WHERE (id MOD 2 != 0) AND (description != 'boring')
ORDER BY rating DESC

Task_16. Write a solution to find the average selling price for each product. average_price should be rounded to 2 decimal places.
Return the result table in any order.

Table: Prices

+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| product_id    | int     |
| start_date    | date    |
| end_date      | date    |
| price         | int     |
+---------------+---------+

Table: UnitsSold

+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| product_id    | int     |
| purchase_date | date    |
| units         | int     |
+---------------+---------+

SELECT 
    p.product_id,
    ROUND(COALESCE(SUM(u.units * p.price) / NULLIF(SUM(u.units), 0), 0), 2) AS average_price # to allow '0' results, SUM can be defined in a separate table
FROM Prices p
LEFT JOIN UnitsSold u
ON 
    p.product_id = u.product_id 
    AND u.purchase_date BETWEEN p.start_date AND p.end_date
GROUP BY 
    p.product_id;

Task_17. Write an SQL query that reports the average experience years of all the employees for each project, rounded to 2 digits.

Table: Project

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| project_id  | int     |
| employee_id | int     |
+-------------+---------+
 

Table: Employee

+------------------+---------+
| Column Name      | Type    |
+------------------+---------+
| employee_id      | int     |
| name             | varchar |
| experience_years | int     |
+------------------+---------+

SELECT p.project_id, ROUND(AVG(e.experience_years), 2) AS 'average_years'
FROM Project p
LEFT JOIN Employee e
ON p.employee_id = e.employee_id
GROUP BY p.project_id

Task_18. Write a solution to find the percentage of the users registered in each contest rounded to two decimals.
Return the result table ordered by percentage in descending order. In case of a tie, order it by contest_id in ascending order.

Table: Users

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| user_id     | int     |
| user_name   | varchar |
+-------------+---------+

Table: Register

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| contest_id  | int     |
| user_id     | int     |
+-------------+---------+

SELECT r.contest_id, ROUND((COUNT(r.user_id) / (SELECT COUNT(*) FROM Users)) * 100, 2) AS percentage
FROM Register r
GROUP BY 
    r.contest_id
ORDER BY 
    percentage DESC, 
    r.contest_id ASC;
    
Task_19. We define query quality as: The average of the ratio between query rating and its position. We also define poor query percentage as:
The percentage of all queries with rating less than 3. Write a solution to find each query_name, the quality and poor_query_percentage.
Both quality and poor_query_percentage should be rounded to 2 decimal places.
Return the result table in any order.  

Table: Queries

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| query_name  | varchar |
| result      | varchar |
| position    | int     |
| rating      | int     |
+-------------+---------+

SELECT query_name, ROUND(AVG(rating/position), 2) AS quality, 
ROUND(SUM(CASE WHEN rating < 3 THEN 1 ELSE 0 END)*100/COUNT(*) , 2) AS poor_query_percentage
FROM Queries
GROUP BY query_name
HAVING query_name IS NOT null 

Task_20. Write an SQL query to find for each month and country, 
the number of transactions and their total amount, 
the number of approved transactions and their total amount.

Table: Transactions

+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| country       | varchar |
| state         | enum    |
| amount        | int     |
| trans_date    | date    |
+---------------+---------+

SELECT 
    DATE_FORMAT(trans_date, '%Y-%m') AS month,
    country,
    COUNT(*) AS trans_count,
    SUM(CASE WHEN state = 'approved' THEN 1 ELSE 0 END) AS approved_count,
    SUM(amount) AS trans_total_amount,
    SUM(CASE WHEN state = 'approved' THEN amount ELSE 0 END) AS approved_total_amount
FROM 
    Transactions
GROUP BY 
    month, country
    
Task_21. If the customers preferred delivery date is the same as the order date, then the order is called immediate; otherwise, it is called scheduled.
The first order of a customer is the order with the earliest order date that the customer made. It is guaranteed that a customer has precisely one first order.
Write a solution to find the percentage of immediate orders in the first orders of all customers, rounded to 2 decimal places.    

Table: Delivery

+-----------------------------+---------+
| Column Name                 | Type    |
+-----------------------------+---------+
| delivery_id                 | int     |
| customer_id                 | int     |
| order_date                  | date    |
| customer_pref_delivery_date | date    |
+-----------------------------+---------+

WITH First AS (
    SELECT 
        customer_id, 
        MIN(order_date) AS first_order_date
    FROM Delivery
    GROUP BY customer_id
)
SELECT 
    ROUND(SUM(CASE WHEN d.order_date = d.customer_pref_delivery_date THEN 1 ELSE 0 END) * 100.0 
/ COUNT(*), 2) AS immediate_percentage
FROM First f
JOIN Delivery d
ON f.customer_id = d.customer_id AND f.first_order_date = d.order_date; 

Task_22. Write a solution to report the fraction of players that logged in again 
on the day after the day they first logged in, rounded to 2 decimal places. 
In other words, you need to count the number of players that logged in for at 
least two consecutive days starting from their first login date, then divide that 
number by the total number of players.

Table: Activity

+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| player_id    | int     |
| device_id    | int     |
| event_date   | date    |
| games_played | int     |
+--------------+---------+

SELECT
  ROUND(COUNT(DISTINCT player_id) / (SELECT COUNT(DISTINCT player_id) FROM Activity), 2) AS fraction
FROM
  Activity
WHERE
  (player_id, DATE_SUB(event_date, INTERVAL 1 DAY))
  IN (
    SELECT player_id, MIN(event_date) AS first_login FROM Activity GROUP BY player_id
  )


