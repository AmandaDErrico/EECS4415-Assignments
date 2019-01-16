#!/usr/bin/env python
import sys;

def reducer_list():
    previous = None
    sums = 0
    # this will be used for reading the sorted mapper and accumulating the values of the same keys
    for line in sys.stdin:
        # split on tab since the mapper printed a tab for each map task
        key, value = line.split( '\t' )
        if key != previous:
            if previous is not None:
                # if there are accumulated song ids, print them here and separate by , and space.
                # Otherwise, songL is an empty list since it is the beginning of the file
                song_ids = ""
                for i in range(len(songL)):
                    if i != 0:
                        song_ids += ", "
                    song_ids += songL[i]
                print(previous + ":" + '\t' + song_ids)
            previous = key
            songL = []
        
        # New song_id added to the list, but only if it is not there
        song_num = value.strip()
        if song_num not in songL:
            songL.append(song_num)

    # prints the last line since previous is still saved
    print(previous + ":" + '\t' + song_ids)      


def main():

    reducer_list()

if __name__ == "__main__": main()	


	

	
