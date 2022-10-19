from peewee import *
import json
import sys
from datetime import date

database = PostgresqlDatabase('flightsskewed', **{'host': 'localhost', 'user': 'vagrant', 'password': 'vagrant'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Airports(BaseModel):
    airportid = CharField(primary_key=True)
    city = CharField(null=True)
    name = CharField(null=True)
    total2011 = IntegerField(null=True)
    total2012 = IntegerField(null=True)

    class Meta:
        table_name = 'airports'

class Airlines(BaseModel):
    airlineid = CharField(primary_key=True)
    hub = ForeignKeyField(column_name='hub', field='airportid', model=Airports, null=True)
    name = CharField(null=True)

    class Meta:
        table_name = 'airlines'

class Customers(BaseModel):
    birthdate = DateField(null=True)
    customerid = CharField(primary_key=True)
    frequentflieron = ForeignKeyField(column_name='frequentflieron', field='airlineid', model=Airlines, null=True)
    name = CharField(null=True)

    class Meta:
        table_name = 'customers'

class Flights(BaseModel):
    airlineid = ForeignKeyField(column_name='airlineid', field='airlineid', model=Airlines, null=True)
    dest = ForeignKeyField(column_name='dest', field='airportid', model=Airports, null=True)
    flightid = CharField(primary_key=True)
    local_arrival_time = TimeField(null=True)
    local_departing_time = TimeField(null=True)
    source = ForeignKeyField(backref='airports_source_set', column_name='source', field='airportid', model=Airports, null=True)

    class Meta:
        table_name = 'flights'

class Flewon(BaseModel):
    customerid = ForeignKeyField(column_name='customerid', field='customerid', model=Customers, null=True)
    flightdate = DateField(null=True)
    flightid = ForeignKeyField(column_name='flightid', field='flightid', model=Flights, null=True)

    class Meta:
        table_name = 'flewon'

class Numberofflightstaken(BaseModel):
    customerid = CharField(null=True)
    customername = CharField(null=True)
    numflights = IntegerField(null=True)

    class Meta:
        table_name = 'numberofflightstaken'
        primary_key = False

def runORM(jsonFile):
    customer_set = set()
    airlines_dict = {}
    
    for customer in Customers.select().order_by(Customers.customerid):
        customer_set.add(customer.customerid.strip())
        
    for airline in Airlines.select().order_by(Airlines.name):            
        airlines_dict[airline.name.strip()] = airline.airlineid.strip()
        
    with open(jsonFile) as file:
        for line in file:
            L = json.loads(line)
            if "newcustomer" in L:
                newcustomer_id = L["newcustomer"]["customerid"]
                if newcustomer_id in customer_set:
                    print("Error424")
                    sys.exit()
                else:
                    frequentflieron = L["newcustomer"]["frequentflieron"]
                    if frequentflieron in airlines_dict:
                        airlineCode = airlines_dict[frequentflieron] 
                        InsertCustomer(L["newcustomer"], airlineCode)
                    else:
                        print("Error424")
                        sys.exit()
            if "flewon" in L:
                customers = L["flewon"]["customers"]
                for r in customers:
                    customerid = r["customerid"]
                    if r["customerid"] in customer_set:
                        InsertFlewon(L["flewon"], customerid)
                    else:
                        frequentflieron= r["frequentflieron"]
                        InsertCustomer(r, frequentflieron)
                        InsertFlewon(L["flewon"], customerid)

                        
def InsertCustomer(data, frequentflieron1):
    customerid1= data["customerid"]
    name1= data["name"]
    birthdate1= data["birthdate"]
    Customers(customerid=customerid1, name=name1, birthdate=birthdate1, frequentflieron=frequentflieron1).save(force_insert=True)
    
def InsertFlewon(data, customerid1):
    flightid1 = data["flightid"]
    flightdate1 = data["flightdate"] 
    Flewon(flightid=flightid1, flightdate=flightdate1, customerid=customerid1).save(force_insert=True)