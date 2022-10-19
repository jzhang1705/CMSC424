#!/usr/bin/python3
import psycopg2
import json
import sys
from types import *

def runPsy(conn, curs, jsonFile):
    
    curs.execute("SELECT * FROM customers")
    customer_rec = curs.fetchall()
    customer_set = set()
    for r in customer_rec: # r[0].strip() contains the customer id
        customer_set.add(r[0].strip())
    
    curs.execute("SELECT * FROM airlines")
    airlines_rec = curs.fetchall()
    airlines_dict = {}
    for r in airlines_rec: # r[0].strip() contains the airline code, r[1].strip() contains the airline name
        airlines_dict[r[1].strip()]= r[0].strip()
    with open(jsonFile) as file:
        check = False
        for line in file:
            L = json.loads(line)
            if "newcustomer" in L:
                check = True
                newcustomer_id = L["newcustomer"]["customerid"]
                if newcustomer_id in customer_set:
                    print("Error424")
                    sys.exit()
                else:
                    frequentflieron = L["newcustomer"]["frequentflieron"]
                    if frequentflieron in airlines_dict:
                        airlineCode = "'" + airlines_dict[frequentflieron] + "'"
                        InsertCustomer(conn, curs, L["newcustomer"], airlineCode)
                    else:
                        print("Error424")
                        sys.exit()
            if "flewon" in L:
                check = True
                customers = L["flewon"]["customers"]
                for r in customers:
                    customerid = "'" + r["customerid"] + "'"
                    if r["customerid"] in customer_set:
                        InsertFlewon(conn, curs, L["flewon"], customerid)
                    else:
                        frequentflieron="'"+r["frequentflieron"]+"'"
                        InsertCustomer(conn, curs, r, frequentflieron)
                        InsertFlewon(conn, curs, L["flewon"], customerid)
            if check != True:
                print("Error424")
                sys.exit()
            check = False
                        
def InsertCustomer(conn, curs, data, frequentflieron):
    customerid="'"+data["customerid"]+"'"
    name="'"+data["name"] + "'"
    birthdate="'" + data["birthdate"] +"'"
    insertCustomer="INSERT INTO customers (customerid,name,birthdate,frequentflieron) VALUES (%s,%s,%s,%s)" % (customerid,name,birthdate,frequentflieron)
    curs.execute(insertCustomer)
    conn.commit()
    
def InsertFlewon(conn, curs, data, customerid):
    flightid="'"+data["flightid"]+"'"
    flightdate="'"+data["flightdate"] + "'"
    insertFlewon = "INSERT INTO flewon (flightid,flightdate,customerid) VALUES (%s,%s,%s)" % (flightid,flightdate,customerid)
    curs.execute(insertFlewon)
    conn.commit()