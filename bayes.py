import csv, sys, math, random, operator
import split

train_nodes = []

def get_features(train_nodes):
    f = {}

    for node in train_nodes:
        phrase, label = node[-2], node[-1]
        words = split.tokenize(phrase)

        for word in words:
            f[word] = label
    
    return f

    
if __name__ == "__main__":
    with open('train.csv') as train_file:
        train_reader = csv.reader(train_file, delimiter=',')

        #Parses train.csv in (PhraseId, SentenceId, Sentence, Sentiment) tuples
        train_header_parsed = False
        for row in train_reader:
            if not train_header_parsed:
                train_header_parsed = True
            else:
                train_nodes.append(row)

    print(train_nodes[:5])
    train_set = get_features(train_nodes)
    print(train_set[0])


