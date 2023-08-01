# -*- coding: utf-8 -*-
"""Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KWwKTuqqbRz6Avb-N3xdEmHKbhriNK7g
"""

import pandas
import numpy as np
import warnings
import itertools
import matplotlib.pyplot as plt
import seaborn


from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFE
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn import metrics as metrics
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier


warnings.filterwarnings("ignore")

train = pandas.read_csv("Train_data.csv")
test = pandas.read_csv("Test_data.csv")

print(train.head())

print("Training data has {} rows & {} columns".format(train.shape[0],train.shape[1]))

print(test.head())

print("Testing data has {} rows & {} columns".format(test.shape[0],test.shape[1]))

train.describe()

ratio = train['class'].value_counts()
labels = ratio.index[0], ratio.index[1]
sizes = [ratio.values[0], ratio.values[1]]

figure, axis = plt.subplots()
axis.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
axis.axis('equal')

plt.title("Normal vs Anomaly Ratio")
plt.show()

print(train['num_outbound_cmds'].value_counts())
print(test['num_outbound_cmds'].value_counts())

train.drop(['num_outbound_cmds'], axis=1, inplace=True)
test.drop(['num_outbound_cmds'], axis=1, inplace=True)

scaler = StandardScaler()

cols = train.select_dtypes(include=['float64','int64']).columns
sc_train = scaler.fit_transform(train.select_dtypes(include=['float64','int64']))
sc_test = scaler.fit_transform(test.select_dtypes(include=['float64','int64']))

sc_traindf = pandas.DataFrame(sc_train, columns = cols)
sc_testdf = pandas.DataFrame(sc_test, columns = cols)

encoder = LabelEncoder()

cattrain = train.select_dtypes(include=['object']).copy()
cattest = test.select_dtypes(include=['object']).copy()

traincat = cattrain.apply(encoder.fit_transform)
testcat = cattest.apply(encoder.fit_transform)

enctrain = traincat.drop(['class'], axis=1)
cat_Ytrain = traincat[['class']].copy()

train_x = pandas.concat([sc_traindf,enctrain],axis=1)
train_y = train['class']
train_x.shape

test_df = pandas.concat([sc_testdf,testcat],axis=1)
test_df.shape

rfc = RandomForestClassifier();

rfc.fit(train_x, train_y);

score = np.round(rfc.feature_importances_,3)
importances = pandas.DataFrame({'feature':train_x.columns,'importance':score})
importances = importances.sort_values('importance',ascending=False).set_index('feature')

plt.rcParams['figure.figsize'] = (16,4)
importances.plot.bar();

rfc = RandomForestClassifier()

rfe = RFE(rfc, n_features_to_select=10)
rfe = rfe.fit(train_x, train_y)

feature_map = [(i, v) for i, v in itertools.zip_longest(rfe.get_support(), train_x.columns)]
selected_features = [v for i, v in feature_map if i==True]

print(selected_features)

seaborn.heatmap(train_x[selected_features].corr(), annot = True, fmt='.1g')

X_train,X_test,Y_train,Y_test = train_test_split(train_x,train_y,train_size=0.60, random_state=2)

model = KNeighborsClassifier(n_jobs=-1)
model.fit(X_train, Y_train);

scores = cross_val_score(model, X_train, Y_train, cv=10)
accuracy = metrics.accuracy_score(Y_train, model.predict(X_train))
confusion_matrix = metrics.confusion_matrix(Y_train, model.predict(X_train))
classification = metrics.classification_report(Y_train, model.predict(X_train))

print ("Cross Validation Mean Score:" "\n", scores.mean())
print ("Model Accuracy:" "\n", accuracy)
print ("Confusion matrix:" "\n", confusion_matrix)
print ("Classification report:" "\n", classification)

accuracy_test = metrics.accuracy_score(Y_test, model.predict(X_test))
confusion_matrix = metrics.confusion_matrix(Y_test, model.predict(X_test))
classification = metrics.classification_report(Y_test, model.predict(X_test))

print ("Model Accuracy:" "\n", accuracy)
print ("Confusion matrix:" "\n", confusion_matrix)
print ("Classification report:" "\n", classification)

prediction = model.predict(test_df)
test['KNN_prediction'] = prediction
print(test.head())

prediction

ratio = test['KNN_prediction'].value_counts()
labels = ratio.index[0], ratio.index[1]
sizes = [ratio.values[0], ratio.values[1]]
ratio_knn = ratio

figure, axis = plt.subplots()
axis.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
axis.axis('equal')

plt.title("K-Nearest Neighbors Predictions on Test Data")
plt.show()

svm_model = SVC()

svm_model.fit(X_train, Y_train)

svm_scores = cross_val_score(svm_model, X_train, Y_train, cv=10)
svm_accuracy = metrics.accuracy_score(Y_train, svm_model.predict(X_train))
svm_confusion_matrix = metrics.confusion_matrix(Y_train, svm_model.predict(X_train))
svm_classification = metrics.classification_report(Y_train, svm_model.predict(X_train))

print("SVM - Cross Validation Mean Score:" "\n", svm_scores.mean())
print("SVM - Model Accuracy:" "\n", svm_accuracy)
print("SVM - Confusion matrix:" "\n", svm_confusion_matrix)
print("SVM - Classification report:" "\n", svm_classification)

svm_accuracy_test = metrics.accuracy_score(Y_test, svm_model.predict(X_test))
svm_confusion_matrix_test = metrics.confusion_matrix(Y_test, svm_model.predict(X_test))
svm_classification_test = metrics.classification_report(Y_test, svm_model.predict(X_test))

print("SVM - Model Accuracy (Test Set):" "\n", svm_accuracy_test)
print("SVM - Confusion matrix (Test Set):" "\n", svm_confusion_matrix_test)
print("SVM - Classification report (Test Set):" "\n", svm_classification_test)

svm_prediction = svm_model.predict(test_df)
test['svm_prediction'] = svm_prediction
print(test.head())

ratio_svm = test['svm_prediction'].value_counts()
labels_svm = ratio_svm.index[0], ratio_svm.index[1]
sizes_svm = [ratio_svm.values[0], ratio_svm.values[1]]

figure_svm, axis_svm = plt.subplots()
axis_svm.pie(sizes_svm, labels=labels_svm, autopct='%1.1f%%', startangle=90)
axis_svm.axis('equal')
plt.title("SVM Predictions on Test Data")
plt.show()

X_train, X_test, Y_train, Y_test = train_test_split(train_x, train_y, train_size=0.60, random_state=2)

nb_model = GaussianNB()
nb_model.fit(X_train, Y_train)

nb_scores = cross_val_score(nb_model, X_train, Y_train, cv=10)
nb_accuracy = metrics.accuracy_score(Y_train, nb_model.predict(X_train))
nb_confusion_matrix = metrics.confusion_matrix(Y_train, nb_model.predict(X_train))
nb_classification = metrics.classification_report(Y_train, nb_model.predict(X_train))

print("Naive Bayes - Cross Validation Mean Score:" "\n", nb_scores.mean())
print("Naive Bayes - Model Accuracy:" "\n", nb_accuracy)
print("Naive Bayes - Confusion matrix:" "\n", nb_confusion_matrix)
print("Naive Bayes - Classification report:" "\n", nb_classification)

nb_accuracy_test = metrics.accuracy_score(Y_test, nb_model.predict(X_test))
nb_confusion_matrix_test = metrics.confusion_matrix(Y_test, nb_model.predict(X_test))
nb_classification_test = metrics.classification_report(Y_test, nb_model.predict(X_test))

print("Naive Bayes - Model Accuracy (Test Set):" "\n", nb_accuracy_test)
print("Naive Bayes - Confusion matrix (Test Set):" "\n", nb_confusion_matrix_test)
print("Naive Bayes - Classification report (Test Set):" "\n", nb_classification_test)

nb_prediction = nb_model.predict(test_df)
test['nb_prediction'] = nb_prediction
print(test.head())

ratio_nb = test['nb_prediction'].value_counts()
labels_nb = ratio_nb.index[1], ratio_nb.index[0]
sizes_nb = [ratio_nb.values[1], ratio_nb.values[0]]

figure_nb, axis_nb = plt.subplots()
axis_nb.pie(sizes_nb, labels=labels_nb, autopct='%1.1f%%', startangle=90)
axis_nb.axis('equal')
plt.title("Naive Bayes Predictions on Test Data")
plt.show()

lr_model = LogisticRegression()
lr_model.fit(X_train, Y_train)

lr_scores = cross_val_score(lr_model, X_train, Y_train, cv=10)
lr_accuracy = metrics.accuracy_score(Y_train, lr_model.predict(X_train))
lr_confusion_matrix = metrics.confusion_matrix(Y_train, lr_model.predict(X_train))
lr_classification = metrics.classification_report(Y_train, lr_model.predict(X_train))

print("Logistic Regression - Cross Validation Mean Score:" "\n", lr_scores.mean())
print("Logistic Regression - Model Accuracy:" "\n", lr_accuracy)
print("Logistic Regression - Confusion matrix:" "\n", lr_confusion_matrix)
print("Logistic Regression - Classification report:" "\n", lr_classification)

lr_accuracy_test = metrics.accuracy_score(Y_test, lr_model.predict(X_test))
lr_confusion_matrix_test = metrics.confusion_matrix(Y_test, lr_model.predict(X_test))
lr_classification_test = metrics.classification_report(Y_test, lr_model.predict(X_test))

print("Logistic Regression - Model Accuracy (Test Set):" "\n", lr_accuracy_test)
print("Logistic Regression - Confusion matrix (Test Set):" "\n", lr_confusion_matrix_test)
print("Logistic Regression - Classification report (Test Set):" "\n", lr_classification_test)

lr_prediction = lr_model.predict(test_df)
test['lr_prediction'] = lr_prediction
print(test.head())

ratio_lr = test['lr_prediction'].value_counts()
labels_lr = ratio_lr.index[0], ratio_lr.index[1]
sizes_lr = [ratio_lr.values[0], ratio_lr.values[1]]

figure_lr, axis_lr = plt.subplots()
axis_lr.pie(sizes_lr, labels=labels_lr, autopct='%1.1f%%', startangle=90)
axis_lr.axis('equal')
plt.title("Logistic Regression Predictions on Test Data")
plt.show()

gb_model = GradientBoostingClassifier()
gb_model.fit(X_train, Y_train)

gb_scores = cross_val_score(gb_model, X_train, Y_train, cv=10)
gb_accuracy = metrics.accuracy_score(Y_train, gb_model.predict(X_train))
gb_confusion_matrix = metrics.confusion_matrix(Y_train, gb_model.predict(X_train))
gb_classification = metrics.classification_report(Y_train, gb_model.predict(X_train))

print("Gradient Boosting - Cross Validation Mean Score:" "\n", gb_scores.mean())
print("Gradient Boosting - Model Accuracy:" "\n", gb_accuracy)
print("Gradient Boosting - Confusion matrix:" "\n", gb_confusion_matrix)
print("Gradient Boosting - Classification report:" "\n", gb_classification)

gb_accuracy_test = metrics.accuracy_score(Y_test, gb_model.predict(X_test))
gb_confusion_matrix_test = metrics.confusion_matrix(Y_test, gb_model.predict(X_test))
gb_classification_test = metrics.classification_report(Y_test, gb_model.predict(X_test))

print("Gradient Boosting - Model Accuracy (Test Set):" "\n", gb_accuracy_test)
print("Gradient Boosting - Confusion matrix (Test Set):" "\n", gb_confusion_matrix_test)
print("Gradient Boosting - Classification report (Test Set):" "\n", gb_classification_test)

gb_prediction = gb_model.predict(test_df)
test['gb_prediction'] = gb_prediction
print(test.head())

ratio_gb = test['gb_prediction'].value_counts()
labels_gb = ratio_gb.index[1], ratio_gb.index[0]
sizes_gb = [ratio_gb.values[0], ratio_gb.values[1]]

figure_gb, axis_gb = plt.subplots()
axis_gb.pie(sizes_gb, labels=labels_gb, autopct='%1.1f%%', startangle=90)
axis_gb.axis('equal')
plt.title("Gradient Boosting Predictions on Test Data")
plt.show()

classifiers = ['KNN', 'SVM', 'Naive Bayes', 'Logistic Regression', 'Gradient Boosting']
train_accuracies = [accuracy, svm_accuracy, nb_accuracy, lr_accuracy, gb_accuracy]
test_accuracies = [accuracy_test, svm_accuracy_test, nb_accuracy_test, lr_accuracy_test, gb_accuracy_test]

bar_width = 0.35

plt.figure(figsize=(12, 6))
plt.bar(np.arange(len(classifiers)), train_accuracies, bar_width, color='blue', label='Training Data')
plt.bar(np.arange(len(classifiers)) + bar_width, test_accuracies, bar_width, color='red', label='Test Data')
plt.xticks(np.arange(len(classifiers)) + bar_width / 2, classifiers)
plt.ylim(0.85, 1.05, 0.2)
plt.xlabel('Classifiers')
plt.ylabel('Accuracy')
plt.title('Classifier Performance on Training and Test Data')
plt.legend()

for i, train_acc, test_acc in zip(np.arange(len(classifiers)), train_accuracies, test_accuracies):
    plt.text(i, train_acc + 0.01, f'{train_acc:.2f}', ha='center', va='bottom', color='black', fontweight='bold')
    plt.text(i + bar_width, test_acc + 0.01, f'{test_acc:.2f}', ha='center', va='bottom', color='black', fontweight='bold')

plt.show()