#import thinkAboutIt
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

#Helper Module - for debugging - outputs the set of the Artists
#Plug in your CSV

def calculate_artists_profiles():

    reader = csv.reader(sys.stdin) #read  the files into the reader

    #Comfirmed with prof!
    #IN THIS PART WE NEED TO CONCATENATE ALL OF THE SONGS BY THIS ARTIST
    #That Way the number of Artists = N in IDF = number of all concatenated songs 
    # our DF is the number of times a word appears in the CONCATENATED SONGS by ALL OF THE ARTISTS 

    songs = {}

    #Skip the first line with teh column names
    next(reader)
    # Use artist as key, removed stopwords lyrics as value
    for row in reader:
        if row[0] not in songs.keys():
            formatted = _eliminate_stopwords(row[3])
            songs[row[0]] = formatted
        else:
            #use this for removed stopwords
            formatted = _eliminate_stopwords(row[3])
            songs[row[0]] = songs[row[0]] + " \n " + formatted

    artistsCount = len(songs.keys())

    #PERFORM SAME TF*IDF BUT WITH THE RULES ABOVE
    #Refer to the first file for the comments about the code

    all_words = {} # remembers every single word

    for akey in songs:
        lyrics=songs[akey].lower()
        words = re.findall(r'\w+', lyrics)
        wordsSet = set(words) # takes the unique words for tf-idf
        for aword in wordsSet:
            if aword not in all_words.keys():
                all_words[aword] = 1
            else:
                all_words[aword] += 1

    # take all keys in all_words and take log over frequency
    for akey in all_words:
        all_words[akey] = log10(artistsCount/all_words[akey])			

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
        final_sorted.append(artist_tf_words)
    return final_sorted

def main():
    artist_prof_list = calculate_artists_profiles()
    for tf_idf in artist_prof_list:
        print(tf_idf[0])
        tf_words = tf_idf[1]
        for words in tf_words:
            pprint(words[0] + ': ' + str(round(words[1], 3)))
            
if __name__ == "__main__": main()