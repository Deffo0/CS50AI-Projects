# Construction
+ load the data from the folders as images in 2d array with fixed size and labels indicate the number og the traffic sign.
+ construct the model which consists of conv layer with 64 filter and 3 x 3 size, 2 x 2 pooling layer, 1024 units for the hidden layer with 20% drop out to avoid overfitting, and the output layer consists of 43 units for the categories.
# Experiments
+ starting with 512 units for the hidden layer with 0.5 drop out:
    - this make the accuracy of the model is 95%.
+ increasing the number of units will improve the accuracy but we must consider the overfitting, so we make the drop out 0.2:
    - by this way the accuracy reached to 96.6%.