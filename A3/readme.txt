This is a readme file to explain how to run each file. Each file follows the docker instructions and opens two docker containers. All twitter and spark files must be in the same directory.

To run:

1. Run in the twitter container: python twitter_appA.py
2. Run in the other container: spark-submit spark_appA.py. Output will be saved to a text file in the titled outputA.txt. Keep this file in its remote directory.


To generate graphs:

Go to the docker container where spark_app ran.
>>> python post-processing outputA.txt
and the graph is saved in outputA.png

