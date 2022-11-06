import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

dataset = pd.read_csv('/Users/rajatnathan/Desktop/UnderlyingOptionsEODCalcs_TrainOUT_ALL.csv')
dataset.set_index('date',drop=True, inplace=True)

#features and label
x = dataset.filter(['lagtradevoldiff', 'lagOIdiff', 'lagbidaskdiff', 'lagavgclose'], axis=1)

y = dataset.filter(['upordown'], axis=1)


#data splitting
from sklearn.model_selection import train_test_split 
xtrain, xtest, ytrain, ytest = train_test_split( 
        x, y, test_size = 0.25, random_state = 0)      
print (xtest)
print (ytest)

#feature scaling
#from sklearn.preprocessing import StandardScaler 
#sc_x = StandardScaler() 
#xtrain = sc_x.fit_transform(xtrain)  
#xtest = sc_x.transform(xtest) 
#print (xtrain[0:10, :]) 

#training the model
from sklearn.linear_model import LogisticRegression 
classifier = LogisticRegression(random_state = 0) 
classifier.fit(xtrain, ytrain)

#predict on test set
y_pred = classifier.predict(xtest)

df2 = pd.DataFrame((y_pred), columns=list('P'))
df2 = df2.set_index(xtest.index)
print (df2)

z = xtest.copy()

z ['predicted'] =  df2.P
z['actual'] = ytest.upordown
print (z)


#performance of the model - a11 + a22 = true pos + true neg
y2_pred = classifier.predict(xtest)
from sklearn.metrics import confusion_matrix 
cm = confusion_matrix(ytest, y2_pred) 
  
print ("Confusion Matrix : \n", cm)

#accuracy
from sklearn.metrics import accuracy_score 
print ("Accuracy : ", accuracy_score(ytest, y2_pred))




#visualization

#from matplotlib.colors import ListedColormap 
#X_set, y_set = xtest, ytest 
#X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1,  
#                               stop = X_set[:, 0].max() + 1, step = 0.01), 
#                     np.arange(start = X_set[:, 1].min() - 1,  
#                               stop = X_set[:, 1].max() + 1, step = 0.01)) 
  
#plt.contourf(X1, X2, classifier.predict( 
#             np.array([X1.ravel(), X2.ravel()]).T).reshape( 
#             X1.shape), alpha = 0.75, cmap = ListedColormap(('red', 'green'))) 
  
#plt.xlim(X1.min(), X1.max()) 
#plt.ylim(X2.min(), X2.max()) 
  
#for i, j in enumerate(np.unique(y_set)): 
#    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1], 
#                c = ListedColormap(('red', 'green'))(i), label = j) 
      
#plt.title('Classifier (Test set)') 
#plt.xlabel('features') 
#plt.ylabel('output') 
#plt.legend() 
#plt.show() 