import csv, sys, math, random, operator
import split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

train_nodes = []
test_nodes = []

def get_features(train_set, test_set):
    vectorizer = CountVectorizer()
    train = vectorizer.fit_transform([n[2] for n in train_set])
    test = vectorizer.transform([n[2] for n in test_set])
    return (train, test)
    
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

    with open('testset_1.csv') as test_file:
        test_reader = csv.reader(test_file, delimiter=',')

        #Parses train.csv in (PhraseId, SentenceId, Sentence, Sentiment) tuples
        test_header_parsed = False
        for row in test_reader:
            if not test_header_parsed:
                test_header_parsed = True
            else:
                test_nodes.append(row)

    train_features, test_features = get_features(train_nodes, test_nodes)
    nb = MultinomialNB()
    nb.fit(train_features, [int(n[3]) for n in train_nodes])
    predictions = nb.predict(test_features)
    
    flags = []
    for row in test_nodes:
        phrase = row[2]
        flags.append(0 if len(phrase) < 46 else 1)

    file = open("bayes_results.csv", "w")
    for i in range(len(predictions)):
        result = map(str, [test_nodes[i][0], predictions[i], '"' + test_nodes[i][2] + '"', flags[i]])
        write_line = ", ".join(result) + "\n"
        print(write_line)
        file.write(write_line)
    file.close()
