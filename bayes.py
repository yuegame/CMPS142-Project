import csv, sys, math, random, operator
import nltk, split

train_nodes = []

def get_features(train_nodes):
    f = []

    for node in train_nodes:
        (phrase_id, sentence_id, phrase, label) = node
        words = split.tokenize(phrase)
        phrase_features = ({word: 1 for word in words}, label)
        f.append(phrase_features)

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

    train_set = get_features(train_nodes)
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    prediction = classifier.classify({word:1 for word in split.tokenize('good')})
    print(prediction)

