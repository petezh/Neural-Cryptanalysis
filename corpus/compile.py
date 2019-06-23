# this code will:
# parse through each collection of papers
# construct 150 word texts
# compile them in one document

import numpy
import re
import glob
import csv

def main():
    
    # select folders
    folders = ["abernathy", "berk", "castro", "fletcher", "kauffman", "rubczenski"]
    allWords = list()

    for folderName in folders:
        
        # find all textfiles
        textFiles = glob.glob(folderName +"/*.txt")

        # extract and compile words from all
        for fileName in textFiles:
            allWords = allWords + extract(fileName)

    snip(allWords)    


# parsing function
def extract(fileName):

    file = open(fileName, 'r', encoding="utf8")

    # store words here
    alltext = ""
    
    for line in file:

        # scrub line of anything but letters and spaces
        line = re.sub(r'[^a-zA-Z ]+', '', line)

        alltext = alltext + line
            
    return alltext.split()


# make snippets
def snip(wordList):

    # define output file
    file = open('snippets.txt', 'w')

    snippet = ""
    counter = 0

    # make 150 word snippets
    for word in wordList:
        
        snippet = snippet + str(word) + " "
        counter = counter + 1
        if counter==150:

            
            file.write(snippet)
            counter = 0
            snippet = ""

        
        
    file.close()

            
if __name__ == '__main__':
    main()

extract("abernathy//ch1.txt")

