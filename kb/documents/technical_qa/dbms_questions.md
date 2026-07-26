## Q: What is Database Normalization and why is it used?
**Topic:** Database Management Systems
**Difficulty:** easy
**A:** Normalization is the systematic process of organizing data in a relational database to minimize data redundancy and prevent update anomalies. It involves decomposing large, unstructured tables into smaller, well-structured tables linked by foreign keys. Standard normal forms include First Normal Form (1NF), Second Normal Form (2NF), Third Normal Form (3NF), and BCNF.

## Q: What is a database index and what are its trade-offs?
**Topic:** Database Management Systems
**Difficulty:** medium
**A:** A database index is a data structure (typically a B-Tree or Hash table) that speeds up data retrieval operations on a table at the expense of additional storage and write performance. By maintaining sorted references to row locations, indexes allow queries to execute logarithmic search rather than full table scans. However, every INSERT, UPDATE, or DELETE operation incurs overhead because indexes must also be updated.

## Q: What are ACID properties and SQL Joins in relational databases?
**Topic:** Database Management Systems
**Difficulty:** hard
**A:** ACID stands for Atomicity, Consistency, Isolation, and Durability, which collectively guarantee reliable database transactions even in the event of errors or system crashes. SQL Joins (INNER, LEFT, RIGHT, FULL OUTER) allow users to combine rows from two or more tables based on related columns. Together, ACID transactions and SQL Joins ensure data integrity while enabling complex queries across relational entities.
