queries = ["" for i in range(0, 16)]

### 0. Report the votes for the normal (i.e, not special) Senate Election in Maryland in 2018.
### Output column order: candidatename, candidatevotes
### Order by candidatename ascending
queries[0] = """
SELECT candidatename, candidatevotes
FROM sen_state_returns
WHERE year = 2018 AND specialelections = FALSE AND statecode = 'MD';
"""

### 1. Write a query to find the maximum, minimum, and average population in 2010 across all states.
### The result will be a single row.
### Truncate the avg population to a whole number using trunc
### Output Columns: max_population, min_population, avg_population
queries[1] = """
SELECT TRUNC(MAX(population_2010)) AS max_population, TRUNC(MIN(population_2010)) AS min_population, TRUNC(AVG(population_2010)) AS avg_population
FROM states;
"""

### 2. Write a query to find the candidate with the maximum votes in the 2008 MI Senate Election. 
### Output Column: candidatename
### Order by: candidatename
queries[2] = """
SELECT candidatename
FROM sen_state_returns
WHERE year = 2008 AND statecode = 'MI' AND candidatevotes = (SELECT MAX(candidatevotes) FROM sen_state_returns WHERE year = 2008 AND statecode = 'MI');
"""

### 3. Write a query to find the number of candidates who are listed in the sen_state_returns table for each senate election held in 2018. 
### Note that there may be two elections in some states, and there should be two tuples in the output for that state.
### 'NA' or '' (empty) should be treated as candidates. 
### Output columns: statecode, specialelections, numcandidates
### Order by: statecode, specialelections
queries[3] = """
SELECT statecode, specialelections, COUNT(*) AS numcandidates
FROM sen_state_returns 
WHERE year = 2018
GROUP BY statecode, specialelections;
"""

### 4. Write a query to find, for the 2008 elections, the number of counties where Barack Obama received strictly more votes 
### than John McCain.
### This will require you to do a self-join, i.e., join pres_county_returns with itself.
### Output columns: num_counties
queries[4] = """
WITH temp AS (SELECT r1.countyname AS countyname
FROM pres_county_returns r1, pres_county_returns r2
WHERE r1.year = 2008 AND r2.year = 2008 AND r1.statecode = r2.statecode AND r1.countyname = r2.countyname AND r1.candidatename = 'Barack Obama' AND r2.candidatename = 'John McCain' AND r1.candidatevotes > r2.candidatevotes)
SELECT Count(*) AS num_counties
FROM temp;
"""


### 5. Write a query to find the names of the states with at least 100 counties in the 'counties' table.
### Use HAVING clause for this purpose.
### Output columns: statename, num_counties
### Order by: statename
queries[5] = """
SELECT s.name AS statename, COUNT(c.statecode) AS num_counties
FROM states s, counties c
WHERE s.statecode = c.statecode 
GROUP BY s.name
HAVING COUNT(c.statecode) >= 100
ORDER BY s.name; 
"""

### 6. Write a query to construct a table:
###     (statecode, total_votes_2008, total_votes_2012)
### to count the total number of votes by state for Barack Obama in the two elections.
###
### Use the ability to "sum" an expression (e.g., the following query returns the number of counties in 'AR')
### select sum(case when statecode = 'AR' then 1 else 0 end) from counties;
###
### Order by: statecode
queries[6] = """
SELECT statecode, SUM(case when year = 2008 AND candidatename = 'Barack Obama' then candidatevotes else 0 end) AS total_votes_2008, SUM(case when year = 2012 AND candidatename = 'Barack Obama' then candidatevotes else 0 end) total_votes_2012
FROM pres_county_returns
GROUP BY statecode
ORDER BY statecode;

"""

### 7. Create a table to list the disparity between the populations listed in 'states' table and those listed in 'counties' table for 1950 and 2010.
### Result should be: 
###        (statename, disparity_1950, disparity_2010)
### So disparity_1950 = state population 1950 - sum of population_1950 for the counties in that state
### Use HAVING to only output those states where there is some disparity (i.e., where at least one of the two is non-zero)
### Order by statename
queries[7] = """
SELECT s.name AS statename, s.population_1950 - SUM(case when c.statecode = s.statecode then c.population_1950 else 0 end) AS disparity_1950, s.population_2010 - SUM(case when c.statecode = s.statecode then c.population_2010 else 0 end) AS disparity_2010 
FROM states s, counties c
GROUP BY s.name, s.population_1950, s.population_2010
HAVING s.population_1950 - SUM(case when c.statecode = s.statecode then c.population_1950 else 0 end) != 0 OR s.population_2010 - SUM(case when c.statecode = s.statecode then c.population_2010 else 0 end) != 0
ORDER BY s.name; 
"""

### 8. Use 'EXISTS' or 'NOT EXISTS' to find the states where no counties have population in 2010 above 500000 (500 thousand).
### Output columns: statename
### Order by statename
queries[8] = """
SELECT name as statename 
FROM states s 
WHERE NOT EXISTS (SELECT c.population_2010 FROM counties c WHERE c.population_2010 > 500000 AND s.statecode = c.statecode) 
ORDER BY statename;
"""



### 9. List all counties and their basic information that have a unique name across all states. 
### Use scalar subqueries to simplify the query.
### Output columns: all attributes of counties (name, statecode, population_1950, population_2010)
### Order by name, statecode
queries[9] = """
SELECT name, statecode, population_1950, population_2010
FROM counties c
WHERE 1 = (SELECT COUNT(c1.name) FROM counties c1 WHERE c.name = c1.name)
ORDER BY name, statecode;
"""
### 10. Use Set Intersection to find the counties that Barack Obama lost in 2008, but won in 2012.
### We have created a temporary table using WITH that you can use (or not).
###
### Output columns: countyname, statecode
### Order by countyname, statecode
queries[10] = """
WITH max_votes AS (SELECT year, countyname, statecode, max(candidatevotes) as max_county_votes 
FROM pres_county_returns GROUP BY year, countyname, statecode), 
status AS (select p.year, p.countyname, p.statecode, p.candidatevotes = m.max_county_votes as election_won 
from max_votes m, pres_county_returns p where candidatename = 'Barack Obama' 
and m.countyname = p.countyname AND p.statecode = m.statecode AND p.year = m.year) 
SELECT countyname, statecode FROM
((SELECT countyname, statecode FROM status WHERE 
election_won = False AND year = 2008 ORDER BY countyname, statecode) 
INTERSECT 
(SELECT countyname, statecode FROM status WHERE election_won = True AND year = 2012
ORDER BY countyname, statecode)) AS X
Order by countyname, statecode;
"""


### 11. Find all presidential candidates listed in pres_county_returns who also ran for senator.
### HINT: Use "intersect" to simplify the query
###
### Every candidate should be reported only once. You will see incorrect answers in there because "names" don't match -- that's fine.
###
### Output columns: candidatename
### Order by: candidatename
queries[11] = """
(SELECT candidatename
FROM pres_county_returns WHERE candidatename != 'Other')
INTERSECT
(SELECT candidatename
FROM sen_state_returns);
"""



### 12. Create a table listing the months and the number of states that were admitted to the union (admitted_to_union field) in that month.
### Use 'extract' for operating on dates, and the ability to create a small inline table in SQL. For example, try:
###         select * from (values(1, 'Jan'), (2, 'Feb')) as x;
###
### Output columns: month_no, monthname, num_states_admitted
### month should take values: Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec
### Order by: month_no
queries[12] = """
SELECT x.column1 AS month_no, x.column2 AS monthname, SUM(case when EXTRACT(MONTH FROM s.admitted_to_union) = x.column1 then 1 else 0 end) AS num_states_admitted
FROM (values(1, 'Jan'), (2, 'Feb'), (3,'Mar'), (4,'Apr'),(5,'May'),(6,'Jun'),(7,'Jul'),(8,'Aug'),(9,'Sep'),(10,'Oct'),(11,'Nov'),(12,'Dec')) as x, states s
WHERE x.column1 = EXTRACT(MONTH FROM s.admitted_to_union)
GROUP BY x.column1, x.column2
ORDER BY month_no;
"""


### 13. Create a view pres_state_votes with schema (year, statecode, candidatename, partyname, candidatevotes) where we maintain aggregated counts by statecode (i.e.,
### candidatevotes in this view would be the total votes for each state, including states with statecode 'NA').
queries[13] = """
CREATE VIEW pres_state_votes AS 
SELECT p.year, p.statecode, p.candidatename, p.partyname, SUM(p.candidatevotes) AS candidatevotes
FROM pres_county_returns p
GROUP BY p.year, p.statecode, p.candidatename, p.partyname;
"""

### 14. Use a single ALTER TABLE statement to add (name, statecode) as primary key to counties, and to add CHECKs that neither of the two populations are less than zero.
### Name the two CHECK constraints nonzero2010 and nonzero1950.
queries[14] = """
ALTER TABLE counties
ADD PRIMARY KEY (name,statecode),
ADD CONSTRAINT nonzero1950 CHECK (population_1950 >= 0),
ADD CONSTRAINT nonzero2010 CHECK (population_2010 >= 0);
"""


### 15. Create a list of percentage each presidential candidate won in each state, in each year, and
### show only the top 10 (among all year and state) in descending order. "percentvote" should be a float
### with one digit to the right of the decimal point.
### Output columns: year, statecode, candidatename, candidatevotes, totalvotes, percentvote
### Order by: percentvote desc, year asc, candidatename asc, limit to 10 lines
queries[15] = """
WITH total_votes AS (SELECT year, statecode, sum(candidatevotes) as totalvotes 
FROM pres_county_returns GROUP BY statecode, year), 
winners AS (SELECT year, statecode, candidatename, sum(candidatevotes) as candidatevotes 
FROM pres_county_returns GROUP BY year, statecode, candidatename) 
SELECT t.year, t.statecode, w.candidatename, w.candidatevotes, t.totalvotes, 
ROUND((w.candidatevotes*1.0/t.totalvotes)*100.0, 1) as percentvote 
FROM total_votes t, winners w
WHERE t.totalvotes != 0 AND t.year = w.year AND t.statecode = w.statecode 
ORDER BY percentvote desc, year asc, candidatename asc LIMIT 10;
"""

