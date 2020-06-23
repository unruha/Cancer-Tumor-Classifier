# Cancer Identifier

attributeList = []
attributeList.append("ID")
attributeList.append("radius")
attributeList.append("texture")
attributeList.append("perimeter")
attributeList.append("area")
attributeList.append("smoothness")
attributeList.append("compactness")
attributeList.append("concavity")
attributeList.append("concave")
attributeList.append("symmetry")
attributeList.append("fractal")
attributeList.append("class")



###############################################################################
def makeTrainingSet(filename):

# str -> list
# PRE:  filename is the name of a file with with training data 
# POST: a list of patient records is returned. Each patient record is a
#       dictionary which has 12 keys from attributeList 
#
    trainingSet = []
    # Read in file
    for line in open(filename,'r'):
        if '#' in line:
            continue
        line = line.strip('\n')
        linelist = line.split(',')
        # Create a dictionary for the line
        # (assigns each attribute of the record 
        #  to an element of the dictionary, using the keys in attributeList)
        record = {}
        for i in range(len(attributeList)):
              if(i==11): #11th item is class label (M or B) not a float
                  record[attributeList[i]] = linelist[31].strip() 
              else:
                  record[attributeList[i]] = float(linelist[i])
        # Add the dictionary to a list
        trainingSet.append(record)        

    return trainingSet



###############################################################################
def makeTestSet(filename):

#str -> list
#PRE:  filename is the name of a file with testing data.
#POST: a list of dictionaries is returned.  Each dictionary has the 12 keys 
#      from attributeList PLUS an additional key representing the prediction 
#      you will make.  Note each prediction is initialized to "none"

    testset = makeTrainingSet(filename)

    for record in testset:
        record["prediction"] = "none"

    return testset



###############################################################################
def trainClassifier(trainingSet):
#list -> dict
#PRE:  trainingSet is a list of dictionaries.  Each item in the list is one 
#      patient record stored as a dictionary with keys from attributeList.
#POST: a dictionary is returned.  This dictionary has 10 keys (all the 
#      keys from attributeList EXCEPT "ID" and "class").  The values of these 10
#      keys represent the midpoints between the average of each attribute's 
#      values for benign and malignant tumors
    


    averagesDict = {}
    malignantDict = {}
    benignDict = {}

    for attribute in attributeList[1:11]:
        averagesDict[attribute] = 0
        malignantDict[attribute] = 0
        benignDict[attribute] = 0
        
    benign_patients = 0
    malignant_patients = 0
    
    for patient in trainingSet:
        if patient["class"] == "B":
            for attribute in attributeList[1:11]:
                benignDict[attribute] += patient[attribute]
            benign_patients += 1
        elif patient["class"] == "M":
            for attribute in attributeList[1:11]:
                malignantDict[attribute] += patient[attribute]
            malignant_patients += 1
   
    for key in benignDict.keys():
        benignDict[key] = benignDict[key] / benign_patients
        
    for key in malignantDict.keys():
        malignantDict[key] = malignantDict[key] / malignant_patients
        
    for key in averagesDict.keys():
        averagesDict[key] = (malignantDict[key] + benignDict[key]) / 2
        
    return averagesDict
   



###############################################################################
def classifyTestRecords(testSet, classifier):
# list, dict -> void
# PRE:  testSet is a list of patient records where each record is a dictionary. 
#       The keys of the dictionary are the same as in attributeList.
#       classifier is a dictionary of the threshold values for each attribute
#POST:  testSet["prediction"] is filled in for each patient record in testSet.
#       Specifically, testSet["prediction"] is filled in with "malignant" if 
#       5 or more attributes were above the threshold, otherwise it is filled 
#       in with "benign".
    


    for patient in testSet:
        malignant_features = 0
        for attribute in attributeList[1:11]:
            if patient[attribute] > classifier[attribute]:
                malignant_features += 1
        if malignant_features >= 5:
            patient["prediction"] = "M"
        else:
            patient["prediction"] = "B"
    


###############################################################################
def reportAccuracy(testSet):
# list -> void
# PRE:  list is a list of patient records in testSet.  Each record is a 
#       dictionary with 13 keys (the 12 keys from attributeList plus the 
#       prediction key). 
#POST:  the function prints out the accuracy of the predictions made overall.
#       It reports overall accuracy (# correct predictions / # predictions).
   

    correct_predictions = 0
    num_predictions = 0
    
    for patient in testSet:
        if patient["class"] == patient["prediction"]:
            correct_predictions += 1
        num_predictions += 1
    
    accuracy = correct_predictions / num_predictions
    print("The accuracy of the classifier is " + str(accuracy * 100) + " percent")
    
    
        
    




###############################################################################
# MAIN PROGRAM

print ("Reading in training data...")
trainingSet = []
trainingFile = "cancerTrainingData.txt"
trainingSet = makeTrainingSet(trainingFile)
print ("Done reading training data.\n")

print ("Training classifier..."    )
classifier = trainClassifier(trainingSet)
print (classifier)
print ("Done training classifier.\n")

# if the classifier you just printed is the exact same as the one hw4.pdf
# then carry on and uncomment the next four lines of code to create the
# testSet.  The makeTestSet() function is already written for you. 

print ("Reading in test data...")
testFile = "cancerTestingData.txt"
testSet = makeTestSet(testFile)
print ("Done reading test data.\n")


print ("Making predictions and reporting accuracy...")
classifyTestRecords(testSet, classifier)
reportAccuracy(testSet)
print ("Done.\n")
