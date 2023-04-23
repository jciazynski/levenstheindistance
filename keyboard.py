import numpy as np

def levenstheinerrors(word1,word2,errors): #checking levenstein distance between two words (how different two words are)
    matrix = np.zeros((len(word1)+1,len(word2)+1))
    for i in range(len(word1)+1):
        for j in range(len(word2)+1):
            if j==0:
                matrix[i][j]=i
                continue
            if i==0:
                matrix[i][j]=j
                continue
            if word1[i-1]==word2[j-1]:
                matrix[i][j] = matrix[i-1][j-1]
            elif word2[j-1] in errors.keys() and word1[i-1] in errors[word2[j-1]] or word1[i-1] in errors.keys() and word2[j-1] in errors[word1[i-1]]: #if the error is in our database, cost will be lower
                matrix[i][j] = matrix[i-1][j-1]+0.4
            else:
                matrix[i][j] = min(matrix[i-1][j],matrix[i][j-1],matrix[i-1][j-1])+1  
    return matrix[i][j]


def autocorrect(word1,errors): #this function checks whether we should change a given word to other one, which is in our dictionary
    mindist = 100
    with open("words20k.txt", "r") as file: #basically checks for all words in file, which one is the closest to our word
        for word2 in file:
            dist = levenstheinerrors(word1,word2.strip("\n"),errors)  #use levensthein distance to correct a word
            if dist < mindist: #finding the shortest
                mindist = dist
                result = word2
                if mindist < float(len(word1)/10): #really small margin for finding the exact same / very similar word
                    print(result)
                    return result
    if mindist < float(1.5+len(word1)/5): #some bigger margin to find sufficiently similar word
        return result
    else: #if there is no similar enough word, don't change it
        return word1


def filecorrect(errors): #autocorrecting word after word in an input file, result written in output file
    with open("input.txt", "r") as input:#reading words from input file
        text = input.read()
        input.close()
    splitted_text = text.split()
    counter = 0 #in every line of a file input.txt, there are 10 words+dots+comas, we can use it to make newlines
    with open("output.txt", "w") as output: #writing words to second file
        for word1 in splitted_text:
            counter+=1
            if word1.isalpha() == True: 
                output.write((autocorrect(word1,errors)).strip("\n")) #autocorrecting word
            else:
                output.write(word1) #when there will be dot, coma or other thing which is not a word, do nothing with that
            if counter%10 == 0: #making newlines or spaces, if the input file is different, we can change that
                output.write("\n")
            else:
                output.write(" ") 

                      
errors = { #this can be easily changed depending on the preferences of the user
    "o": "pi",
    "y": "tz",
    "m": "nk",
    "g": "hf",
    "e": "rws"}
#triggering a function
filecorrect(errors)
