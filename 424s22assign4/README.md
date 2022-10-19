## Project 4: Advanced SQL, Python DB app
### Due Feb 20, 2022, 11:59PM

### Setup

As before we have created a VagrantFile for you on [gradescope](https://www.gradescope.com/courses/336033/assignments/1687997). The main differences here are that we have loaded a skewed database (`flightsskewed`), and also installed Java. Start by doing `vagrant up` and `vagrant ssh` as usual.

Ensure that the Vagrantfile has loaded
the `flightsskewed` database, together with tables populated from  `large-skewed.sql`. Use
`flightsskewed` for all parts of this assignment.

## Part 1: Query Construction (2 pts)

Consider the following query which finds the number of flights
  taken by users whose name starts with 'William'.

```
select c.customerid, c.name, count(*)
from customers c join flewon f on (c.customerid = f.customerid and c.name like 'William%')
group by c.customerid, c.name
order by c.customerid;
```

The result however does not contain the users whose name contains 'William' but who did
not fly at all (e.g., `cust733`). So we may consider
modifying this query to use a left outer join instead, so we get those users as well:

```
select c.customerid, c.name, count(*)
from customers c left outer join flewon f on (c.customerid = f.customerid and c.name like 'William%')
group by c.customerid, c.name
order by c.customerid;
```

Briefly explain why this query does not return the expected answer (as below), and rewrite the query so that it does.

The final answer should look like this:
```
	customerid |              name              | count
	------------+--------------------------------+-------
	cust727    | William Harris                 |     4
	cust728    | William Hill                   |     6
	cust729    | William Jackson                |     6
	cust730    | William Johnson                |     5
        cust731    | William Lee                    |     0
	cust732    | William Lopez                  |     6
	cust733    | William Martinez               |     0
	cust734    | William Mitchell               |     6
	cust735    | William Moore                  |     5
	cust736    | William Parker                 |     4
	cust737    | William Roberts                |     8
	cust738    | William Robinson               |     7
	cust739    | William Rodriguez              |     5
	cust740    | William Wright                 |     8
	cust741    | William Young                  |     5
	(15 rows)
```

Save your query in  `queries.py` as the definition of `queryWilliam`.
Include your explanation as a comment above this definition.

---
## Part 2: Trigger (3 pt)

Let's create a table `NumberOfFlightsTaken(customerid, customername,
numflights)` to keep track of the total number of flights taken by each
customer:
```
create table NumberOfFlightsTaken as
select c.customerid, c.name as customername, count(*) as numflights
from customers c join flewon fo on c.customerid = fo.customerid
group by c.customerid, c.name;
```

Since this is a derived table (and not a view), it will not be kept
up-to-date by the database system.  We (you) will therefore
write a `trigger` to keep this new table updated when a new entry is inserted
into, or a row is deleted from, the `flewon` table. Remember that the `customerid`
corresponding to a new `flewon` insertion update may not yet exist in the
`NumberOfFlightsTaken` table. In that case, it should be added to `NumberOfFlightsTaken`
with a count of 1. 

Similarly, if deletion of a row in `flewon`
results in a user not having any flights, then the corresponding tuple for
that user in `NumberOfFlightsTaken` should be deleted. 

The trigger code should be submitted as the definition of `queryTrigger` in
the `queries.py` file, as straight SQL. This file has an incorrect and
incomplete version of such a trigger commented out. Uncomment this version,
fix it, and test by running `SQLTesting.py`. 

Look inside this file to see
the insertions and deletions being tested, and think about what the proper
actions should be.

Notes:
- `python3 SQLTesting.py` will clean the db, set up `NumberOfFlightsTaken`,
  and run both your queries, printing their outputs.
- We will again be using automated testing. Ensuring that your queries looks to
  be generating correct data w/ `SQLTesting.py` should ensure that the
  autograder will produce correct results as well.

### Mac

- Create db w/ `createdb flightsskewed`.
- Ensure that the user in SQLTesting.py matches your user account.

