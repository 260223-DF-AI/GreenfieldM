# 1. inner join - write a query to show student names and their major names
# only for students with matching majors
SELECT students.name, majors.major_name
FROM students
INNER JOIN majors
    ON students.major_id = majors.major_id;

# 2. left join - show all students, even if they dont have a major
SELECT students.name, majors.major_name
FROM students
LEFT JOIN majors
    ON students.major_id = majors.major_id;

# 3. right join - show all majors, even if no students belong to them
SELECT students.name, majors.major_name
FROM students
RIGHT JOIN majors
    ON students.major_id = majors.major_id;

# 4. full outer join - show all students and all majors, matched where possible
SELECT students.name, majors.major_name
FROM students
FULL OUTER JOIN majors
    ON students.major_id = majors.major_id;

# 5. self join - using employees table with employee_id, name, and manager_id
# show each employee with their manager
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m
    ON e.manager_id = m.employee_id;

# 6. cross join - show every student-major combination
SELECT students.name, majors.major_name
FROM students
CROSS JOIN majors;

# 7. natural join - if two tables both contain major_id, write a natural join query
SELECT *
FROM students
NATURAL JOIN majors;
