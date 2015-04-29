from sklearn.ensemble import GradientBoostingClassifier
from environment import sample_file
from sklearn.cross_validation import train_test_split
from SupervisedLearning import SKSupervisedLearning
from train_files import TrainFiles
import matplotlib.pylab as plt
import numpy as np

X_train, Y_train, X_test, Y_test = TrainFiles.from_csv(sample_file, test_size = 0.2)
print "Read, train: {:d}, test: {:d}".format(X_train.shape[0], X_test.shape[0])

gbc = SKSupervisedLearning(GradientBoostingClassifier, X_train, Y_train, X_test, Y_test)
gbc.train_params = {'max_depth' : 100, 'min_samples_leaf': 3, 'n_estimators' : 5000}
gbc.scoring = "accuracy"
print "Instantiated classifier"

gbc.fit_standard_scaler()
gbc.fit_and_validate()

# downsample the test set for plotting
X, _, Y, _ = train_test_split(X_test, Y_test, test_size = 0.9)

x = np.arange(Y.size)
f = plt.figure(figsize= (15, 7))
plt.scatter(x, Y, color='green')

for pred in gbc.clf.staged_predict(X):
    plt.plot(x, pred, color='red')
