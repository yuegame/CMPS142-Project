#Ruihong Yu
#Edmund Yu
#Rohit Falor
#KNN implementation
import csv
import sys
import math
import random
import operator
from multiprocessing import Pool
from multiprocessing import Process, Queue
from itertools import product

num_neighbors = 9
results={}
    
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

# Multiprocessed KNN

def multi_knn(test_nodes, train_nodes, start, end, queue):
    for test_index in range(start, end):
        neighbors = euclidean_calculation(test_nodes[test_index], train_nodes)

        distribution = {}
        for i in range(num_neighbors):
            if int(neighbors[i][2]) not in distribution:
                distribution[int(neighbors[i][2])] = 1
            else:
                distribution[int(neighbors[i][2])] = distribution[int(neighbors[i][2])] + 1
                
        prediction = max(distribution.items(), key=operator.itemgetter(1))[0]

        # Appended prediction of each neighbor into queue
        queue.put((test_nodes[test_index][0],test_nodes[test_index][1],test_nodes[test_index][2],str(prediction)))

    

def main():

    phrase_id = -1
    if(len(sys.argv) > 2):
        print("Usage: python analyze.py phraseID")
        print("Usage: python analyze.py")
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

    # Parses testset_1 in the same way as train.csv
    with open('testset_1.csv') as test_file:
        test_reader = csv.reader(test_file, delimiter = ',')

        test_header_parsed = False
        for row in test_reader:
            if not test_header_parsed:
                test_header_parsed = True
            else:
                test_nodes.append(row)


    print("Length of training nodes is: ", len(train_nodes))
    print("Length of test nodes is: ", len(test_nodes))

    # Used in debugging purposes to find the prediction for a specific phraseID
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

    # Used in training data testing
    #correct_predictions = 0
    #incorrect_predictions = 0

    results=[]
    queue = Queue()
    pool = []

    # Sets up processes for multiprocessing
    process_count = 25
    increment = int(len(test_nodes)/process_count)
    
    # Multiprocessing done here
    for i in range(process_count):
        pool.append(Process(target=multi_knn, args=(test_nodes,train_nodes,increment*i, increment*(i+1),queue)))
        pool[i].start()
        if(i+1 == process_count):
            pool.append(Process(target=multi_knn, args=(test_nodes, train_nodes, 1+(increment*process_count), len(test_nodes), queue)))
            pool[i+1].start()

    completion = 0

    # Gives realtime updates for results
    while(len(results) < len(test_nodes)):

        try:
            data = queue.get(timeout = 10)
        except:
            break
        if(((float(len(results))/len(test_nodes))*100) - completion > .1):
            completion = (float(len(results))/len(test_nodes))*100
            print(str(completion)[:4]+"% done")
        results.append((data[0], data[1], data[2], data[3]))
        print(-len(results)+len(test_nodes))

    #print(results)

    # Finish processes
    for i in range(len(pool)):
        pool[i].join()

    # Writes results to CSV file
    print("Writing results...")
    file = open("results.csv", "w")
    for i in range(len(results)):
        file.write(str(results[i][0])+","+str(results[i][3])+"\n")
    file.close()
    print("Done!")

    # Only reached if debugging
    if(int(phrase_id) >=0 ):
        print("PhraseID not found!")
    else:
        pass
    return
        
                    
     
if __name__ == "__main__":
    main()
