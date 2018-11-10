#Ruihong Yu
#Edmund Yu
#Rohit Falor
#Analyzer for train.csv
import csv
import sys
import math

def main():

    if(len(sys.argv) != 2):
        print("Usage: python analyze.py phraseID")
        return
    else:
        phrase_id = sys.argv[1]
    
    with open('train.csv') as train_file:
        train_reader = csv.reader(train_file, delimiter=',')
        train_nodes = []

        #Parses train.csv in (PhraseId, SentenceId, Sentence, Sentiment) tuples
        train_header_parsed = False
        for row in train_reader:
            if not train_header_parsed:
                train_header_parsed = True
            else:
                train_nodes.append(row)
    
    for index in range(0, len(train_nodes)):
        if(train_nodes[index][0] == phrase_id):
            print(train_nodes[index])
            return

    print("PhraseID not found!")
    return
        
                    
     
if __name__ == "__main__":
    main()
