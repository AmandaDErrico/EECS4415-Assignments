#!/usr/bin/env python
import sys;


def reducer():
    previous = None
    sums = 0
    # this will be used for reading the sorted mapper and accumulating the values of the same keys
    for line in sys.stdin:
        # split on tab since the mapper printed a tab for each map task
        key, value = line.split( '\t' )
        if key != previous:
            if previous is not None:
                # if accumulated a sum more than 1, print the sum before previous gets the new value of key
                # Otherwise, sums = 1 since there is only one occurance
                print(str(sums) + '\t' + previous)
            previous = key
            sums = 0

        sums += int(value)

    # prints the last line since previous is still saved
    print(str(sums) + '\t' + previous)

def main():
    
    reducer()
    
if __name__ == "__main__": main()


	