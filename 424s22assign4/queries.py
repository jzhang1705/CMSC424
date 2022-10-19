# EXPLANATION: The given left-join query fails because it does a left join on customerid from queries customers and a subquery of flewon that contains people with the first name William. Extracting only the customerids and names from the created query creates a query that simply lists all customerids and names and has displays the customerid and name of Williams who have taken flights more than once a few times. The count(*) and group by c.customerid, c.name simply ensures each of the respected entries are unique and displays the number of times each entry is repeated. As one can see, this result will not eliminate all the customers who don't have the name William and it counts the Williams who haven't been on a flight once rather than none at all.
#
queryWilliam = """
SELECT c.customerid, c.name, SUM(CASE WHEN c.customerid = f.customerid THEN 1 ELSE 0 END) AS count 
FROM customers c JOIN flewon f ON (c.name LIKE 'William%') 
GROUP BY c.customerid, c.name 
ORDER BY c.customerid; 
"""



# NOTE:  This trigger is both INCORRECT and INCOMPLETE. You need to find and fix the bugs, and ensure
# that it will correctly update NumberOfFlightsTaken on both insertions and deletions from "flewon".
queryTrigger = """

CREATE OR REPLACE FUNCTION updateStatusCount() RETURNS trigger AS $updateStatus$
        DECLARE
            old_flight_count integer;
        BEGIN
            IF (TG_OP = 'INSERT') THEN
                IF EXISTS (SELECT customerid FROM NumberOfFlightsTaken WHERE customerid = NEW.customerid) THEN
                    UPDATE NumberOfFlightsTaken
                    SET numflights = numflights + 1
                    WHERE customerid = NEW.customerid;
                ELSE
                   INSERT INTO NumberOfFlightsTaken(customerid, customername, numflights) VALUES (NEW.customerid, (SELECT customers.name FROM customers WHERE customers.customerid = NEW.customerid), 1);

                END IF;
            ELSE
                SELECT numflights INTO old_flight_count FROM NumberOfFlightsTaken WHERE customerid = OLD.customerid;
                IF old_flight_count <= 1 THEN
                    DELETE FROM NumberOfFlightsTaken WHERE customerid = OLD.customerid;
                ELSE
                    UPDATE NumberOfFlightsTaken
                    SET numflights = numflights - 1
                    WHERE customerid = OLD.customerid;
                END IF;
            END IF;
        RETURN NULL;

        END;
$updateStatus$ LANGUAGE plpgsql;

CREATE TRIGGER update_num_status AFTER 
INSERT OR DELETE ON flewon
FOR EACH ROW EXECUTE PROCEDURE updateStatusCount();
END;
"""
