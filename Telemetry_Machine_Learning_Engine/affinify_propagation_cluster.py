from sklearn import datasets
from sklearn import cluster
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import euclidean_distances

x, _ = datasets.make_blobs(n_samples=100, centers=2,n_features=2, random_state=10)
x1=[]
y1=[]
for xx in x:
    x1.append(xx[0])
    y1.append(xx[1])

plt.scatter(x1,y1)
plt.show()

S = euclidean_distances(x)
aff_pro = cluster.AffinityPropagation().fit(S)

labels = aff_pro.labels_
styles = ['o','x','^','.']

for style, label in zip(styles, np.unique(labels)):
    print(label)
    plt.plot(x[labels == label], style, label=label)

plt.show()

for label in np.unique(labels):
    print(x[labels == label])