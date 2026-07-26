## Q: What is the difference between WHERE and HAVING clauses in SQL?

**Topic:** Data Analysis & SQL  
**Role:** Data Analyst  
**Difficulty:** easy  
**Q:** What is the difference between WHERE and HAVING clauses in SQL?  
**A:** The `WHERE` clause filters rows before any aggregate function or `GROUP BY` calculation is applied. The `HAVING` clause filters aggregated groups after `GROUP BY` execution. For instance, `WHERE sales > 100` filters raw records, whereas `HAVING SUM(sales) > 1000` filters aggregated totals.

## Q: What is the difference between INNER JOIN, LEFT JOIN, and FULL OUTER JOIN?

**Topic:** Data Analysis & SQL  
**Role:** Data Analyst  
**Difficulty:** easy  
**Q:** What is the difference between INNER JOIN, LEFT JOIN, and FULL OUTER JOIN?  
**A:** `INNER JOIN` returns only records with matching keys in both tables. `LEFT JOIN` returns all records from the left table and matched records from the right table (filling unmatched right columns with NULL). `FULL OUTER JOIN` returns all records from both tables, filling missing values on either side with NULL.

## Q: How do you handle missing or NULL values in a dataset during data preprocessing?

**Topic:** Data Preprocessing & Wrangling  
**Role:** Data Analyst  
**Difficulty:** medium  
**Q:** How do you handle missing or NULL values in a dataset during data preprocessing?  
**A:** Common strategies include: 1) Dropping rows/columns if missingness is minimal (<5%) and random. 2) Imputation using statistical metrics (mean/median for numerical, mode for categorical). 3) Advanced imputation using KNN or regression models. 4) Creating an indicator variable (`is_missing`) to preserve missingness signal for predictive modeling.

## Q: What is an A/B test and what key metrics do you evaluate before declaring a winner?

**Topic:** Experimentation & A/B Testing  
**Role:** Data Analyst  
**Difficulty:** medium  
**Q:** What is an A/B test and what key metrics do you evaluate before declaring a winner?  
**A:** An A/B test splits users into control (A) and variant (B) groups to evaluate feature changes. Key steps: 1) Formulate hypothesis and select primary metric (e.g., Conversion Rate) and guardrail metrics (e.g., Page Load Time). 2) Calculate required sample size for statistical power (typically 80%). 3) Run p-value significance tests (e.g., Z-test/T-test, threshold p < 0.05) and confidence intervals before declaring a winner.

## Q: What is the difference between Correlation and Causation?

**Topic:** Statistics & Experimentation  
**Role:** Data Analyst  
**Difficulty:** easy  
**Q:** What is the difference between Correlation and Causation?  
**A:** Correlation measures the strength and direction of a linear relationship between two variables (e.g., ice cream sales and sunscreen sales). Causation indicates that change in one variable directly produces change in another (e.g., temperature rise causing both). Correlation does not imply causation due to potential confounding variables.

## Q: What are Window Functions in SQL and how do ROW_NUMBER(), RANK(), and DENSE_RANK() differ?

**Topic:** Advanced SQL  
**Role:** Data Analyst  
**Difficulty:** hard  
**Q:** What are Window Functions in SQL and how do ROW_NUMBER(), RANK(), and DENSE_RANK() differ?  
**A:** Window functions perform calculations across a set of table rows related to the current row using `OVER (PARTITION BY ... ORDER BY ...)`. `ROW_NUMBER()` assigns a unique sequential integer to every row regardless of ties. `RANK()` assigns identical ranks to tied rows and skips subsequent numbers (e.g., 1, 2, 2, 4). `DENSE_RANK()` assigns identical ranks to ties without skipping numbers (e.g., 1, 2, 2, 3).

## Q: What is an ETL pipeline and what are its core components?

**Topic:** Data Engineering & Pipeline Design  
**Role:** Data Analyst  
**Difficulty:** medium  
**Q:** What is an ETL pipeline and what are its core components?  
**A:** ETL stands for Extract, Transform, Load. 1) **Extract**: Ingests raw data from source databases, APIs, or log files. 2) **Transform**: Cleans, normalizes, deduplicates, and joins raw data into analytical schema format. 3) **Load**: Writes processed data into a data warehouse (e.g., Snowflake, BigQuery) for reporting and analytics.

## Q: What is an outlier, and how do Z-Score and Interquartile Range (IQR) detect them?

**Topic:** Exploratory Data Analysis  
**Role:** Data Analyst  
**Difficulty:** medium  
**Q:** What is an outlier, and how do Z-Score and Interquartile Range (IQR) detect them?  
**A:** An outlier is an observation distant from other observations. **Z-Score** measures how many standard deviations a data point is from the mean; values above +3 or below -3 are typically outliers. **IQR method** calculates $IQR = Q3 - Q1$; data points below $Q1 - 1.5 \times IQR$ or above $Q3 + 1.5 \times IQR$ are flagged as outliers.

## Q: What is the difference between OLTP and OLAP systems?

**Topic:** Data Warehousing & Architecture  
**Role:** Data Analyst  
**Difficulty:** hard  
**Q:** What is the difference between OLTP and OLAP systems?  
**A:** `OLTP` (Online Transaction Processing) systems handle high-frequency row-based operational transactions (insert/update/delete) with low latency (e.g., PostgreSQL for e-commerce checkouts). `OLAP` (Online Analytical Processing) systems handle complex column-based analytical queries across massive historical datasets (e.g., Snowflake/Redshift for executive dashboards).

## Q: How do you choose between a bar chart, line chart, scatter plot, and heatmap for visualization?

**Topic:** Data Visualization & Storytelling  
**Role:** Data Analyst  
**Difficulty:** easy  
**Q:** How do you choose between a bar chart, line chart, scatter plot, and heatmap for visualization?  
**A:** **Bar chart**: Comparing discrete categorical quantities. **Line chart**: Displaying continuous trends over time. **Scatter plot**: Evaluating relationship/correlation between two numerical variables. **Heatmap**: Showing 2D intensity matrices or correlation matrices across multiple variables.
