# This is the parser code for the Mini Project 2 task given for CMPUT 291
# Authors: Jose Ramirez, Curtis Goud

# Definition: This program will take some xml input and produce 4 .txt files
# that will be used later to be indexed

import sqlite3
import time
# lxml is the main parser that we are using for better simplicity
from lxml import *

def getInformation(xmlTag, xmlLine):
    # get all of the information that is between the the xmlTag
    # xmlTag format: "ad" where it is part of <ad></ad>
    # return: the returned string is the information within the tags

    startTag = "<" + xmlTag + ">"
    endTag = "</" + xmlTag + ">"
    startTagLen = len(startTag)

    posStartTag = xmlLine.find(startTag) + startTagLen
    posEndTag = xmlLine.find(endTag)

    return xmlLine[posStartTag:posEndTag]

def readXMLFile():
    # here we will be reading the xml or text file. From here we will be parsing it

    return

def generateTerms():
    return

def generatePDates():
    return

def generatePrices():
    return

def generateAds():
    return

# def main():
#     # test the functions
#     xmltest = "<ad> This is a testing string</ad>"
#     print(getInformation("ad", xmltest))
#     return
#
# if __name__ == "__main__":
#     main()
