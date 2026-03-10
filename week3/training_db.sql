CREATE DATABASE training_db;

-- DDL: CREATE, DROP, ALTER

CREATE TABLE associates (
    associate_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hire_date DATE DEFAULT CURRENT_DATE
);

/*DROP TABLE associates;*/


-- DML: INSERT, UPDATE, DELETE, TRUNCATE(?)

INSERT INTO associates (
    first_name,
    last_name,
    email
)
VALUES (
    'Magan',
    'Greenfield',
    'magan.greenfield@revature.net'
), (
    'Lee',
    'Wilson',
    'lee.wilson@revature.net'
)

SELECT * FROM associates;

ALTER TABLE associates ADD COLUMN department VARCHAR(50);
ALTER TABLE associates ALTER COLUMN hire_date SET NOT NULL;
ALTER TABLE associates ALTER COLUMN email TYPE VARCHAR(115);

SELECT * FROM associates;

UPDATE associates SET department = 'Training';
--or UPDATE associates SET department = 'Training' where associate_id = 1; to be specific
ALTER TABLE associates ALTER COLUMN department SET NOT NULL;