import csv, sys, math, random, operator, copy
import nltk, split

train_nodes = []

def get_all_words(train_nodes):
    w = set()
    for n in train_nodes:
        (phrase_id, sentence_id, phrase, label) = n
        w.update(split.tokenize(phrase))
    return w

def get_features(all_words, train_nodes):
    f = []
    phrase_features = {word: 0 for word in all_words}
    for node in train_nodes:
        (phrase_id, sentence_id, phrase, label) = node
        phrase_words = split.tokenize(phrase)
        for word in phrase_words: 
            phrase_features[word] = 1  

        f.append((copy.deepcopy(phrase_features), label))

        # reset dict
        for word in phrase_words: 
            phrase_features[word] = 0
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
    all_words = get_all_words(train_nodes)
    train_set = get_features(all_words, train_nodes)
    print(train_set[0])
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    prediction = classifier.classify({word:1 for word in split.tokenize(', inane images keep popping past your head')})
    print(prediction)

