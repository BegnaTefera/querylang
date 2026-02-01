# QueryLang



QueryLang is a \*\*simple SQL-like query engine\*\* implemented in Python that executes queries directly on \*\*in-memory data structures\*\*.

The goal of this project is clarity and correctness rather than performance or full SQL compliance.



---



\## Supported Features



\* `SELECT` specific columns

\* `FROM` a table (in-memory Python list of dictionaries)

\* `WHERE` simple equality conditions

\* `JOIN` (INNER JOIN with equality condition)

\* Aggregation functions:



&nbsp; \* `COUNT(column)`

&nbsp; \* `SUM(column)`

&nbsp; \* `AVG(column)`

\* `GROUP BY`

\* \*\*Limited nested queries\*\* (subquery inside `WHERE IN`)



---



\## Example Queries



\### Simple SELECT



```sql

SELECT name, salary

FROM employees

WHERE dept = 'IT'

```



\### GROUP BY with Aggregation



```sql

SELECT dept, COUNT(id), AVG(salary)

FROM employees

GROUP BY dept

```



\### JOIN Query



```sql

SELECT employees.name, departments.name

FROM employees JOIN departments

ON employees.dept = departments.id

```



\### Nested Query



```sql

SELECT name

FROM employees

WHERE dept IN (

&nbsp;   SELECT id

&nbsp;   FROM departments

&nbsp;   WHERE name = 'IT'

)

```



---



\## How It Works (High-Level)



1\. \*\*Parsing\*\*

&nbsp;  The query string is split into logical components (`SELECT`, `FROM`, `JOIN`, `WHERE`, `GROUP BY`).

&nbsp;  This is done using straightforward string processing to keep the system simple and readable.



2\. \*\*Execution Model\*\*

&nbsp;  QueryLang uses an \*\*interpreter-based execution model\*\*. The parsed query is executed directly on Python data structures without generating bytecode or machine code.



3\. \*\*Filtering (`WHERE`)\*\*

&nbsp;  Rows are filtered early using simple equality predicates. Nested queries are executed first, and their results are reused in the outer query.



4\. \*\*JOIN Processing\*\*

&nbsp;  JOINs are executed using a \*\*nested-loop join\*\* strategy, which is simple and suitable for in-memory datasets.



5\. \*\*Grouping \& Aggregation\*\*

&nbsp;  When `GROUP BY` is present, rows are grouped using Python dictionaries and aggregate functions are computed per group.



---



\## Design Decisions



\* No external parser generators (ANTLR) were used to keep the learning curve low

\* Interpreter execution was chosen over compilation for simplicity

\* Data is stored entirely in memory for fast access and easy debugging



---



\## Limitations



\* Only equality conditions are supported in `WHERE`

\* JOINs are limited to INNER JOINs

\* Nested queries are limited to `IN (SELECT ...)`

\* No cost-based optimization or indexing



---



\## How to Run



```bash

python main.py

```



---



\## Educational Value



This project demonstrates core \*\*database system concepts\*\*:



\* Query parsing

\* Logical query execution

\* JOIN algorithms

\* Aggregation

\* Nested query handling



It serves as a foundation that can be extended with advanced parsing, optimization, and execution strategies.



