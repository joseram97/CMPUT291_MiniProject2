import os
from bsddb3 import db
import time


def sysSort(file):
    os.system("sort --output="+ file + " -u " + file)
    return

## PHASE 2 (1)
def initDBAd():
    database = db.DB()
    DB_File = "ad.idx"
    database.set_flags(db.DB_DUP) #Important! declare duplicates allowed
    database.open(DB_File,None,db.DB_HASH,db.DB_CREATE)
    insertAds(database)
    return

def insertAds(database):
    curs = database.cursor()
    fpr = open("ads.txt")
    for line in enumerate(fpr):
        sp = line[1].split(":") # 0 is key 1 is data
        database.put(bytes(sp[0],"utf-8"),sp[1])

#####################################

## PHASE 2 (2)
def initDBTerms():
    database = db.DB()
    DB_File = "te.idx"
    database.set_flags(db.DB_DUP) #Important! declare duplicates allowed
    database.open(DB_File,None,db.DB_BTREE,db.DB_CREATE)
    insertTerms(database)
    return

def insertTerms(database):
    curs = database.cursor()
    fpr = open("terms.txt")
    for line in enumerate(fpr):
        sp = line[1].split(":") # 0 is key 1 is data
        database.put(bytes(sp[0],"utf-8"),sp[1])

#####################################

## PHASE 2 (3)
def initDBPDates():
    database = db.DB()
    DB_File = "da.idx"
    database.set_flags(db.DB_DUP) #Important! declare duplicates allowed
    database.open(DB_File,None,db.DB_BTREE,db.DB_CREATE)
    insertPDates(database)
    return

def insertPDates(database):
    curs = database.cursor()
    fpr = open("pdates.txt")
    for line in enumerate(fpr):
        sp = line[1].split(":") # 0 is key 1 is data
        database.put(bytes(sp[0],"utf-8"),sp[1])

#####################################

## PHASE 2 (4)
def initDBPr():
    database = db.DB()
    DB_File = "pr.idx"
    database.set_flags(db.DB_DUP) #Important! declare duplicates allowed
    database.open(DB_File,None,db.DB_BTREE,db.DB_CREATE)
    insertPrices(database)
    return

def insertPrices(database):
    curs = database.cursor()
    fpr = open("prices.txt")
    for line in enumerate(fpr):
        sp = line[1].split(":") # 0 is key 1 is data
        k = "{:>12}".format(sp[0])
        database.put(bytes(k,"utf-8"),sp[1])


#####################################


def main():
    #the main code for the software applications
    #enable a print to ask the user for their username
    startSort = time.clock()
    print("Starting sorting...")
    sysSort("prices.txt")
    sysSort("ads.txt")
    sysSort("terms.txt")
    sysSort("pdates.txt")
    endSort = time.clock()
    sortTime = "Sorting complete. Time Elapsed: {0}sec".format(endSort - startSort)
    print(sortTime)
    print("Creating index dbs'...")
    startIdx = time.clock()
    initDBAd()
    initDBTerms()
    initDBPDates()
    initDBPr()
    endIdx = time.clock()
    idxTime = "Index dbs' created. Time Elapsed: {0}sec".format(endIdx - startIdx)
    print(idxTime)
    return

if __name__ == "__main__":
    main()
