#!/usr/bin/env python
import sys;

def k_skip_n_grams_per_song(n,k=None):
    for line in sys.stdin:
        # Use the input from the preprocessed file to split the line on whitespace 
        split_words = line.split()
        # Takes care of if n=1 so function is more efficient and can bypass unigrams (since unigrams is just occurrances of one word)
        if n == 1:
            words = split_words
        else:
            words = []
            if k is not None:
                # Happens when a skip occurs. Calls all new combinations from the 1-skip-2-gram by adding the word n away from the 
                # word at the first index of the bigram.
                for i in range(len(split_words)-n):
                    last_i = i+n
                    words.append(split_words[i:i+n-k] + [split_words[last_i]])
            for i in range(len(split_words)-n+1):
                # if it is an ngram then start appending words here. Otherwise we will already have words here from the skipgram
                words.append(split_words[i:i+n])
        for single_word_or_list in words:
            if n != 1:
                word = ""
                for i in range(len(single_word_or_list)):
                    # case where bigram or trigram
                    if i != 0:
                        word += " "
                    word += single_word_or_list[i]
                print(word.lower() + "\t1")
            else:
                print(single_word_or_list.lower() + "\t1")

def main():
    
    k_skip_n_grams_per_song(1)
    
if __name__ == "__main__": main()