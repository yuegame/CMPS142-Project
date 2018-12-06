import csv

train_nodes = []
with open('train.csv') as train_file:
        train_reader = csv.reader(train_file, delimiter=',')

        #Parses train.csv in (PhraseId, SentenceId, Sentence, Sentiment) tuples
        train_header_parsed = False
        for row in train_reader:
            if not train_header_parsed:
                train_header_parsed = True
            else:
                train_nodes.append(row)

        
file = open("train.txt", "w")
for node in train_nodes[:80000]:
    file.write(node[2] + " __label__" + node[3])
    file.write("\n")
    