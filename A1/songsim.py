import csv, re, math, sys;
from pprint import pprint;
from math import log10;
from nltk.corpus import stopwords; 
from nltk.tokenize import word_tokenize;
from string import punctuation;

def _eliminate_stopwords(text):
    # Eliminates all stopwords and punctuation
    # All stopwords are in english lib
    stop_words = set(stopwords.words('english'))
    # Replace apostrophes with "" so important words are not separated and contraction words are taken as separate words
    tokened_text = word_tokenize(text.lower().replace("'", ""))
    stopword_text = ""
    for t in tokened_text:
        if len(t) > 1 and t not in stop_words:
            if t not in punctuation:
                stopword_text += " " + t
    return stopword_text

def calculate_song_profiles():

    reader = csv.reader(open(sys.argv[1], "rt"))    
    songs = {}
    next(reader)
    for row in reader:
        formatted = _eliminate_stopwords(row[3])
        songs[row[2]] = row[1], formatted
    
    # for IDF part - computing the N for idf
    songsNumber = len(songs.keys())
    # IDF PART BEGINS HERE	
    all_words = {} # remembers every single word FROM ALL THE LYRICS
   
    #COMPUTE THE DF: iterate over each lyrics in our dictionary
    for akey in songs:
        #convert the lyrics ot the lower case
        lyrics=songs[akey][1].lower()
        #use the regex to extract the words - forms a "list"
        words = re.findall(r'\w+', lyrics)
        #convert the list above to set - we only need the words, not their duplicates
        #DF term - number of documents the certain word appears in
        #Only single appearance of a word is required, therefore we dont need the duplicates
        wordsSet = set(words)
        #itirate over the set of words adn add them to the overall set of all words form all lyrics
        #compute the count of each word in each of the lyrics
        for aword in wordsSet:
            #count the words - if the word is NOT in the dictionary - add it and put count as 1
            if aword not in all_words.keys():
                all_words[aword] = 1
            #else, increment the counter for exisiting word	
            else:
                all_words[aword] += 1
    
    #COMPUTE THE IDF: Now that we have all the word counts from ALL songs - compute the IDF
    for akey in all_words:
        all_words[akey] = log10(songsNumber/all_words[akey])			
    final_sorted = []
    
    #COMPUTE THE TF: Itirate over the songs again - no other choice
    for akey in songs:
        word_counts = {}
        word_tf = {}
        word_tf_idf = {}
        count = 0
        #COnvert everything to the lower case
        lyrics=songs[akey][1].lower()
        #use the regex to extract the words - forms a "list"	
        words = re.findall(r'\w+', lyrics) #r means that the regex is next
        for aword in words:
            #Count every word in this lyric
            if aword not in word_counts.keys():
                word_counts[aword] = 1
            else:
                word_counts[aword] += 1
            #Count the total number of the words in the document	
            count +=1

        #DISPLAY TF for this song	
        #Arrange the term frequency in a separate dictionary - {word -> wordCount/totalWords}	
        for aword in word_counts:
            word_tf[aword] = word_counts[aword]/count
        #pprint(word_tf)

        # COMPUTE THE TF*IDF NOW - sort it in a separate dictionary
        for aword in word_tf:
            word_tf_idf[aword] = word_tf[aword]*all_words[aword]

        sorted_tf_idf = sorted(word_tf_idf.items(), key=lambda kv: kv[1], reverse = True)
        sorted_tf_idf_top_50 = sorted_tf_idf[:50]
        song_tf_words = [songs[akey][0], sorted_tf_idf_top_50]
        # append list into final list
        final_sorted.append(song_tf_words)
    return final_sorted

def song_jaccard():
    song_list = calculate_song_profiles()

    # for IDF part - computing the N for idf
    songsNumber = len(song_list)

    #Get the song IDs from the User
    firstArg = sys.argv[2]
    secondArg = sys.argv[3]

    #Try parsing the IDs first to make sure they are integers. Otherwise - exit.
    try: 
        firstArg = int(sys.argv[2])
    except:
        pprint("The type of the first passed argument is not int. Please try again")
        sys.exit()

    try: 
        secondArg = int(sys.argv[3])
    except:
        pprint("The type of the second passed argument is not int. Please try again")	
        sys.exit()	


    # Checking if the IDs are in the range of our dataset
    while((int(firstArg) < 1) or (int(secondArg) < 1) or (int(firstArg) > songsNumber) or (int(secondArg) > songsNumber)):
        pprint("The two ints are not the existing song IDs. Please try again:" + " \n")
        firstArg = input("First ID:" + " \n")
        secondArg = input("Second ID:" + " \n")

    firstArgRange = int(firstArg)
    secondArgRange = int(secondArg)

    firstSongProf = song_list[firstArgRange-1][1:][0]
    secondSongProf = song_list[secondArgRange-1][1:][0]
    

    wordListFirstSong = []
    wordListSecondSong = []
    # Compute list of words:
    for word in firstSongProf:
        wordListFirstSong.append(word[0])
        
    for word in secondSongProf:
        wordListSecondSong.append(word[0])
    
    #find the Sets of those two songs
    firstSongSet = set(wordListFirstSong)
    secondSongSet = set(wordListSecondSong)

    #find the intersection and union of the two words sets 
    intersected = firstSongSet.intersection(secondSongSet)
    unioned = firstSongSet.union(secondSongSet)

    #find jaccard
    jaccard = len(intersected)/len(unioned)
    # Return tuple with jaccard and the first arg and second arg given to compute the jaccard (for error checking, proper computation with
    # no error cases)
    return (jaccard, firstArg, secondArg)

def main():
    jaccard = song_jaccard()
    print("The Jaccard index of the two songs of ID",int(jaccard[1]),"and",int(jaccard[2]),"is:")
    print(round(jaccard[0], 3))

if __name__ == "__main__": main()