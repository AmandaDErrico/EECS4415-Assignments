import re, csv, sys;
from nltk.corpus import stopwords; 
from nltk.tokenize import word_tokenize;
from string import punctuation;

reader = csv.reader(sys.stdin)
next(reader)


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
                # Replace ',' with '' so numbers like 10,000 wont be separated
                if "," in t:
                    t = t.replace(",", "")
                # Replace '-' with " " so words such as about-think (which appear in songdata) doesn't merge into one word about think,
                # but rather two separate words
                elif "-" in t:
                    t = t.replace("-", " ")                 
                if stopword_text != "":
                    stopword_text += " "
                stopword_text += t
    # clear any punctuation
    clean_lyrics = re.sub( r'[^\w\s]', '', stopword_text)
    return clean_lyrics



for line in reader:
    # our preprocessor file will only print the important lyrics of each song and will be split on whitespace
    elim_stop = _eliminate_stopwords(line[3])
    clean_lyrics = re.sub(r'^\W+|\W+$', '', elim_stop)
    # any remaining commas put a space
    clean_lyrics = clean_lyrics.replace(",", " ")
    print(clean_lyrics)        
