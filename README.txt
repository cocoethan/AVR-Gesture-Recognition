AVRGlove-Gesture Recognition v0.1
Contributors: Ethan Coco, Maxwell Twardowski

Description: 
AVRGlove-Gesture Recognition is an American Sign Language (ASL) gesture recognition software that reads input from custom data-gloves.

Notes:
The current release (v0.1) only supports 16 distinct static sign language letters (a,b,c,d,e,f,g,h,i,k,l,o,s,w,x,y) with ~96 percent training accuracy, and ~92 percent testing accuracy. If re-training the model used in the current release with the alternative 'categories' list located in 'train_model.py', 24 static sign language letters (all ASL letters except j, z), are supported with ~82 percent training accuracy, and ~75 percent testing accuracy. Future releases will focus on improving this accuracy.

This software works in conjunction with a custom data-glove. This custom data-glove can be replicated using an ESP32 and five flex-sensors across each finger. In the current release (v0.1), the data-glove needs to be connected through a USB port and the corresponding COMM port needs to be specified in 'main.py'. 

Navigation:
src : Source folder.
      -> input_data.py : Python file to manually create data for dataset gestures using a data-glove. (Optional Run)
      -> main.py : Python file to run main functions of the software; loads model, displays GUI, predicts, displays output. (Required Run)
      -> mind_flayer.h5 : h5 file containing pre-trained learning model. (Required)
      -> normalize_data.py : Python file to manually normalize data for datasets. (Optional Run)
      -> train_model.py : Python file to manually train the learning model. (Optional Run)
avr_dataset.zip : Zipped folder for our custom dataset containing 5 files of 1500 lines of data-glove data for each of the 24 ASL static letters.
      -> AVRDataset : Dataset folder.
            -> asl
                  -> testing_set_normalized : Folder for min-max normalized data to be used as a test set.
                  -> testing_set_raw : Folder for raw data to be used as a test set.
                  -> training_set_normalized : Folder for min-max normalized data to be used as a training set.
                  -> training_set_raw : Folder for raw data to be used as a training set.

Instructions:
1. Place 'src' folder in current directory if not already. (Optional: If using train_model.py or normalize_data.py; unzip and place AVRDataset in current directory.)
2. Change current directory to src folder.
3. Connect data-glove via USB and find it's correlating COMM port (You can use device manager to find this if using Windows).
4. Open main.py and change the variables 'comPort' and 'baud' to match your current data-glove's specifications. 
(Optional: 
If using train_model.py, change the variables 'dataset_dir' and 'testing_dataset_dir' to the directory the 'training_set_normalized' and 'testing_set_normalized' are currently in.
If using normalize_data.py, change the variable 'dataset_dir' to the directory the dataset files you want to normalize are in.
If using input_data.py, change the variables 'espData' to match your current data-glove's specifications.
)
5. Compile and run each file you want to run. (Note: If you only want the software running, only compile and run main.py.)
      Ex.
