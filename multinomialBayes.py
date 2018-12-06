import csv, sys, math, random, operator
import split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

train_nodes = []

def get_features(train_set, test_set):
    vectorizer = CountVectorizer(tokenizer=split.tokenize)
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

    train_set = []
    for index in range(0, 85000):
        train_set.append(train_nodes.pop(random.randint(0,len(train_nodes)-1)))
    test_set = train_nodes
    train_features, test_features = get_features(train_set, test_set)
    nb = MultinomialNB()
    nb.fit(train_features, [int(n[3]) for n in train_set])
    
    predictions = nb.predict(test_features)
    print(predictions)

    # Compute the error.  It is slightly different from our model because the internals of this process work differently from our implementation.
    comparison = list(zip([int(n[3]) for n in test_set], predictions))
    
    # file = open("bayes_results.csv", "w")


    # correct, incorrect = 0, 0
    # len_correct, len_incorrect = 0, 0
    # for i in range(len(comparison)):
    #     if (comparison[i][0] == comparison[i][1]):
    #         correct += 1
    #         len_correct += len(test_set[i][2])
    #         print(test_set[i][2])
    #     else:
    #         print("\t" + test_set[i][2])
    #         len_incorrect += len(test_set[i][2])
    #         incorrect += 1
    
    # accuracy = correct / (correct + incorrect)
    print(accuracy)
