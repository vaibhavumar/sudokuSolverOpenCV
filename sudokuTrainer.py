import numpy as np
from sklearn.svm import LinearSVC
import os
import cv2
import joblib

# Generate training set
TRAIN_PATH = "SudokuDataset\Train"
list_folder = os.listdir(TRAIN_PATH)
trainset = []
train_label = []
for folder in list_folder:
    flist = os.listdir(os.path.join(TRAIN_PATH, folder))
    for f in flist:
        im = cv2.imread(os.path.join(TRAIN_PATH, folder, f))
        im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY )
        im = cv2.resize(im, (36,36))
        trainset.append(im)
        train_label.append(int(folder))

# Generate testing set
TEST_PATH = "SudokuDataset\Test"
list_folder = os.listdir(TEST_PATH)
testset = []
test_label = []
for folder in list_folder:
    flist = os.listdir(os.path.join(TEST_PATH, folder))
    for f in flist:
        im = cv2.imread(os.path.join(TEST_PATH, folder, f))
        im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY )
        im = cv2.resize(im, (36,36))
        testset.append(im)
        test_label.append(int(folder))
trainset = np.reshape(trainset, (len(trainset), -1))

# Create an linear SVM object
clf = LinearSVC()

# Perform the training
clf.fit(trainset, train_label)
print("Training finished successfully")

# Testing
testset = np.reshape(testset, (len(testset), -1))
y = clf.predict(testset)
print("Testing accuracy: " + str(clf.score(testset, test_label)))

joblib.dump(clf, "classifier.pkl", compress=3)