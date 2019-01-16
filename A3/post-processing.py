import sys, csv;
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np;
import matplotlib.pyplot as plt;
import matplotlib.ticker as ticker;



def hashtag_list(file):

    L = []
    dash_time = []

    with open(file, "rt") as f:
        for row in f.readlines():
        # eliminate rows in empty spaces
            if row != "":
                if row[0] == '#':
                    # take all hashtags
                    row = row.split()
                    dash_time.append(row)
                elif row[0] == '-':
                    # new time interval starts, append prev hastag values to total list of hastag vals per time
                    if len(dash_time) != 0:
                        L.append(dash_time)
                        # reset the new time interval
                        dash_time = []

    # take last elem (latest time to plot)
    L = L[-1]


    hashtags = []
    occurrances = []
    for tweet in L:
        # split on whitespace and move hashtags to hashtag list and occurrances to occurance list
        #t = tweet[0].split()
        hashtags.append(tweet[0])
        occurrances.append(int(tweet[1]))

    return [hashtags, occurrances]


def sentiment_list(file):

    with open(file, "rt") as f:
        first_line = f.readline()
        first_line = first_line.strip("\n")
        rowL = first_line.split("--")

        cat1 = rowL[1]
        cat2 = rowL[2]
        cat3 = rowL[3]
        cat4 = rowL[4]
        cat5 = rowL[5]    

        cat1List = []
        cat2List = []
        cat3List = []
        cat4List = []
        cat5List = []

        xtimes = []

        lines = f.readlines()

        for row in lines:
            row = row.strip("\n")
            rowL = row.split(",")
            if rowL != [''] and "" not in rowL:
                # take only values with sentiments, place times into xtimes and everything else into its respective category
                xtimes.append(rowL[0])
                cat1List.append(int(rowL[1]))
                cat2List.append(int(rowL[2]))
                cat3List.append(int(rowL[3]))
                cat4List.append(int(rowL[4]))
                cat5List.append(int(rowL[5]))


    return [xtimes, [cat1List, cat2List, cat3List, cat4List, cat5List], [cat1, cat2, cat3, cat4, cat5]]


def main():

    firstArg = sys.argv[1]
    while str(firstArg) != "outputA.txt" and str(firstArg) != "outputB.txt":
        print("Cannot post-process txt files outside of the assignment. Please try again\n")
        firstArg = input("Enter new file name: ")

    print("Graphing " + str(firstArg) + "...\n")

    # Bar plot for outpuA and outputB txt files, otherwise try again
    if str(firstArg) == "outputA.txt":
        G = hashtag_list(firstArg)
        hashtags = G[0]
        occurances = G[1]


        listObjects = []
        performance = []

        for i in range(len(hashtags)):
            hashtag = hashtags[i]
            occur = occurances[i]
            listObjects.append(hashtag)
            performance.append(occur)

        objects = tuple(listObjects)
        y_pos = np.arange(len(objects))

        fig, ax = plt.subplots()
        # plot the graph with hastags and values
        plt.bar(y_pos, performance, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.xlabel('Hashtags')
        plt.ylabel('Occurrances')
        plt.title('Occurrances of Similar Hashtags')
        fig.autofmt_xdate()

        plt.savefig('outputA.png')

    elif str(firstArg) == "outputB.txt":
        td = sentiment_list(firstArg)[0]
        vals = sentiment_list(firstArg)[1]
        cats = sentiment_list(firstArg)[2]

        # Plot graph      
        objects = tuple(td)
        y_pos = np.arange(len(objects))

        fig, ax = plt.subplots()
        # set interval in between
        ax = plt.axes()
        ax.xaxis.set_major_locator(ticker.MultipleLocator(len(objects)//10))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))

        plt.plot(td, vals[0])
        plt.plot(td, vals[1])
        plt.plot(td, vals[2])
        plt.plot(td, vals[3])
        plt.plot(td, vals[4])

        plt.xlabel('Times')
        plt.ylabel('Sentiment Value')
        plt.title('Sentiments of Tweets per Time')
        fig.autofmt_xdate()

        plt.legend([cats[0], cats[1], cats[2], cats[3], cats[4]], loc='upper left')        

        plt.savefig('outputB.png')



if __name__ == "__main__": main()




