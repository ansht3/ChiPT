## Generate Data


```python
%matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import numpy as np

# Generate some data
from sklearn.datasets import make_blobs

X, y_true = make_blobs(n_samples=[100, 100, 100, 50], centers=None,
                       cluster_std=1.60, random_state=42)
X = X[:, ::-1] # flip axes for better plotting


plt.scatter(X[:, 0], X[:, 1], s=40);
```


    
![png](Clustering2Dexample_files/Clustering2Dexample_1_0.png)
    


## Clustering with K-means

Note that the cluster colors are not required to be consistent between different clustering methods
- It is only important that the different clustering methods are able to distinguish the 4 clusters


```python
# Plot the data with K Means Labels
from sklearn.cluster import KMeans

kmeans = KMeans(4, random_state=42) # 4 clusters
labels = kmeans.fit(X).predict(X)

plt.scatter(X[:, 0], X[:, 1], c=labels, s=40, cmap='viridis');
```


    
![png](Clustering2Dexample_files/Clustering2Dexample_3_0.png)
    


## Clustering with a Gaussian Mixture Model

Note that the cluster colors are not required to be consistent between different clustering methods
- It is only important that the different clustering methods are able to distinguish the 4 clusters


```python
from sklearn import mixture


# fit a Gaussian Mixture Model with four components
gmm = mixture.GaussianMixture(n_components=4, covariance_type="full", max_iter=20, random_state=42)
gmm.fit(X)

labels = gmm.predict(X)

plt.scatter(X[:, 0], X[:, 1], c=labels, s=40, cmap='viridis');
```


    
![png](Clustering2Dexample_files/Clustering2Dexample_5_0.png)
    


## Clustering with Gaussian Mixture Model by Minimizing Negative Log-Likelihood with Gradient Descent (Hard)

Note that the cluster colors are not required to be consistent between different clustering methods
- It is only important that the different clustering methods are able to distinguish the 4 clusters



```python
# Requires pytorch 1.10 (released Oct 21, 2021)

import numpy as np
import matplotlib.pyplot as plt
import sklearn.datasets as datasets

import torch
from torch import optim
import torch.distributions as D
import torch.nn.functional as F

C = 4 # Number of distributions in the mixture
weights = torch.ones(C,requires_grad=True)
means = torch.tensor(np.random.randn(C,2),requires_grad=True)
# Only considers diagonal covariance matrices right now
_stdevs = torch.tensor(np.random.rand(C,2)*10,requires_grad=True)

parameters = [means, _stdevs]
optimizer1 = optim.SGD(parameters, lr=0.01, momentum=0.99)
parameters = [weights]
optimizer2 = optim.SGD(parameters, lr=0.001)

x = torch.from_numpy(np.flip(X,axis=0).copy())

num_iter = 10001
for i in range(num_iter):
    mix = D.Categorical(F.softmax(weights,dim=0))
    stdevs = _stdevs**2
    comp = D.Independent(D.Normal(means,stdevs), 1)
    gmm = D.MixtureSameFamily(mix, comp)

    optimizer1.zero_grad()
    optimizer2.zero_grad()
    loss2 = -gmm.log_prob(x).mean()
    loss2.backward()
    optimizer1.step()
    optimizer2.step()

    if i % 1000 == 0:
        print(f'Step {i} with loss {loss2.item()}')
```

    Step 0 with loss 8.856727181188647
    Step 1000 with loss 5.125036970368335
    Step 2000 with loss 5.088956430659944
    Step 3000 with loss 5.087538244037488
    Step 4000 with loss 5.086630715603499
    Step 5000 with loss 5.0860363423358335
    Step 6000 with loss 5.08563599421746
    Step 7000 with loss 5.085356149691853
    Step 8000 with loss 5.0851513293079424
    Step 9000 with loss 5.084993031433867
    Step 10000 with loss 5.0848624988391515



```python
print(f'Cluster assigments probabilities: {F.softmax(weights.data,dim=0).numpy()}')
```

    Cluster assigments probabilities: [0.28438735 0.20854636 0.27899325 0.22807312]


## Plot Cluster Results


```python
from scipy.stats import multivariate_normal

def normal_density(X,mean,stdev):
    rv = multivariate_normal(mean,stdev)
    return (rv.pdf(X))

```


```python
fig, ax_kwargs = plt.subplots(figsize=(6, 6))

ax_kwargs.axvline(c='grey', lw=1)
ax_kwargs.axhline(c='grey', lw=1)

# Plot the ellipse with zorder=0 in order to demonstrate
# its transparency (caused by the use of alpha).
col = ['yellow','magenta','blue','green']

p_X_given_K = np.zeros((4,X.shape[0]))

for cid in range(4):
    p_X_given_K[cid,:] = normal_density(X,means[cid,:].detach(), np.diag(stdevs[cid,:].detach()))

w = weights.view(4,1).detach().numpy()
    
# Posterior distribution gamma of clister assigments
gamma = (p_X_given_K * w[:,None]) / (p_X_given_K * w[:,None]).sum(axis=1)

# Cluster labels
labels = np.argmax(gamma, axis=1)[0,:]
    
#    samples_x1,samples_x2 = np.random.multivariate_normal(means[cid,:].detach(), np.diag(stdevs[cid,:].detach()), 5000).T
#    plot_confidence_ellipse(samples_x1,samples_x2, ax_kwargs,
#                   alpha=0.2, facecolor=col[cid], edgecolor='black', zorder=0)

ax_kwargs.scatter(X[:, 0], X[:, 1], c=labels, s=40, cmap='viridis');

fig.subplots_adjust(hspace=0.25)
plt.show()

```


    
![png](Clustering2Dexample_files/Clustering2Dexample_11_0.png)
    



```python

```


```python

```


```python

```
