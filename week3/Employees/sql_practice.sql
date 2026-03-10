-- Create database
CREATE DATABASE sql_practice;
--\c sql_practice

-- Create tables
CREATE TABLE departments (
    dept_id SERIAL PRIMARY KEY,
    dept_name VARCHAR(50) NOT NULL,
    location VARCHAR(100),
    budget DECIMAL(12, 2)
);

CREATE TABLE employees (
    emp_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    hire_date DATE DEFAULT CURRENT_DATE,
    salary DECIMAL(10, 2),
    dept_id INTEGER REFERENCES departments(dept_id)
);

CREATE TABLE projects (
    project_id SERIAL PRIMARY KEY,
    project_name VARCHAR(100) NOT NULL,
    start_date DATE,
    end_date DATE,
    budget DECIMAL(12, 2),
    dept_id INTEGER REFERENCES departments(dept_id)
);

-- Insert sample data
INSERT INTO departments (dept_name, location, budget) VALUES
('Engineering', 'Building A', 500000),
('Sales', 'Building B', 300000),
('Marketing', 'Building C', 200000),
('HR', 'Building D', 150000);

INSERT INTO employees (first_name, last_name, email, hire_date, salary, dept_id) VALUES
('Alice', 'Johnson', 'alice@company.com', '2020-03-15', 85000, 1),
('Bob', 'Smith', 'bob@company.com', '2019-07-01', 72000, 1),
('Carol', 'Williams', 'carol@company.com', '2021-01-10', 65000, 2),
('David', 'Brown', 'david@company.com', '2018-11-20', 90000, 1),
('Eve', 'Davis', 'eve@company.com', '2022-05-01', 55000, 3),
('Frank', 'Miller', 'frank@company.com', '2020-09-15', 78000, 2),
('Grace', 'Wilson', 'grace@company.com', '2021-06-01', 62000, 4),
('Henry', 'Taylor', 'henry@company.com', '2019-03-01', 95000, 1);

INSERT INTO projects (project_name, start_date, end_date, budget, dept_id) VALUES
('Website Redesign', '2024-01-01', '2024-06-30', 50000, 3),
('Mobile App', '2024-02-15', '2024-12-31', 150000, 1),
('Sales Portal', '2024-03-01', '2024-09-30', 75000, 2),
('HR System', '2024-04-01', '2024-08-31', 40000, 4);

SELECT * FROM departments;
SELECT * FROM employees;
SELECT * FROM projects;

--PART 1: DDL PRACTICE
--TASK 1.1: ADD A COLUMN
ALTER TABLE employees ADD COLUMN phone VARCHAR(20);

--TASK 1.2: MODIFY A COLUMN
ALTER TABLE departments ALTER COLUMN budget TYPE DECIMAL(15,2);

--TASK 1.3: CREATE A NEW TABLE
CREATE TABLE training_courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    duration_hours INTEGER,
    instructor VARCHAR(100)
)

--PART 2: DML PRACTICE
--TASK 2.1: INSERT OPERATIONS
INSERT INTO employees (first_name, last_name, email, salary, dept_id)
VALUES
('Grace', 'Lee', 'grace.lee@company.com', 58000, 4),
('Ivan', 'Chen', 'ivan@company.com', 61000, 4),
('Julia', 'Kim', 'julia@company.com', 55000, 4);

--TASK 2.2: UPDATE OPERATIONS
UPDATE employees SET salary = salary * 1.10 WHERE dept_id = 1;
UPDATE employees SET email = 'bob.smith@company.com' WHERE first_name = 'Bob' AND last_name = 'Smith'

--TASK 2.3: DELETE OPERATIONS
DELETE FROM projects WHERE end_date < CURRENT_DATE;
DELETE FROM employees WHERE dept_id IS NULL;

--PART 3: DQL PRACTICE
--QUERY 3.1: LIST ALL EMPLOYEES ORDERED BY SALARY (HIGHEST FIRST)
SELECT * FROM employees ORDER BY salary DESC;

--QUERY 3.2: FIND ALL EMPLOYEES IN THE ENGINEERING DEPARMENT
SELECT e.* FROM employees e JOIN departments d ON e.dept_id = d.dept_id WHERE d.dept_name = 'Engineering';

--QUERY 3.3: LIST EMPLOYEES HIRED IN 2021 OR LATER
SELECT * FROM employees WHERE hire_date >= '2021-01-01';

--QUERY 3.4: FIND EMPLOYEES WITH SALARIES BTWN 60K AND 80K
SELECT * FROM employees WHERE salary BETWEEN 60000 AND 80000;

--QUERY 3.5: FIND EMPLOYEES WHOSE EMAIL CONTAINS 'COMPANY'
SELECT * FROM employees WHERE email LIKE '%company%';

--QUERY 3.6: LIST DEPARMENTS IN BUILDINGS A OR B
SELECT * FROM departments WHERE location IN ('Building A', 'Building B');

--QUERY 3.7: CALCULATE THE TOTAL SALARY EXPENSE PER DEPARTMENT
SELECT d.dept_name, SUM(e.salary) AS total_salary_expense FROM departments d JOIN employees e ON d.dept_id = e.dept_id GROUP BY d.dept_name;

--QUERY 3.8: FIND THE AVG, MIN, AND MAX SALARY
SELECT AVG(salary) AS average_salary,
       MIN(salary) AS minimum_salary,
       MAX(salary) AS maximum_salary
FROM employees;

--QUERY 3.9: COUNT EMPLOYEES IN EACH DEPARTMENT, ONLY SHOW DEPARTMENTS WITH 2+ EMPLOYEES
SELECT d.dept_name,
       COUNT(e.emp_id) AS employee_count
FROM departments d JOIN employees e ON d.dept_id = e.dept_id GROUP BY d.dept_name HAVING COUNT(e.emp_id) >= 2;

--QUERY 3.10: CREATE A REPORT SHOWING FULL NAME (FIRST + LAST), DEPARTMENT NAME, AND FORMATTED SALARY
SELECT 
    e.first_name || ' ' || e.last_name AS full_name,
    d.dept_name AS department,
    TO_CHAR(e.salary, '$999,999.00') AS salary_formatted
FROM employees e JOIN departments d ON e.dept_id = d.dept_id;

--PART 4: CHALLENGE
--CHALLENGE 4.1: FIND EMPLOYEES WHO EARN MORE THAN AVG SALARY
SELECT * FROM employees WHERE salary > (SELECT AVG(salary) FROM employees);

--CHALLENGE 4.2: LIST DEPARTMENTS THAT HAVE AT LEAST ONE PROJECT
--THIS ONE DOESNT WORK
SELECT DISTINCT d.dept_name FROM departments d JOIN projects p ON d.dept_id = p.dept_id;

--CHALLENGE 4.3: FIND THE EMPLOYEE WITH THE HIGHEST SALARY IN EACH DEPARTMENT
SELECT d.dept_name, e.first_name, e.last_name, e.salary FROM employees e JOIN departments d ON e.dept_id = d.dept_id WHERE e.salary = (
    SELECT MAX(salary) FROM employees WHERE dept_id = e.dept_id
);
--CHALLENGE 4.4: CALC HOW LONG EACH EMPLOYEE HAS BEEN WITH THE COMPANY (IN YEARS AND MONTHS)
SELECT first_name, last_name, AGE( CURRENT_DATE, hire_date) AS time_with_company FROM employees

