# This is the main code for mini project 2 in CPUT 291
# Authors: Curtis Goud, Jose Ramirez

# Definition: The program will ask for a file to parse. Then it will run the
# desired queries and output the data, as well as some stats

# may not need these
import sqlite3
import time
# for the regex if required
import re

def printQuery(queryResult):
    # Parameters:
    #   queryResult - is the list of rows from the query result
    print(queryResult)
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
    termQuery = "[0-9a-zA-Z_-]+|[0-9a-zA-Z_-]+%"
    # these 2 patterns we may not be using. Maybe just for error checking to make
    # sure that the queries are inputted correctly
    expression = "{0}|{1}|{2}|{3}|{4}".format(dateQueryPattern,
     priceQueryPattern, locationQueryPattern, catQuery, termQuery)
    query = "{0}( {0})*".format(expression)
    queryRe = re.compile(query)
    expressionSplit = re.compile(expression)

    # check if the condition is in the correct format
    if queryRe.match(condition) is not None:
        # continue with the query
        # split by the expressions to check what the expressions are individually
        listOfExp = expressionSplit.findall(condition)
        for exp in listOfExp:
            #check if each of the conditions match an existing one
            if re.match(dateQueryPattern, exp) is not None:
                # handle the query for date
            elif re.match(priceQueryPattern, exp) is not None:
                # handle the query for price
            elif re.match(locationQueryPattern, exp) is not None:
                # handle the query for location
            elif re.match(catQuery, exp) is not None:
                # handle the query for the category
            elif re.match(termQuery, exp) is not None:
                # handle the query for terms
    else:
        return "Query condition was not in the correct format. Please try again"


    return "Under Construction"

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
        printQuery(queryResult)


    return

def main():
    # handle any initialization and make sure that the the files have been created
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
