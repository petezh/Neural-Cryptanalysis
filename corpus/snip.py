import re

def main():

    words = open('alltext.txt', 'r')
    allWords = eval(next(words))

    snip(allWords, 500)


# make snips
def snip(wordList, length):

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






