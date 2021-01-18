# This is a program to set up the SQL database for the carData program.
# It sets up the makes table in its entirety and creates a model table if there isn't one.
# Theoretically this file should not need to be ran unless the carInfo.sqlite file is damaged or missing, or
# to add car manufacturers to the makeList table.


import sqlite3

db = sqlite3.connect("carInfo.sqlite")
cursor = db.cursor()

# list of manufacturers
companies = ("Ford", "Lincoln", "Mercury", "Merkur",
             "Chevy", "Pontiac", "Buick", "Oldsmobile", "Cadillac", "Saab",
             "VW", "Audi", "Porsche", "Bentley", "Lamborghini", "Bugatti",
             "Dodge", "Chrysler", "Jeep",
             "Fiat", "Alfa Romeo", "Ferrari", "Maserati", "Lancia",
             "Honda", "Acura", "Toyota", "Lexus", "Subaru", "Mitsubishi",
             "Mercedes", "BMW", "Mini", "Caterham"
             )

# get rid of old table and create a fresh one
cursor.execute("DROP TABLE IF EXISTS makeList")
db.execute("CREATE TABLE makeList(_id INTEGER, make TEXT)")

# place all manufacturers in makeList table (sanitized input)
for x in companies:
    db.execute("INSERT INTO makeList(_id, make) VALUES (?, ?)", (companies.index(x) + 1, x,))

# create table for models if one doesn't already exist
# cursor.execute("DROP TABLE makeList") # WILL DELETE ALL STORED MODELS
db.execute("CREATE TABLE IF NOT EXISTS modelList(_id INTEGER, make INTEGER, model TEXT, notes INT, start INTEGER, "
           "end INTEGER, info TEXT)")


# db.execute("INSERT INTO modelList VALUES (1, 13, '924', '2.0 N//A', 1976, 1982, 'The best car ever made.')")
# db.execute("INSERT INTO modelList VALUES (2, 13, '944', '2.5 N//A', 1982, 1991, 'A real gem, apparently.')")
# db.execute("INSERT INTO modelList VALUES (3, 13, '968', '2.0 N//A', 1991, 1995, 'Gettin a bit old there, eh?')")

# assign make id's to make column of modelList table
# cursor.execute("SELECT * IN modelList")
# for c in cursor:
#     db.execute("UPDATE ?(")

db.commit()
db.close()
