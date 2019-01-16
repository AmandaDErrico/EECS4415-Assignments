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

def calculate_artists_profiles():

    reader = csv.reader(open(sys.argv[1], "rt")) #read  the files into the reader
    songs = {}

    #Skip the first line with teh column names
    next(reader)
    for row in reader:
        if row[0] not in songs.keys():
            # take artist as key and stopwords removed as value
            formatted = _eliminate_stopwords(row[3])
            songs[row[0]] = formatted
        else:
            #use this for removed stopwords
            formatted = _eliminate_stopwords(row[3])
            songs[row[0]] = songs[row[0]] + " \n " + formatted

    #count the number of artists - N
    artistsCount = len(songs.keys())

    #PERFORM SAME TF*IDF BUT WITH THE RULES ABOVE
    #Refer to the first file for the comments about the code
    all_words = {} # remembers every single word
    for akey in songs:
        lyrics=songs[akey].lower()
        words = re.findall(r'\w+', lyrics)
        wordsSet = set(words)
        for aword in wordsSet:
            if aword not in all_words.keys():
                all_words[aword] = 1
            else:
                all_words[aword] += 1

    for akey in all_words:
        all_words[akey] = log10(artistsCount/all_words[akey])			

    # Used for list of each artist and their tf-idf scores
    final_sorted = []
    for akey in songs:
        word_counts = {}
        word_tf = {}
        word_tf_idf = {}
        count = 0
        lyrics=songs[akey].lower()
        words = re.findall(r'\w+', lyrics) #r means that the regex is next
        for aword in words:
            if aword not in word_counts.keys():
                word_counts[aword] = 1
            else:
                word_counts[aword] += 1
            count +=1

        for aword in word_counts:
            word_tf[aword] = word_counts[aword]/count

        for aword in word_tf:
            word_tf_idf[aword] = word_tf[aword]*all_words[aword]
            
        #Print the top 100 words as per spec
        sorted_tf_idf_top_100 = sorted(word_tf_idf.items(), key=lambda kv: kv[1], reverse = True)
        artist_tf_words = [akey, sorted_tf_idf_top_100]
        # append list into final list
        final_sorted.append(artist_tf_words)
    return final_sorted

def artist_jaccard():
    
    artist_list = calculate_artists_profiles()

    # for IDF part - computing the N for idf
    artistsNumber = len(artist_list)

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
    while((int(firstArg) < 1) or (int(secondArg) < 1) or (int(firstArg) > artistsNumber) or (int(secondArg) > artistsNumber)):
        pprint("The two ints are not the existing song IDs. Please try again:" + " \n")
        firstArg = input("First ID:" + " \n")
        secondArg = input("Second ID:" + " \n")
    
    firstArgRange = int(firstArg)
    secondArgRange = int(secondArg)

    firstArtistProf = artist_list[firstArgRange-1][1]
    secondArtistProf = artist_list[secondArgRange-1][1]
    
    
    wordListFirstArtist = []
    wordListSecondArtist = []
    # Compute list of words:
    for word in firstArtistProf:
        wordListFirstArtist.append(word[0])
        
    for word in secondArtistProf:
        wordListSecondArtist.append(word[0])
    
    #find the Sets of those two songs
    firstArtistSet = set(wordListFirstArtist)
    secondArtistSet = set(wordListSecondArtist)

    #find the intersection and union of the two words sets 
    intersected = firstArtistSet.intersection(secondArtistSet)
    unioned = firstArtistSet.union(secondArtistSet)

    #find jaccard
    jaccard = len(intersected)/len(unioned)
    # Return tuple with jaccard and the first arg and second arg given to compute the jaccard (for error checking, proper computation with
    # no error cases)
    return (jaccard, firstArg, secondArg)

def main():
    jaccard = artist_jaccard()
    print("The Jaccard index of the two artists of ID",int(jaccard[1]),"and",int(jaccard[2]),"is:")
    print(round(jaccard[0], 3))

if __name__ == "__main__": main()  