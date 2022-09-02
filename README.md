# 4g-database
This is a 4-glider collision database generated using a modified version of popseq. Around 7.7 million collisions were collected, of which 1901590 of them stabilize into usable apgcodes and without escaping spaceships. As a limitation on popseq, the database only consists of two-directional 90-degree glider collisions. However, this ensures that clearance is being maximized, especially for certain conditions where syntheses become invalid when a glider of another direction is being introduced.

Since it has more than ten times more entries than the old 4-glider database (https://github.com/dvgrn/glider-collisions/tree/main/four-glider-collisions ), it is recommended that both databases are downloaded, and that the old one is used to supplement the new one in case the new one doesn't return any results. Note that the old 4-glider database has 464745 3-glider entries apart from the 131431 4-glider entries, and that it doesn't have the directional limitations that popseq has.

There are even more entries on popseq than the ones collected in the database, as there are 20386397 collisions on it. The result-generation script was terminated after around two minutes of constantly outputting results. If you want to search for population matches in active regions (like that in synthesise-patt.py), use popseq to achieve this purpose.

The original version of popseq can be found here: 
https://conwaylife.com/forums/viewtopic.php?p=43319#p43319

The result-generation script can be found on this repository:
https://github.com/carson-cheng/4g-database/blob/main/popseq.c

The result-generation script can be compiled by running:

```g++ -O3 popseq.c -o popseq```

If you compile and run this script, it prints out results instead of saving them into a file. Therefore, it is recommended that the script is run like this:

```./popseq > 4g_database.txt```
