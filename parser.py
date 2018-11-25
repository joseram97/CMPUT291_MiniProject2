# This is the parser code for the Mini Project 2 task given for CMPUT 291
# Authors: Jose Ramirez, Curtis Goud

# Definition: This program will take some xml input and produce 4 .txt files
# that will be used later to be indexed

import sqlite3
import time
# lxml is the main parser that we are using for better simplicity
#from lxml import *

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

def readXMLFile():
    # here we will be reading the xml or text file. From here we will be parsing it

    return

def generateTerms():
    return

def generatePDates():
    return

def generatePrices(file):
    #TODO: Change file name later
    fpr = open(file)
    fpw = open("prices.txt","w+")
    for line in enumerate(fpr):
        if getInformation("ad",line[1]) is not "":
            price = getInformation("price",line[1])
            adID = getInformation("aid",line[1])
            category = getInformation("cat",line[1])
            location = getInformation("loc",line[1])
            fpw.write(price + "," + adID + "," + category + "," + location + "\r\n")
            print(price + ":" + adID + "," + category + "," + location)
    fpr.close()
    fpw.close()
    return

def generateAds(file):
    #TODO: Change file name later
    fpr = open(file)
    fpw = open("ads.txt","w+")
    for line in enumerate(fpr):
        if getInformation("ad",line[1]) is not "":
            adID = getInformation("aid",line[1])
            ad = "<ad>" + getInformation("ad",line[1]) + "</ad>"
            fpw.write(adID + ":" + ad + "\r\n")
            print(adID + ":" + ad)
    fpr.close()
    fpw.close()
    return


def main():
     # test the functions
     #xmltest = "<ad> This is a testing string</ad>"
     #print(getInformation("ad", xmltest))
     generateAds("data.xml")
     generatePrices("data.xml")
     return

if __name__ == "__main__":
    main()
