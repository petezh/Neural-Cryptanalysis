# this code will:
# parse through each collection of papers
# construct snippets of text
# compile them in one document

import re
import glob

def main():
    
    # select folders
    folders = ["abernathy", "berk", "castro", "fletcher", "kauffman", "rubczenski", "eggan", "911report", "govreport"]
    allWords = list()

    for folderName in folders:
        
        # find all textfiles
        textFiles = glob.glob(folderName +"/*.txt")

        # extract and compile words from all
        for fileName in textFiles:
            allWords = allWords + extract(fileName)

    length = 150
    snip(allWords, length)    


# parsing function
def extract(fileName):

    file = open(fileName, 'r', encoding="utf8")

    # store words here
    alltext = ""
    
    for line in file:

        # scrub line of anything but letters and spaces
        line = re.sub("[^a-zA-Z]+", '', line)

        alltext = alltext + line
            
    return alltext.split()


# make snippets
def snip(wordList):

    # define output file
    file = open('snippets.txt', 'w')

    snippet = ""
    counter = 0
    nosnips = 0

    # make word snippets
    for word in wordList:
        
        snippet = snippet + str(word)
        counter = counter + 1
        if counter==length:

            # write to file in all upper
            snippet = re.sub(r'[^a-zA-Z ]+', '', snippet)
            file.write(snippet.upper()+"\n")
            counter = 0
            snippet = ""
            nosnips = nosnips+1

        
    print("Total Snips: "+str(nosnips))
    file.close()

            
if __name__ == '__main__':
    main()

