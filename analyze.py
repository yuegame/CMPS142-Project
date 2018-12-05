#Ruihong Yu
#Edmund Yu
#Rohit Falor
#Analyzer for train.csv
import csv
import sys
import math
import random
import operator
from multiprocessing import Pool
from multiprocessing import Process, Queue
from itertools import product

num_neighbors = 9

# L1 calculations
def euclidean_calculation(test_row, train_nodes):
    node_distances = []
    
    for node in train_nodes:
        dist_sum = 0
        
        dist_sum = dist_sum + (int(test_row[0])-int(node[0]))**2
        dist_sum = dist_sum + 50*((int(test_row[1])-int(node[1]))**2)
                
                                   
        distance = math.sqrt(dist_sum)
        node_distances.append((node, distance, node[3]))

    output_list = sorted(node_distances, key=lambda tup:tup[1])
    return output_list

# Multiprocess KNN
def multi_knn(test_nodes, train_nodes, start, end, queue):
    correct_predictions = 0
    incorrect_predictions = 0
    for test_index in range(start, end):
        if(test_index % 50 == 0 and start == 0):
            percentage = (float(test_index)/(end - start))*100
            print(percentage,"% done")
        neighbors = euclidean_calculation(test_nodes[test_index], train_nodes)

        distribution = {}
        for i in range(num_neighbors):
            if int(neighbors[i][2]) not in distribution:
                distribution[int(neighbors[i][2])] = 1
            else:
                distribution[int(neighbors[i][2])] = distribution[int(neighbors[i][2])] + 1
                
        prediction = max(distribution.items(), key=operator.itemgetter(1))[0]
        if int(prediction) == int(test_nodes[test_index][3]):
            correct_predictions += 1
        else:
            incorrect_predictions += 1

    queue.put((correct_predictions, incorrect_predictions))
    

def main():

    phrase_id = -1
    if(len(sys.argv) > 2):
        print("Usage: python analyze.py phraseID")
        return
    elif (len(sys.argv) == 2):
        phrase_id = sys.argv[1]

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

    test_nodes=[]
    
    for index in range(0, 25000):
        test_nodes.append(train_nodes.pop(random.randint(0,len(train_nodes)-1)))

    print("Length of training nodes is: ", len(train_nodes))
    print("Length of test nodes is: ", len(test_nodes))

    if(int(phrase_id) >= 0):
        for index in range(0, len(train_nodes)):
            if(train_nodes[index][0] == phrase_id):
                neighbors = euclidean_calculation(train_nodes[index], train_nodes)
                print("The",num_neighbors,"closest neighbors are:")
                for i in range(num_neighbors):
                    print(neighbors[i])

                distribution = {}
                print("\nThe sentiment distribution between the", num_neighbors,"neighbors is:")
                for i in range(num_neighbors):
                    if int(neighbors[i][2]) not in distribution:
                        distribution[int(neighbors[i][2])] = 1
                    else:
                        distribution[int(neighbors[i][2])] = distribution[int(neighbors[i][2])] + 1 
                print(distribution)
                return

    correct_predictions = 0
    incorrect_predictions = 0
    results={}
    queue = Queue()
    pool = []

    process_count = 25
    increment = 25000/process_count
    
    # Multiprocessing done here
    for i in range(process_count):
        pool.append(Process(target=multi_knn, args=(test_nodes,train_nodes,increment*i, increment*(i+1),queue)))
        pool[i].start()

    # Finish processes and tally results for testing accuracy
    for i in range(process_count):
        data = queue.get()
        correct_predictions += data[0]
        incorrect_predictions += data[1]
        pool[i].join()

    accuracy = float(correct_predictions) / (correct_predictions + incorrect_predictions)
    
    if(int(phrase_id) >=0 ):
        print("PhraseID not found!")
    else:
        print("We have", correct_predictions,"correct predictions and",incorrect_predictions,
              "incorrect predictions for an accuracy of",accuracy)
    return
        
                    
     
if __name__ == "__main__":
    main()
