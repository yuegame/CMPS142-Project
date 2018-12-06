import sys
import csv

if __name__ == '__main__':

    knn_results = []

    with open('knn_results.csv') as knn_file:
        knn_reader = csv.reader(knn_file, delimiter = ',')

        for row in knn_reader:
            knn_results.append(row)

    bayes_results = []

    with open('bayes.csv') as bayes_file:
        bayes_reader = csv.reader(bayes_file, delimiter = ',')
        for row in bayes_reader:
            bayes_results.append(row)
    changed = 0
    supposedly_incorrect = 0
    disagree = 0
    for index in range(len(knn_results)):
        bayes_instance = bayes_results[index]
        knn_instance = knn_results[index]
        
        if(bayes_instance[1] != knn_instance[1]):
            disagree += 1
            if(bayes_instance[3] == str(0)):
                knn_results[index][1] = bayes_results[index][1]
                changed += 1
            
        if(bayes_instance[3] == str(1)):
            supposedly_incorrect += 1

    test = []

    with open('testset_1.csv') as test_file:
        test_reader = csv.reader(test_file, delimiter = ',')
        
        header = False
        for row in test_reader:
            if not header:
                header = True
            else:
                test.append(row)

    print(test[0])

    counter = 0
    for test_index in range(len(test)):
        #print(test_index)
        for knn_index in range(len(knn_results)):
            if(str(knn_results[knn_index][0]) == str(test[test_index][0])):
                counter +=1
                print(counter)
                knn_results[knn_index], knn_results[test_index] = knn_results[test_index], knn_results[knn_index]

    file = open("predictions.csv", "w")
    file.write("PhraseID,Sentiment\n")
    for index in range(len(knn_results)):
        file.write(knn_results[index][0]+","+knn_results[index][1]+"\n")

    file.close()
    print(str(changed)+" sentiments changed!")
    print(str(supposedly_incorrect)+" instances are supposedly incorrect in Bayes!")
    print(str(disagree)+" instances are different between Bayes and KNN!")
    
