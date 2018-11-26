# This is the main code for mini project 2 in CPUT 291
# Authors: Curtis Goud, Jose Ramirez

# Definition: The program will ask for a file to parse. Then it will run the
# desired queries and output the data, as well as some stats

# may not need these
from parser import *
from bsddb3 import db
import time
# for the regex if required
import re

databasePr = db.DB()
databaseAd = db.DB()
databaseTe = db.DB()
databaseDa = db.DB()


def initDBs():
    ##Comp function must be set before opening
    databaseTe.set_bt_compare(termComp)
    databaseDa.set_bt_compare(dateComp)
    databasePr.set_bt_compare(priceComp)
    databasePr.open("pr.idx")
    databaseAd.open("ad.idx")
    databaseTe.open("te.idx")
    databaseDa.open("da.idx")
    return

def printQuery(adsList,mode="full"):
    # Parameters:
    #   queryResult - is the list of rows from the query result

    if mode == "full":
        for x in adsList:
            print("Ad Id: " + x[0].decode("utf-8"))
            print("Ad Info: " + x[1].decode("utf-8"))
    elif mode == "brief":
        for x in adsList:
            print("Ad Id: " + x[0].decode("utf-8") + " Title: " + getInformation("ti",x[1].decode("utf-8")))
    return

def query(output, condition):
    # Parameters:
    #   output - the output flag of how much to query. Either True or False
    #   condition - The condition statement of what to query for

    # need to parse the condition to determine the 5 type of queries
    # this is going to require regex

    # the 5 terms to look for are as follows
    # - term: will just be a word
    # - date: the date and its ranges
    # - price: the price range
    # - location: check for the location
    # - cat: check for the category of the ad

    # use the following query library
    # alphanumeric    ::= [0-9a-zA-Z_-]
    # numeric		  ::= [0-9]
    # date            ::= numeric numeric numeric numeric '/' numeric numeric '/' numeric numeric
    # datePrefix      ::= 'date' whitespace* ('=' | '>' | '<' | '>=' | '<=')
    # dateQuery       ::= datePrefix whitespace* date
    # price		      ::= numeric+
    # pricePrefix     ::= 'price' whitespace* ('=' | '>' | '<' | '>=' | '<=')
    # priceQuery	  ::= pricePrefix whitespace* price
    # location	      ::= alphanumeric+
    # locationPrefix  ::= 'location' whitespace* '='
    # locationQuery	  ::= locationPrefix whitespace* location
    # cat		      ::= alphanumeric+
    # catPrefix  	  ::= 'cat' whitespace* '='
    # catQuery	      ::= catPrefix whitespace* cat
    # term            ::= alphanumeric+
    # termSuffix      ::= '%'
    # termQuery       ::= term | term termSuffix
    # expression      ::= dateQuery | priceQuery | locationQuery | catQuery | termQuery
    # query           ::= expression (whitespace expression)*


    dateQueryPattern = "date *(?:=|>|<|>=|<=) *[0-9]{4}/[0-9]{2}/[0-9]{2}"
    priceQueryPattern = "price *(?:=|>|<|>=|<=) *[0-9]+"
    locationQueryPattern = "location *= *[0-9a-zA-Z_-]+"
    catQuery = "cat *= *[0-9a-zA-Z_-]+"
    termQuery = "[0-9a-zA-Z_-]+%|[0-9a-zA-Z_-]+"
    # these 2 patterns we may not be using. Maybe just for error checking to make
    # sure that the queries are inputted correctly
    expression = "{0}|{1}|{2}|{3}|{4}".format(dateQueryPattern,
     priceQueryPattern, locationQueryPattern, catQuery, termQuery)
    query = "{0}( {0})*".format(expression)
    queryRe = re.compile(query)
    expressionSplit = re.compile(expression)

    ads = set() # Set with ad ids
    setInit = False #Necessary to prevent duplicates
    # check if the condition is in the correct format
    if queryRe.match(condition) is not None:
        # continue with the query
        # split by the expressions to check what the expressions are individually
        listOfExp = expressionSplit.findall(condition)

        for exp in listOfExp:
            #check if each of the conditions match an existing one
            if re.match(dateQueryPattern, exp) is not None:
                # handle the query for date
                dates = queryDate(exp)
                dts = set()
                for i in dates:
                    dts.add(i)
                if len(ads) is 0 and not setInit:
                    #on 0 len fill the new set
                    ads = ads.union(dts)
                    setInit = True
                else:
                    #else check for intersection
                    ads = ads.intersection(dts)
            elif re.match(priceQueryPattern, exp) is not None:
                # handle the query for price
                print(exp)
            elif re.match(locationQueryPattern, exp) is not None:
                # handle the query for location
                locs = queryLoc(exp)
                lcs = set()
                for i in locs:
                    #init set for adding/intersecting
                    lcs.add(i)
                if len(ads) is 0 and not setInit:
                    #on 0 len fill the new set
                    ads = ads.union(lcs)
                    setInit = True
                else:
                    #else intersect
                    ads = ads.intersection(lcs)
            elif re.match(catQuery, exp) is not None:
                # handle the query for the category
                cats = queryCats(exp)
                cts = set()
                for i in cats:
                    #init set for adding/intersecting
                    cts.add(i)
                if len(ads) is 0 and not setInit:
                    #on 0 len fill the new set
                    ads = ads.union(cts)
                    setInit = True
                else:
                    #else intersect
                    ads = ads.intersection(cts)
            elif re.match(termQuery, exp) is not None:
                # handle the query for terms
                # TODO: Not catching wildcard
                terms = queryTerm(exp)
                ts = set()
                for i in terms:
                    #init set for adding
                    ts.add(i)
                if len(ads) is 0 and not setInit:
                    #add if new set
                    ads = ads.union(ts)
                    setInit = True
                else:
                    #else intersect
                    ads = ads.intersection(ts)
    else:
        return "Query condition was not in the correct format. Please try again"

    adsList = queryAds(ads)
    return adsList

def queryMainKey(expression, type):

    lowerStr = str.lower(expression)
    strSign = lowerStr.strip(type)
    content = strSign.strip(">=<")

    outlines = []
    equals = [] #Filled with equal dates, added if = is present
    db = None
    if type == "date":
        db = databaseDa
    elif type == "price":
        db = databasePr

    curs = db.cursor()
    curs.set_range(content.encode("utf-8"))
    # use the cursor
    iter = curs.current()
    while iter:
        ln = iter[1].decode("utf-8").strip(" \n")
        lines = ln.split(",")
        adID = lines[0]
        equals.append(adID)
        iter = curs.next_dup()

    if "=" in strSign:
        for x in enumerate(equals):
            outlines.append(x[1])

    if ">" in strSign:
        ##Go forward
        next = curs.next()
        while next:
            ln = next[1].decode("utf-8").strip(" \n")
            lines = ln.split(",")
            adID = lines[0]
            outlines.append(adID)
            next = curs.next()
    elif "<" in strSign:
        ##GO back
        next = curs.prev_nodup()
        while next:
            ln = next[1].decode("utf-8").strip(" \n")
            lines = ln.split(",")
            adID = lines[0]
            outlines.append(adID)
            next = curs.prev_nodup()


    print("Print for "+ type)
    #for i in enumerate(outlines):
    #  print(i)

    return outlines

################# PRICES ##########################
def queryPrice(price):
    return queryMainKey(price, "price")

def priceComp(ourSearchKey, treeKey):
    if ourSearchKey == treeKey:
        return 0
    if ourSearchKey > treeKey:
        return 1
    else:
        return -1
################# PRICES ##########################

################# LOCATION ########################
def queryLoc(location):
    #TODO: this may need to change to be faster
    # for location we are going to be searching from the
    location = str.lower(location)
    location = location.replace("location", "")
    loc = location.strip("=")
    # we are going to get all of the aid based from the locations from the pdates
    # index database
    outlines = []
    db = databaseDa
    curs = db.cursor()
    curs.first()
    iter = curs.current()
    while iter:
        data = iter[1].decode("utf-8").strip(" \n")
        list = data.split(",")
        currentLoc = list[2]
        if str.lower(currentLoc) == loc:
            outlines.append(list[0])
        iter = curs.next()

    #for i in enumerate(outlines):
    #    print(i)

    return outlines

################# LOCATION ########################

################# TERMS ###########################

def queryTerm(tq):
    ## At this point, if our query has a suffix (%) it has been removed from the string and suffix is true
    ## Returns a list of tuples (b'key',b'data')
    ## THE ABOVE DATA MUST BE DECODED WHEN USED
    suffix = False
    if "%" in tq:
        suffix = True
        tq = tq.strip("%")

    tq = str.lower(tq)
    outlines = []
    db = databaseTe
    curs = db.cursor()
    curs.set_range(tq.encode("utf-8"))
     # use the cursor
    iter = curs.current()
    while iter:
        outlines.append(iter[1].decode("utf-8").strip(" \n"))
        iter = curs.next_dup()

    if suffix:
        next = curs.next()
        nextKey = next[0].decode("utf-8")
        done = False
        if tq in nextKey and not done:
            outlines.append(next[1].decode("utf-8").strip(" \n"))
        else:
            done = True


    #for i in enumerate(outlines):
    #    print(i)


    return outlines

def termComp(ourSearchKey, treeKey):
    if ourSearchKey == treeKey:
        return 0
    if ourSearchKey > treeKey:
        return 1
    else:
        return -1

################# TERMS ###########################

################# DATES ###########################

def queryDate(dq):
    ##
    tq = str.lower(dq)
    tq = tq.strip("date")
    dt = tq.strip(">=<")

    outlines = []
    equals = [] #Filled with equal dates, added if = is present
    db = databaseDa
    curs = db.cursor()
    curs.set_range(dt.encode("utf-8"))
    # use the cursor
    iter = curs.current()
    while iter:
        ln = iter[1].decode("utf-8").strip(" \n")
        lines = ln.split(",")
        adID = lines[0]
        equals.append(adID)
        iter = curs.next_dup()

    if "=" in tq:
        for x in enumerate(equals):
            outlines.append(x[1])

    if ">" in tq:
        ##Go forward
        next = curs.next()
        while next:
            ln = next[1].decode("utf-8").strip(" \n")
            lines = ln.split(",")
            adID = lines[0]
            outlines.append(adID)
            next = curs.next()
    elif "<" in tq:
        ##GO back
        next = curs.prev_nodup()
        while next:
            ln = next[1].decode("utf-8").strip(" \n")
            lines = ln.split(",")
            adID = lines[0]
            outlines.append(adID)
            next = curs.prev_nodup()



    #for i in enumerate(outlines):
    #    print(i)

    return outlines

def dateComp(ourSearchKey, treeKey):
    if ourSearchKey == treeKey:
        return 0
    if ourSearchKey > treeKey:
        return 1
    else:
        return -1

################# DATES ###########################

################# CATS ###########################

def queryCats(cq):
    ##
    cq = str.lower(cq)
    cq = cq.strip("cat")
    cq = cq.strip("=")
    cq = cq.strip(" ")

    outlines = []
    db = databaseDa
    curs = db.cursor()
    # use the cursor
    iter = curs.first()
    while iter:
        ln = iter[1].decode("utf-8").strip("\n")
        lines = ln.split(",")
        adID = lines[0]
        cat = lines[1]
        if str.lower(cq) == cat:
            outlines.append(adID)
        iter = curs.next()

    #for i in enumerate(outlines):
    #    print(i)

    return outlines

################# CATS ###########################

################# ADS ###########################
def queryAds(adList):
    ##
    outlines = []
    db = databaseAd
    curs = db.cursor()

    for i in adList:
        outlines.append(curs.set(i.encode("utf-8")))

    return outlines
################# ADS ###########################


def main_loop():
    # start the while loop for the application. The user will be prompted to input
    # a specific format in order to ensure the query is correct
    print("**Must input in the format 'output=full/brief condition'**")
    print("**To leave the application please type 'exit'\n")
    # set any variables
    while (True):
        # prompt the user for input
        inputStr = input(">> ")
        if inputStr == "exit":
            #leave the application
            break
        # get the split arguments. We are going to assume that the user put in the
        # correct format
        outputArg = inputStr[:inputStr.find(" ")]
        conditionArg = inputStr[inputStr.find(" ")+1:]
        print("Output argument: " + outputArg)
        print("Condition argument: " + conditionArg)


        # get the description of the flag
        outputFlag = False; # automatically is set to brief
        outputArgFlag = outputArg.split("=")[1]
        if (outputArgFlag == "full"):
            outputFlag = True

        queryResult = query(outputFlag, conditionArg)
        printQuery(queryResult,outputArgFlag)


    return

def main():
    # handle any initialization and make sure that the the files have been created

    initDBs()

    ##TESTS
    queryTerm("cAmEra%")
    queryDate("date>=2018/11/05")
    queryCats("cat=art-collectibles")
    queryLoc("location=Edmonton")
    queryPrice("price>100")
    ##

    print("Welcome to the query interface! Please ensure that the following files")
    print("Have been created:")
    print("- ad.idx")
    print("- da.idx")
    print("- pr.idx")
    print("- te.idx\n")
    print("If not please make those files with the parser.py and the index.py program.\n")

    main_loop()

    print("Leaving the query interface application...Good bye!")
    return

if __name__ == "__main__":
    main()
