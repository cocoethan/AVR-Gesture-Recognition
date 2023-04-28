import os
import pandas as pd

dataset_dir = 'C:/Users/ethan/Desktop/test/' #Change to local dataset
categories = ['a','b','c','d','e','f','g','h','i','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y']

training_data = []

thumb_max = 1300 #1019.0
index_max = 1458.0
middle_max = 1798 #1712.0
ring_max = 2971.0
pinky_max = 1191.0

max_ring = []

for category in categories:
    path = os.path.join(dataset_dir, category) #Path to categories
    category_num = categories.index(category)
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        file_name = category + ".csv"
        #print(file_name)
        data = pd.read_csv(file_path)
        data = data.values

        data[:, 1] = ((data[:, 1]) / thumb_max)
        data[:, 2] = ((data[:, 2]) / index_max)
        data[:, 3] = ((data[:, 3]) / middle_max)
        data[:, 4] = ((data[:, 4]) / ring_max)
        data[:, 5] = ((data[:, 5]) / pinky_max)

        #max_ring.append(max(data[:, 1]))

        training_data.append([data[:, 1:6], category_num])

        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)

print(training_data)
#print("Here:",max(max_ring))