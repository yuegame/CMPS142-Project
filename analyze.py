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
from multiprocessing import Process

num_neighbors = 9
results={}
# L1 calculations
def set_results(key, correct, incorrect):
    results[key] = (correct, incorrect)
    
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
def multi_knn(test_nodes, train_nodes, start, end):
    correct_predictions = 0
    incorrect_predictions = 0
    print()
    for test_index in range(start, end):
        print("Index: ",test_index)
    
        neighbors = euclidean_calculation(test_nodes[test_index], train_nodes)

        distribution = {}
        for i in range(num_neighbors):
            if int(neighbors[i][2]) not in distribution:
                distribution[int(neighbors[i][2])] = 1
            else:
                distribution[int(neighbors[i][2])] = distribution[int(neighbors[i][2])] + 1
                
        prediction = max(distribution.items(), key=operator.itemgetter(1))[0]
        print("prediction", prediction)
        print("index", test_nodes[test_index][3])
        if int(prediction) == int(test_nodes[test_index][3]):
            correct_predictions += 1
        else:
            incorrect_predictions += 1

        print (correct_predictions, incorrect_predictions)

    set_results(start, correct_predictions, incorrect_predictions)
    #results[start] = (correct_predictions, incorrect_predictions)
    print(results)
    

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
    
    for index in range(0, 2500):
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

    # pool = Pool(processes=10)
    # answer = [pool.apply_async(multi_knn, args=(test_nodes,train_nodes,2500*x,2500*(x+1),results)) for x in range(10)]
    # output = [p.get() for p in answer]
    
    # for i in range(500):
    #     x = Process(target=multi_knn, args=(test_nodes,train_nodes,50*i, 50*(i+1),results))
    #     x.start()

    p0 = Process(target=multi_knn, args=(test_nodes, train_nodes,0,250))
    p1 = Process(target=multi_knn, args=(test_nodes, train_nodes,250,500))
    p2 = Process(target=multi_knn, args=(test_nodes, train_nodes,500,750))
    p3 = Process(target=multi_knn, args=(test_nodes, train_nodes,750,1000))
    p4 = Process(target=multi_knn, args=(test_nodes, train_nodes,1000,1250))
    p5 = Process(target=multi_knn, args=(test_nodes, train_nodes,1250,1500))
    p6 = Process(target=multi_knn, args=(test_nodes, train_nodes,1500,1750))
    p7 = Process(target=multi_knn, args=(test_nodes, train_nodes,1750,2000))
    p8 = Process(target=multi_knn, args=(test_nodes, train_nodes,2000,2250))
    p9 = Process(target=multi_knn, args=(test_nodes, train_nodes,2250,2500))

    p0.start()
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    p7.start()
    p8.start()
    p9.start()

    p0.join()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()
    p7.join()
    p8.join()
    p9.join()

    print(results)
    for k in results.keys():
        correct_predictions += results[k][0]
        incorrect_predictions += results[k][1]

    print("CP", correct_predictions)
    print("IP", incorrect_predictions)
    accuracy = correct_predictions / (correct_predictions + incorrect_predictions)
    
    if(int(phrase_id) >=0 ):
        print("PhraseID not found!")
    else:
        print("We have", correct_predictions,"correct predictions and",incorrect_predictions,
              "incorrect predictions for an accuracy of",accuracy)
    return
        
                    
     
if __name__ == "__main__":
    main()
