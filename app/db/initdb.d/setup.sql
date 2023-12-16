CREATE DATABASE IF NOT EXISTS testdb;

CREATE USER 'tester'@'%' IDENTIFIED BY 'tester1234';
GRANT CREATE, ALTER, INDEX, LOCK TABLES, REFERENCES, UPDATE, DELETE, DROP, SELECT, INSERT ON `testdb`.* TO 'tester'@'%';

FLUSH PRIVILEGES;
