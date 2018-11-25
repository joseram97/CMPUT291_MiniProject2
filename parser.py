# This is the parser code for the Mini Project 2 task given for CMPUT 291
# Authors: Jose Ramirez, Curtis Goud

# Definition: This program will take some xml input and produce 4 .txt files
# that will be used later to be indexed

import sqlite3
import time
# lxml is the main parser that we are using for better simplicity
#from lxml import *
import re

def getInformation(xmlTag, xmlLine):
    # get all of the information that is between the the xmlTag
    # xmlTag format: "ad" where it is part of <ad></ad>
    # return: the returned string is the information within the tags

    startTag = "<" + xmlTag + ">"
    endTag = "</" + xmlTag + ">"
    startTagLen = len(startTag)

    posStartTag = xmlLine.find(startTag) + startTagLen
    posEndTag = xmlLine.find(endTag)

    if(posStartTag != -1 and posEndTag != -1):
        return xmlLine[posStartTag:posEndTag]
    else:
        return ""

def generateTerms(xmlfile):
    # this function is used to create the terms.txt file that is used for the
    # index phase of the project

    # create the terms.txt file
    termsFile = open("terms.txt", "w+")
    # open the xml file and read from it line by line
    xml = open(xmlfile, "r")
    # process each of the lines
    for line in enumerate(xml):
        if getInformation("ad", line[1]) is not "":
            # the line needs to be parsed
            titleString = getInformation("ti", line[1])
            description = getInformation("desc", line[1])
            id = getInformation("aid", line[1])
            # get a list of the terms along with the identy of the ad
            # TODO: Add the correct regex to split
            titleTerms = list(set(re.split("", titleString)))
            descriptionTerms = list(set(re.split("", description)))
            totalTerms = titleTerms + descriptionTerms
            for term in totalTerms:
                # TODO: check if the term is a correct regex
                if len(term) > 2:
                    # good to write to the terms.txt file

                    termsFile.write(lower(term) + ":" + id)
                    print(lower(term) + ":" + id) # make sure it works right
    xml.close()
    termsFile.close()
    return

def generatePDates(xmlfile):
    # this function is used to create the pdates.txt file that is used for the
    # index phase of the project

    # create the pdates.txt file
    pdatesFile = open("pdates.txt", "w+")
    # open the xml file
    xml = open(xmlfile, "r")

    # process each of the lines
    for line in enumerate(xml):
        if getInformation("ad", line[1]) is not "":
            # get the desired information
            date = getInformation("date", line[1])
            adID = getInformation("aid", line[1])
            category = getInformation("cat",line[1])
            location = getInformation("loc",line[1])
            pdatesFile.write(date + ":" + adID + "," + category + "," + location)
            print(date + ":" + adID + "," + category + "," + location)
    pdatesFile.close()
    xml.close()
    return

def generatePrices():
    #TODO: Change file name later
    fpr = open("data.xml")
    fpw = open("prices.txt","w+")
    for line in enumerate(fpr):
        if getInformation("ad",line[1]) is not "":
            price = getInformation("price",line[1])
            adID = getInformation("aid",line[1])
            category = getInformation("cat",line[1])
            location = getInformation("loc",line[1])
            fpw.write(price + "," + adID + "," + category + "," + location + "\r\n")
            print(price + "," + adID + "," + category + "," + location)
    fpr.close()
    fpw.close()
    return

def generateAds():
    return


def main():
     # test the functions
     #xmltest = "<ad> This is a testing string</ad>"
     #print(getInformation("ad", xmltest))
     generatePrices()
     return

if __name__ == "__main__":
    main()
