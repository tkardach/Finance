Financing back-end server written in Python, using MySQL database



Dev Setup
---------

1. MySQL database setup with test@localhost user set with privileges:

GRANT CREATE, SELECT, DROP, DELETE, UPDATE, INSERT, REFERENCES, INDEX 
ON finance_test.* 
TO 'test'@'localhost';

2. Python 3.8.6+ installed
