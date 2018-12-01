#Ruihong Yu
#Edmund Yu
#Rohit Falor
#Analyzer for train.csv
import csv
import sys
import math

num_neighbors = 5

# L1 calculations
def euclidean_calculation(test_row, train_nodes):
    node_distances = []
    
    for node in train_nodes:
        dist_sum = 0
        
        for index in range(0, len(test_row)-2):
            dist_sum = dist_sum + (int(test_row[index])-int(node[index]))**2
                                   
        distance = math.sqrt(dist_sum)
        node_distances.append((node, distance, node[3]))

    output_list = sorted(node_distances, key=lambda tup:tup[1])
    return output_list

def main():

    if(len(sys.argv) != 2):
        print("Usage: python analyze.py phraseID")
        return
    else:
        phrase_id = sys.argv[1]
    
    with open('train.csv') as train_file:
        train_reader = csv.reader(train_file, delimiter=',')
        train_nodes = []

        #Parses train.csv in (PhraseId, SentenceId, Sentence, Sentiment) tuples
        train_header_parsed = False
        for row in train_reader:
            if not train_header_parsed:
                train_header_parsed = True
            else:
                train_nodes.append(row)
    
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

    print("PhraseID not found!")
    return
        
                    
     
if __name__ == "__main__":
    main()
