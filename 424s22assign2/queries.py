queries = ["" for i in range(0, 17)]

### 0. Report the votes for the normal (i.e, not special) Senate Election in Maryland in 2018.
### Output column order: candidatename, candidatevotes
### Order by candidatename ascending
queries[0] = """
select candidatename, partyname, candidatevotes
from sen_state_returns
where year = 2018 and statecode = 'MD' and specialelections = False
order by candidatename asc;
"""

### 1. Report the number of votes for candidate 'Ben Cardin' across all the senate elections.
### Output Column: year, statecode, specialelections, candidatevotes 
### Order by candidatevotes increasing
queries[1] = """
SELECT year, statecode, specialelections, candidatevotes
FROM sen_state_returns
WHERE candidatename = 'Ben Cardin'
ORDER BY candidatevotes ;
"""


### 2. Write a query to output the % increase, truncated to whole integer using TRUNC, in the population from 1950 to 2010.
### So for Autauga, the answer would be: 200  (54571-18186)*100/18186 = 200.7 ==> truncated to 200
### There are some counties with 0 population in 1950 -- remove those counties from the answer.
### Output columns: countyname, statecode, percentincrease
### Order output by precentincrease increasing
queries[2] = """
SELECT name AS countyname, statecode, TRUNC((population_2010 - population_1950)*100/population_1950) AS percentincrease
FROM counties 
WHERE population_1950 > 0
ORDER BY percentincrease ASC;
"""

### 3. Select all the "distinct" party names that senate candidates have been affiliated over all
### the elections. 
### Output column: partyname
### Order output by partyname ascending
queries[3] = """
SELECT DISTINCT partyname
FROM sen_state_returns
ORDER BY partyname ASC;
"""

### 4. Write a query to output for each state how many years ago it was admitted to the union. 
### So if a state was admitted to the union in 1819, the answer would 201 (2020 - 1819). Ignore the specific dates.
### Output columns: name, admittedduration
### Order by admittedduration decreasing
queries[4] = """
SELECT name, 2020 - EXTRACT(year FROM admitted_to_union) AS admittedduration 
FROM states
ORDER BY admittedduration DESC;
"""

### 5. Write a query to find the states where the increase in population from 1900 to 1950 was lower than the increase in population from 2000 to 2010.
### Output Column: name
### Order by: name increasing
queries[5] = """
SELECT name
FROM states
WHERE (population_1950 - population_1900) < (population_2010 - population_2000)
ORDER BY name ASC;
"""

### 6. Write a query to find all candidates for senate who satisfy one of the following conditions:
###        - the candidate is a 'democrat' and has more than 750000 votes in Alabama.
###        - the candidate is a 'republican' and has more 1,000,000 votes in Maryland.
###        - the candidate is neither a democrat or nor a republican and has more than 500,000 votes (in any state).
### Some candidates appear under multiple party names. Ignore that for now (in other words, if a democrat has 700,000 votes in AL as a 'democrat' and
### also gets 100,000 votes as something else, that candidate should NOT be in the result
### Also: ignore any party names like 'democratic-farmer-labor' etc.
### Output columns: year, statecode, specialelections, candidatename, partyname
queries[6] = """
SELECT year, statecode, specialelections, candidatename, partyname
FROM sen_elections NATURAL JOIN sen_state_returns
WHERE (partyname = 'democrat' AND statecode = 'AL' AND candidatevotes > 750000) OR (partyname = 'republican' AND statecode = 'MD' AND candidatevotes > 1000000) OR (partyname != 'democrat' AND partyname != 'republican' AND candidatevotes > 500000);
"""


### 7. Write a query to join the tables states and counties to create a list of county names, county population in 2010, state name, the state
### population in 2010
### Output columns: statename, statepopulation, countyname, countypopulation
### Order first by statename, then by countyname, increasing
queries[7] = """
SELECT states.name AS statename, states.population_2010 AS statepopulation, counties.name AS countyname, counties.population_2010 AS countypopulation
FROM states, counties
WHERE states.statecode = counties.statecode
ORDER BY statename, countyname ASC;
"""

### 8. Write a query to join the tables states and counties to find the counties that had over
### 50% of the population of the state in 2010
### Output columns: statename, countyname 
### Order by statename, then by countyname, increasing
queries[8] = """
SELECT states.name AS statename, counties.name AS countyname 
FROM states, counties
WHERE states.statecode = counties.statecode AND counties.population_2010 > 0.5*states.population_2010
ORDER BY statename, countyname ASC;
"""


### 9. The tables were collected from 2 different sources, and there may be some consistency issues across them. 
### Write a query to find all counties (and the corresponding state names) that are present in "pres_county_returns" table, but 
### do not have any corresponding entry in the "counties"
### table (through straightforward string equality -- so 'Autauga' and 'Autauga ' (with an extra space) would NOT be considered a match.
### Each county+state combination should only appear once in the output.
### HINT: Use "not in".
### Output Columns: countyname, statename
### Order by name, statename ascending
queries[9] = """
SELECT DISTINCT countyname, states.name AS statename 
FROM pres_county_returns, states
WHERE (pres_county_returns.statecode = states.statecode) AND ((countyname, states.statecode) NOT IN (SELECT name, statecode FROM counties))
ORDER BY countyname, statename ASC;
"""


### 10. Write a query to join sen_state_returns and sen_elections to find the candidates that received 70% or more of the total vote.
### Output columns: year, statecode, specialelections, candidatename
### Order by percentage of total vote increasing
queries[10] = """
SELECT sen_state_returns.year AS year, sen_state_returns.statecode AS statecode, sen_state_returns.specialelections AS specialelections, candidatename
FROM sen_state_returns NATURAL JOIN sen_elections
WHERE candidatevotes > 0.7*totalvotes
ORDER BY candidatevotes*100/totalvotes ASC;
"""


### 11. For the 2012 presidential elections and for 'Barack Obama', write a
### query to combine pres_county_returns and counties so that, to produce a result
### with the following columns:
###     countyname, statecode, candidatevotes, population_2010
### However, for the counties in pres_county_returns that do not have a match in 
### 'counties' table, we want population_2010 to be set to NULL.
### Use a left (or right) outer join to achive this.
### Output: countyname, statecode, candidatevotes, population_2010
### Order by: countyname, statecode ascending
queries[11] = """
SELECT p.countyname AS countyname, p.statecode AS statecode, p.candidatevotes AS candidatevotes, population_2010
FROM pres_county_returns p LEFT OUTER JOIN counties c ON (p.countyname = c.name AND c.statecode = p.statecode)
WHERE p.year = 2012 AND p.candidatename = 'Barack Obama'
ORDER BY countyname, statecode ASC;
"""

### 12. SQL "with" clause can be used to simplify queries. It essentially allows
### specifying temporary tables to be used during the rest of the query. See Section
### 3.8.6 (6th Edition) for some examples.
###
### Below we are providing a part of a query that uses "with" to create a
### temporary table where, for 2000 elections, we are finding the maximum of the
### candidate votes for each county. Join this temporary table with the
### 'pres_county_returns' table to find the winner for each county. 
### This is unfortunately the easiest way to do this task.
###
### You don't need to fully understand what the 'temp' query does to do the join
### -- as provided, the query shows you the result of the "temp" table
### Output columns: countyname, statecode, candidatename
### Order by: countyname, statecode, candidatename
queries[12] = """
with temp as (select countyname, statecode, max(candidatevotes) as maxvotes
        from pres_county_returns
        where year = 2000
        group by countyname, statecode)
SELECT t.countyname AS countyname, t.statecode AS statecode, candidatename 
FROM temp t, pres_county_returns p
WHERE t.countyname = p.countyname AND t.statecode = p.statecode AND maxvotes = candidatevotes;
"""


### 13. Some states are just weird. For example, in addition to 95 counties, Virginia has 39 "independent cities",
### which are considered county-equivalents for some purposes. This is not reflected exactly in the data we have, but we
### can see artifacts resulting from this kind of inconsistency in nomenclature.
###
### Write a query to join over pres_county_returns to find "duplicate"
### county names. As a proxy for a more exact solution (because our data
### is inconsistent), group all data for a specific state, county, year,
### and partyname together, and then count them. Any such group w/ more
### than one member is probably a duplicated name.
### Output each state/county combination just once.
### Output columns: statecode, countyname
### Order by statecode, countyname
queries[13] = """
with temp as (SELECT statecode, countyname, year, partyname 
                FROM pres_county_returns 
                GROUP BY statecode, countyname, year, partyname 
                HAVING count(*) > 1) 
SELECT DISTINCT statecode, countyname 
FROM temp 
ORDER BY statecode, countyname;
"""


### 14. Let's create a table showing the vote differences between 2000 and 2016 for
### the democratic presidential candidates in each county. 
### We ONLY want those states/counties for which we have all the information.
### (Note that because of the duplication discussed in (13), you should take the "MAX"
### of the democratic votes for each county/state/year combination.
### Output: statecode, countyname, votes2000, votes2016
### Order by: statecode, countyname ascending
queries[14] = """
WITH temp1 AS (SELECT statecode, countyname, max(candidatevotes) as votes2000 
FROM pres_county_returns WHERE year = 2000 AND partyname = 'democrat' 
GROUP BY statecode, countyname), 
temp2 AS (SELECT statecode, countyname, max(candidatevotes) as votes2016 
FROM pres_county_returns WHERE year = 2016 AND partyname = 'democrat' 
GROUP BY statecode, countyname) 
SELECT DISTINCT t1.statecode AS statecode, t1.countyname AS countyname, votes2000, votes2016 
FROM temp1 t1, temp2 t2
WHERE t1.statecode = t2.statecode AND t1.countyname = t2.countyname 
ORDER BY t1.statecode, t1.countyname ASC;
"""


### 15. Write a statement to add a new column to the counties table called 'pop_trend' of type 'string'.
queries[15] = """
ALTER TABLE counties
ADD COLUMN pop_trend VARCHAR(50);
"""

### 16. The values for the above added column with be empty to begin with. Write an update statement to 
### set it to 'decreased', 'increased somewhat', and 'increased a lot', depending on whether the population decreased,
### increased by less than a factor of 2 (i.e., population_2010 <= 2*population_1950), or increased by a factor of more than 2.
### Use CASE statement to make this easier.
queries[16] = """
UPDATE counties c SET pop_trend = 
CASE
WHEN c.population_2010 <= c.population_1950 THEN 'decreased'
WHEN c.population_2010 <= 2 * c.population_1950 THEN 'increased somewhat'
ELSE 'increased a lot'
END;
"""


