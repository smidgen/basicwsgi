CREATE DATABASE test COLLATE=utf8_general_ci;

CREATE USER 'test'@'localhost' IDENTIFIED BY 'change_me';
GRANT SELECT, INSERT, UPDATE, DELETE ON test.* TO 'test'@'localhost';

USE test;

CREATE TABLE test (
     id int NOT NULL auto_increment PRIMARY KEY
    ,text varchar(256) NULL
);

INSERT INTO test (text)
VALUES   ('Hello, World!')
        ,('Goodbye, World!')
;
