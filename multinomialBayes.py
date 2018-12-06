import csv, sys, math, random, operator
import split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn import metrics
from nltk import word_tokenize
from nltk.stem import PorterStemmer

train_nodes = []

def get_features(train_set, test_set):
    phrases = [n[2] for n in train_set]
    tokenized = [word_tokenize(phrase) for phrase in phrases]  
    stemmer = PorterStemmer()
    
    for i in range(len(tokenized)):
        tokenized[i]= " ".join([stemmer.stem(token) for token in tokenized[i]])
    
    print(tokenized)
    vectorizer = CountVectorizer(tokenizer=split.tokenize)
    train = vectorizer.fit_transform(tokenized)
    # transformer = TfidfTransformer().fit(train)
    # train = transformer.transform(train)  

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

    train_set, test_set = train_nodes[:80000], train_nodes[80000:]
    train_features, test_features = get_features(train_set, test_set)
    nb = MultinomialNB()
    nb.fit(train_features, [int(n[3]) for n in train_set])
    
    predictions = nb.predict(test_features)
    print(predictions)

    # Compute the error.  It is slightly different from our model because the internals of this process work differently from our implementation.
    comparison = zip([int(n[3]) for n in test_set], predictions)
    
    correct, incorrect = 0, 0
    for pair in comparison:
        if (pair[0] == pair[1]):
            correct += 1
        else:
            incorrect += 1
    
    accuracy = correct / (correct + incorrect)
    print(accuracy)
