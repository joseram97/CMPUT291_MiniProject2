import os
from bsddb3 import db


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
        database.put(bytes(sp[0],"utf-8"),sp[1])

    #iter = curs.first()
    #while iter:
    #    print(iter)
    #    iter = curs.next()

#####################################


def main():
    #the main code for the software applications
    #enable a print to ask the user for their username
    sysSort("prices.txt")
    sysSort("ads.txt")
    initDBAd()
    initDBPr()
    return

if __name__ == "__main__":
    main()
