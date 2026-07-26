## Q: What are the ACID properties in database management systems?

**Topic:** DBMS  
**Role:** Software Engineer  
**Difficulty:** medium  
**Q:** What are the ACID properties in database management systems?  
**A:** **Atomicity**: Transactions commit completely or roll back entirely. **Consistency**: Transactions transition database from one valid state to another. **Isolation**: Concurrent transactions execute independently without interference. **Durability**: Committed data persists permanently even during power outages.

## Q: What is Database Normalization and why is 3NF important?

**Topic:** DBMS  
**Role:** Software Engineer  
**Difficulty:** medium  
**Q:** What is Database Normalization and why is 3NF important?  
**A:** Normalization organizes table columns and relations to eliminate data redundancy and insertion/update/deletion anomalies. 3rd Normal Form (3NF) requires that tables are in 2NF and all non-key attributes depend solely on the primary key (no transitive dependencies).

## Q: How does Database Indexing speed up query performance?

**Topic:** DBMS  
**Role:** Software Engineer  
**Difficulty:** hard  
**Q:** How does Database Indexing speed up query performance?  
**A:** Indexing creates auxiliary search data structures (typically B-Trees or Hash tables) mapping indexed keys directly to row pointers, reducing query lookup time complexity from $O(N)$ full table scans to $O(\log N)$ tree traversals.
