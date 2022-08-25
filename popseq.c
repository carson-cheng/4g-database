//Unlike the canonical version of popseq.c, this version prints out all RLEs it generates without accepting an input pattern.
//The original version of popseq.c can be found as a zip file at https://conwaylife.com/forums/viewtopic.php?p=43319#p43319
//It was run for slightly more than 2 minutes to generate the RLEs needed for the database. If it is run to completion, the database will be much larger.

//Compile this file with "g++ -O3 popseq.c -o popseq"
//Run this file with "./popseq > filename.txt" to pipe the printed RLEs to a file, where you can modify the filename based on your favors.
//Note that the quotation marks only signal the location of the commands above, and should not be included when running the command.

#include "LifeAPI.h"
#include <cstring>

int main(int argc, char *argv[]) {

    int pops[16], allpops[256];
    char s[1024], line[1024];
    s[0] = 0;

    /*while (fgets(line, 1024, stdin) != NULL) {
        line[strcspn(line, "\r\n")] = 0;
        if (!strstr(line, "="))
            strcat(s, line);
        if (strstr(line, "!"))
            break;
    }
    
    fprintf(stderr, "Accepted pattern: %s\n", s);*/

    New();

    LifeState *find = NewState(s);

    for (int i = 0; i < 16; i++) {
        pops[i] = GetPop(find);
        Evolve(find, find, 1);
    }

    LifeState *after = NewState();
    LifeState *after4 = NewState();
    LifeState *before = NewState();
    LifeState *g_ne = NewState("3o$2bo$bo!");
    LifeState *g_se = NewState("bo$2bo$3o!");
    LifeState *g_nw = NewState("3o$o$bo!");
    LifeState *g_sw = NewState("bo$o$3o!");

    LifeState *g1 = NewState();
    Copy(g1, g_ne);
    Move(g1, -5, 5);
    LifeIterator *g2 = NewIterator(g_ne, -15, 5, 14, 14, 4);
    LifeIterator *g3 = NewIterator(g_nw, 4, 5, 2, 1, 19);
    LifeIterator *g4 = NewIterator(g_nw, 4, 5, 14, 14, 4);
    int n = 0;
    do {
        
        Copy(before, g1);
        PutState(before, g2);

        Evolve(after, before, 4);

        if (GetPop(after) != 10)
            continue;

        do {
            do {

                Copy(before, g1);
                PutState(before, g2);
                PutState(before, g3);
                PutState(before, g4);
                PrintRLE(before);
                Evolve(after, before, 4);
                if (GetPop(after) != 20)
                    continue;
                for (int gen = 0; gen < 200; gen++) {

                    allpops[gen] = GetPop(after);
                    
                    if (gen < 15)
                        continue;

                    int match = 1;
                    for (int j = 0; j < 16; j++) {
                        if (allpops[gen - 15 + j] != pops[j]) {
                            match = 0;
                            break;
                        }
                    }
                    
                    if (match) {
                        PrintRLE(before);
                        fflush(stdout);
                        break;
                    }

                    Evolve(after, after, 1);
                }
                
            } while(Next(g4));

        } while(Next(g3));
        
    } while(Next(g2));

    return 0;
}
