
"""
Created on Thu Aug 29 10:24:22 2024

@author: timofeevam
"""

Task_6. Write a solution to show the unique ID of each user, If a user does not have a unique ID replace just show null.

Employees table:
+----+----------+
| id | name     |
+----+----------+
| 1  | Alice    |
| 7  | Bob      |
| 11 | Meir     |
| 90 | Winston  |
| 3  | Jonathan |
+----+----------+
EmployeeUNI table:
+----+-----------+
| id | unique_id |
+----+-----------+
| 3  | 1         |
| 11 | 2         |
| 90 | 3         |
+----+-----------+

SELECT unique_id, name
FROM Employees
LEFT JOIN EmployeeUNI
ON Employees.id = EmployeeUNI.id;

Task_7. Write a solution to report the product_name, year, and price for each sale_id in the Sales table.

Table: Sales

+-------------+-------+
| Column Name | Type  |
+-------------+-------+
| sale_id     | int   |
| product_id  | int   |
| year        | int   |
| quantity    | int   |
| price       | int   |
+-------------+-------+
(sale_id, year) is the primary key
 
Table: Product

+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| product_id   | int     |
| product_name | varchar |
+--------------+---------+
product_id is the primary key 

SELECT p.product_name, s.year, s.price
FROM Sales s
JOIN Product p
On s.product_id = p.product_id;

Task_8. Write a solution to find the IDs of the users who visited without making any transactions
and the number of times they made these types of visits.

Visits
+----------+-------------+
| visit_id | customer_id |
+----------+-------------+
| 1        | 23          |
| 2        | 9           |
| 4        | 30          |
| 5        | 54          |
| 6        | 96          |
| 7        | 54          |
| 8        | 54          |
+----------+-------------+
Transactions
+----------------+----------+--------+
| transaction_id | visit_id | amount |
+----------------+----------+--------+
| 2              | 5        | 310    |
| 3              | 5        | 300    |
| 9              | 5        | 200    |
| 12             | 1        | 910    |
| 13             | 2        | 970    |
+----------------+----------+--------+

SELECT v.customer_id, COUNT(v.visit_id) AS count_no_trans
FROM Visits v
LEFT JOIN Transactions t
ON v.visit_id = t.visit_id
WHERE t.transaction_id IS NULL
GROUP BY v.customer_id;

Task_9. Write a solution to find all dates id with higher temperatures compared to its previous dates (yesterday).

Weather table:
+----+------------+-------------+
| id | recordDate | temperature |
+----+------------+-------------+
| 1  | 2015-01-01 | 10          |
| 2  | 2015-01-02 | 25          |
| 3  | 2015-01-03 | 20          |
| 4  | 2015-01-04 | 30          |
+----+------------+-------------+

SELECT w1.id   # Self-Join, where 2 tables are created with w1 - current day, w2 - previous day.
FROM Weather w1
JOIN Weather w2 
ON w1.recordDate = DATE_ADD(w2.recordDate, INTERVAL 1 DAY)
WHERE w1.temperature > w2.temperature;

Task_10. The time to complete a process is the 'end' timestamp minus the 'start' timestamp. 
The average time is calculated by the total time to complete every process on the machine divided by
 the number of processes that were run. The resulting table should have the machine_id along with 
 the average time as processing_time, which should be rounded to 3 decimal places.
 
Activity table:
+------------+------------+---------------+-----------+
| machine_id | process_id | activity_type | timestamp |
+------------+------------+---------------+-----------+
| 0          | 0          | start         | 0.712     |
| 0          | 0          | end           | 1.520     |
| 0          | 1          | start         | 3.140     |
| 0          | 1          | end           | 4.120     |
| 1          | 0          | start         | 0.550     |
| 1          | 0          | end           | 1.550     |
| 1          | 1          | start         | 0.430     |
| 1          | 1          | end           | 1.420     |
| 2          | 0          | start         | 4.100     |
| 2          | 0          | end           | 4.512     |
| 2          | 1          | start         | 2.500     |
| 2          | 1          | end           | 5.000     |
+------------+------------+---------------+-----------+

WITH ProcessTimes AS (
    SELECT machine_id, process_id,
    MAX(CASE WHEN activity_type = 'end' THEN timestamp END) -
    MIN(CASE WHEN activity_type = 'start' THEN timestamp END) AS duration
    FROM Activity
    GROUP BY machine_id, process_id
),
AverageTimes AS (
    SELECT machine_id, AVG(duration) AS average_duration
    FROM ProcessTimes
    GROUP BY machine_id
)
SELECT machine_id, ROUND(average_duration, 3) AS processing_time
FROM AverageTimes

Task_11. Write a solution to report the name and bonus amount of each employee with a bonus less than 1000.

Table: Employee

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| empId       | int     |
| name        | varchar |
| supervisor  | int     |
| salary      | int     |
+-------------+---------+

 
Table: Bonus

+-------------+------+
| Column Name | Type |
+-------------+------+
| empId       | int  |
| bonus       | int  |
+-------------+------+

SELECT e.name, b.bonus
FROM Employee e
LEFT JOIN Bonus b
ON e.empID = b.empID
WHERE b.bonus < 1000 OR b.bonus IS NULL

Task_12. Write a solution to find the number of times each student attended each exam.

Return the result table ordered by student_id and subject_name.

Table: Students

+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| student_id    | int     |
| student_name  | varchar |
+---------------+---------+
 

Table: Subjects

+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| subject_name | varchar |
+--------------+---------+
 

Table: Examinations

+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| student_id   | int     |
| subject_name | varchar |
+--------------+---------+

WITH First_join AS (
    SELECT s.student_id, s.student_name, su.subject_name
    FROM Students s
    CROSS JOIN Subjects su
)
SELECT f.student_id, f.student_name, f.subject_name, COALESCE(COUNT(e.subject_name), 0) AS attended_exams
FROM First_join f
LEFT JOIN Examinations e
ON f.student_id = e.student_id AND f.subject_name = e.subject_name
GROUP BY f.student_id, f.student_name, f.subject_name
ORDER BY f.student_id, f.subject_name;

Task_13.Medium. Write a solution to find managers with at least five direct reports.

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
| department  | varchar |
| managerId   | int     |
+-------------+---------+
id is the primary key (column with unique values) for this table.
Each row of this table indicates the name of an employee, their department, and the id of their manager.
If managerId is null, then the employee does not have a manager.
No employee will be the manager of themself.

WITH Manager AS (
    SELECT managerId
    FROM Employee
    GROUP BY managerId
    HAVING COUNT(managerId) >= 5
)
SELECT e.name
FROM Employee e
JOIN Manager m
ON e.id = m.managerId;

Task_14.Medium. The confirmation rate of a user is the number of 'confirmed' messages divided by the total number of requested confirmation messages. The confirmation rate of a user that did not request any confirmation messages is 0. Round the confirmation rate to two decimal places.
Write a solution to find the confirmation rate of each user.
Return the result table in any order.

Table: Signups

+----------------+----------+
| Column Name    | Type     |
+----------------+----------+
| user_id        | int      |
| time_stamp     | datetime |
+----------------+----------+
 
Table: Confirmations

+----------------+----------+
| Column Name    | Type     |
+----------------+----------+
| user_id        | int      |
| time_stamp     | datetime |
| action         | ENUM     |
+----------------+----------+

WITH First AS (
    SELECT 
        s.user_id, 
        COUNT(c.action) AS total_actions,
        SUM(CASE WHEN c.action = 'confirmed' THEN 1 ELSE 0 END) AS confirmed_actions
    FROM 
        Signups s
    LEFT JOIN 
        Confirmations c ON s.user_id = c.user_id
    GROUP BY 
        s.user_id
)
SELECT 
    f.user_id, 
    ROUND(COALESCE(f.confirmed_actions / NULLIF(f.total_actions, 0), 0), 2) AS confirmation_rate 
FROM 
    First f;