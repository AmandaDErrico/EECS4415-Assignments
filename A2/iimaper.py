#!/usr/bin/env python
import sys;

def song_map_id():
    song_id = 0
    for line in sys.stdin:
        song_id += 1
        # Use the input from the preprocessed file to split the line on whitespace 
        split_words = line.split()
        for word in split_words:
            print(word.lower() + "\t" + str(song_id))


def main():
    
    song_map_id()
    
if __name__ == "__main__": main()
