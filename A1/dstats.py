import csv; import math; import sys; 
from nltk.corpus import stopwords; 
from nltk.tokenize import word_tokenize;
from string import punctuation;
from operator import itemgetter;
import re;

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np;
import matplotlib.pyplot as plt;


def numOfArtists(dict_of_artists):
    # Return an int with number of artists, input must be dictionary
    return len(dict_of_artists)

def numOfSongs(dict_of_artists):
    # Return sum of length of dictionary values
    dsum = 0
    for val in dict_of_artists.values():
        dsum += len(val)
    # Append each list into one big list
    return dsum

def avgNumOfSongs(dict_of_artists):
    # Return average number of songs per artist/band
    numS = numOfSongs(dict_of_artists)
    numA = numOfArtists(dict_of_artists)
    avgNofS = numS / numA
    return avgNofS

def avgNumOfWords(dict_of_artists):
    # Return average num of unique words per song in collection
    words = _unique_dict(dict_of_artists)[1]
    return words / numOfSongs(dict_of_artists)

def pairsOfArtistAvgNumOfWords(dict_of_artists):
    # Return pairs of the artists and the average num of unique words per song they sing
    wordsPerArtist = {}
    # Take the dictionary with unique words in helper function
    uniqueD = _unique_dict(dict_of_artists)[0]
    
    alphanum_key = lambda key: [re.sub('([\W_]+)', '', key.lower())]
    artistStats = sorted(uniqueD, key = alphanum_key)
    artists = ""
    for artist in artistStats:
        avgW = uniqueD[artist][0]/uniqueD[artist][1]
        wordsPerArtist[artist] = avgW
        artists += artist + ": " + str(round(avgW, 3)) + "\n"
    return (artists, wordsPerArtist)


# Helper functions

def _get_dict():
    # Read stdin
    reader = csv.reader(sys.stdin)
    next(reader)
    d = {}
    for row in reader:
        if row[0] not in d:
            d[row[0]] = []
        d[row[0]].append(row[1:])

    return d

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

def _unique_text_set(etext):
    # Returns a list of the UNIQUE lyrics text with stopwords eliminated
    stopW_list_lower = _eliminate_stopwords(etext).lower().split()
    unique_set = set(stopW_list_lower)
    return unique_set

def _unique_dict(dict_of_artists):
    # Return tuple of dictionary with 1st element of tuple:
    # Key: Artist
    # Value: list [total unique words an artist sings, number of songs an artist has]
    # 2nd element of tuple:
    # Accumulated number of unique words
    # dict_of_artists is in the format of _get_dict function where value is a nested list of songs
    total_words = 0
    total_words_per_A = 0
    new_d = {}
    for a in dict_of_artists:
        for song in dict_of_artists[a]: # accessing all songs of particular artist
            num_unique_words_per_song = len(_unique_text_set(song[2]))
            # append the unique words to a string and have the value be number of songs for one artist
            total_words_per_A += num_unique_words_per_song
        new_d[a] = [total_words_per_A, len(dict_of_artists[a])]
        # append total words to local variable to use in part 4
        total_words += total_words_per_A
        # Once done iterating through one artist, initialize total words per artist back to 0 for new artist
        total_words_per_A = 0
    return (new_d, total_words)

def main():
    
    # Use d for calling in functions
    d = _get_dict()

    a = numOfArtists(d)
    s = numOfSongs(d)
    avgS = avgNumOfSongs(d)

    outArtists = "Number of Artists: " + str(a) + "\n"
    outSongs = "Number of Songs: " + str(s) + "\n"
    outAvgSongs = "Average Number of Songs: " + str(round(avgS, 3)) + "\n"
    d2 = _unique_dict(d)

    avgNofW = avgNumOfWords(d)
    pairsAvgNofW = pairsOfArtistAvgNumOfWords(d)
    outAvgUniqueWords = "Average Number of Unique Words in the Collection: " + str(round(avgNofW, 3)) + "\n"
    outPairsAvgUniqueWords = "Average Number of Unique Words per Artist/Band sorted:\n" + pairsAvgNofW[0]

    out = outArtists + outSongs + outAvgSongs + outAvgUniqueWords + outPairsAvgUniqueWords
    out.strip()
    print(out)

    # Bar chart
    sorted_values = sorted(pairsAvgNofW[1].items(), key=lambda kv: kv[1], reverse=True)
    listObjects = []
    performance = []

    # Take top 10 based on value and append to objects (use as x-axis) and performance as y-axis
    range_value = 0
    if len(sorted_values) < 10:
        range_value = len(sorted_values)
    else:
        range_value = 10
    for i in range(range_value):
        artist = sorted_values[i][0]
        listObjects.append(artist)
        avgUniqueWords = sorted_values[i][1]
        performance.append(avgUniqueWords)
            
    objects = tuple(listObjects)
    y_pos = np.arange(len(objects))

    fig, ax = plt.subplots()
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.xlabel('Artists/Band')
    plt.ylabel('Average Number of Words')
    plt.title('Top 10 Pairs of Average Number of Unique Words per song of an Artist/Band')
    fig.autofmt_xdate()

    plt.savefig('plot.png')  
    
if __name__ == "__main__": main()