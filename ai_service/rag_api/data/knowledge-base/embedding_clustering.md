## CS37300 - Data Mining and Machine Learning (Extra Notes)
----
# Unsupervised Learning
## Manifold Clustering

#### Manifold embedding methods

The above clustering / embedding methods all assume the data lives in Euclidean space
- Euclidean space assumes
    - triangle inequality (closeness in Euclidean space = same cluster)
    - a global definition of distance
- Often, Euclidean assumption creates wrong clusters and prevents good low-dimensional embeddings

<center><img src="ManifoldClustering.png" width=400px></center>

### Issues with global definition of distancess

Define a meaninful distance between two chairs (easy):
<center><img src="chair1.png" width=150px></center>
<center><img src="chair2.png" width=100px></center>

Define a meaninful distance between a chair and an airplane (hard):
<center><img src="chair1.png" width=150px></center>
<center><img src="airplane.png" width=150px></center>

### What is a Manifold?

- A **manifold** is a space where we **only define distances between nearby objects**

- On Earth, we are always talking about **manifold** distances, never Euclidean distances
    - Earth distances, however, are locally Euclidean
    - Going from West Lafayette to Indianapolis will obey most properties that we expect in an Euclidean space
    - But, going from Indianapolis to Augusta, Western Australia will not.
        - Indianapolis and Augusta, Western Australia are 7,917 miles away through the dead center of Earth
            - But nobody would say we are only 7,917 miles away from Augusta, Western Australia.
            - By airplane, it takes 11,199 miles to do the same trip

- On a manifold, even simple properties like "the sum of the angles of a triangle is 180$^o$ may be no longer true
    - But "the sum of the angles of a triangle is 180$^o$" may be locally true, at a small patch of the manifold
<center><img src="manifold_example.jpg" width=400px></center>

Earth is a manifold where the shortest distance between far-away objects is not the trajectory with the smallest Euclidean distance
<center><img src="airroute.jpeg" width=300px></center>
    
[Image ack](https://lifethroughamathematicianseyes.wordpress.com/2016/02/06/differential-geometry-day/)

### Manifold Embedding Methods

- Consider a chair as a set $V$ of points in 3D space, $x \in V$ with $x \in \mathbb{R}^3$.

- Create an undirected graph $G=(V,E)$ where
    - The points $V$ are the nodes
    - Two points $u,v \in V$ have Euclidean distance less than some thredhold $T$, $\Vert u -v\Vert_2 < T$, then $(u,v)$ is an edge in $G$, $(u,v) \in E$, with edge weight $w_{u,v} = \Vert u -v\Vert_2$.
    
<center><img src="chair_cloud.jpg" width=400px/></center>
- PS: Note that this is different from a "3D mesh", since a 3D mesh forms polygons that don't intersect, while $G$ is not guaranteed to have this property


Manifold embedding methods define distances only for "close-enough" points:
- Points are nodes in a graph
- Weighted edges represent distances among "close-enough" points
- "Points" can be anything, such as user features, not just 2D or 3D points.

<center><img src="RollManifoldGraph.png" width=450px /></center>

### UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction

[UMAP](https://umap-learn.readthedocs.io/en/latest/) is considered by many as the state-of-the-art manifold emebdding/clustering method.
- McInnes, L, Healy, J, UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction, ArXiv e-prints 1802.03426, 2018 (*the paper was rejected by all top journals, it is only available on ArXiv*)

#### UMAP algorithm (part 1):

- UMAP weight (part 1): defined a Markov chain with an exponential probability in high dimension
$$
  p_{i|j} = \exp\left(-\frac{d(x_j,x_i) - \rho_i}{\sigma_i}\right),
$$
where $d$ is some distance function, $\rho_i$ is the distance from each i-th data point to its first nearest neighbor and $\sigma_i$ is the standard deviation of the distances to all other data points. 
    - This definition of "distance" ensures local connectivity in the graph (no isolated nodes).

- UMAP weight (part 2): UMAP now makes an undirected probability:
$$
p_{ij} = p_{i|j}  + p_{j|i} - p_{i|j}p_{j|i}  
$$

#### UMAP Embedding (Advanced)

<img src="ME.png" width=600px>

The embedding $u_i$ and $u_j$ are defined as:
- Typically, UMAP uses the embedding distance $$d_e(u_i,u_j)= \frac{1}{1+a(u_i - u_j)^{2b}},$$ where $a, b > 0$ are parameters of the method. By default, $a\approx 1.93$ and $b \approx 0.79$.
- Note that $d_e(u_i,u_j) \in (0,1)$ can be seen as a probability

#### UMAP algorithm (part 2) (Advanced):

- Let ${\bf U} \in \mathbb{R}^{n\times d}$ be a matrix whose $i$-th row is $u_i$.

- The score (loss) function of the embedding the graph in low dimensional space ${\bf U}$, UMAP uses an average negative log-likelihood (binary cross-entropy):
$$
L({\bf U}) = -\sum_{i=1}^n \sum_{j=1, j\neq i}^n p_{ij} \log\left(\frac{p_{ij}}{d_e(u_i,u_j)}\right) + (1-p_{ij}) \log\left(\frac{1-p_{ij}}{1-d_e(u_i,u_j)}\right)
$$

- The optimization is 
$$
{\bf U}^\star = \arg\!\min_{\bf U} L({\bf U}).
$$

#### Example from [UMap's Docummentation](https://umap-learn.readthedocs.io/en/latest/basic_usage.html)

In order to setup the CS373 environment on the Scholar cluster, please follow the instructions [here](../../howto/cluster-how-to.html)

For this example we will need the `umap` library:
```bash
$ module load learning/conda-5.1.0-py36-gpu

$ source activate CS373

$ conda install -c conda-forge umap-learn
```



```python
## UMap example from https://umap-learn.readthedocs.io/en/latest/basic_usage.html
import numpy as np
from sklearn.datasets import load_digits
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
%matplotlib inline

```


```python
## Load data
digits = load_digits()
# Images are B/W, 8 x 8 pixels
# There are 1797 images
print(digits.data.shape)
```

    (1797, 64)



```python
# Show data
fig, ax_array = plt.subplots(20, 20)
axes = ax_array.flatten()
for i, ax in enumerate(axes):
    ax.imshow(digits.images[i], cmap='gray_r')
plt.setp(axes, xticks=[], yticks=[], frame_on=False)
plt.tight_layout(h_pad=0.5, w_pad=0.01)
```


    
![png](embedding_clustering_files/embedding_clustering_19_0.png)
    


#### We will now apply PCA


```python
from sklearn.decomposition import PCA

# Two-dimensional embeddings using PCA
#   By defult, PCA will center the data
pca = PCA(n_components=2)

pca.fit(digits.data)
```




    PCA(n_components=2)



Let's look at the resulting embeddings (colors determine the labels 0-9)


```python
embedding = pca.transform(digits.data)

plt.scatter(embedding[:, 0], embedding[:, 1], c=digits.target, cmap='Spectral', s=5)
plt.gca().set_aspect('equal', 'datalim')
plt.colorbar(boundaries=np.arange(11)-0.5).set_ticks(np.arange(10))
plt.title('PCA projection of the Digits dataset', fontsize=24);
```


    
![png](embedding_clustering_files/embedding_clustering_23_0.png)
    


#### Applying UMAP to digits data


```python
import umap

reducer = umap.UMAP()
# Fits the data to UMAP embedding
reducer.fit(digits.data)
```




    UMAP(dens_frac=0.0, dens_lambda=0.0)



Let's look at the resulting embedding dimensions


```python
# Project the data into the new embedding
embedding = reducer.transform(digits.data)
# Verify that the result of calling transform is
# identical to accessing the embedding_ attribute
assert(np.all(embedding == reducer.embedding_))

print(f'Dimensionality of the embedding: {embedding.shape}')
```

    Dimensionality of the embedding: (1797, 2)


Let's look at the embeddings of the digits


```python
plt.scatter(embedding[:, 0], embedding[:, 1], c=digits.target, cmap='Spectral', s=5)
plt.gca().set_aspect('equal', 'datalim')
plt.colorbar(boundaries=np.arange(11)-0.5).set_ticks(np.arange(10))
plt.title('UMAP projection of the Digits dataset', fontsize=24);
```


    
![png](embedding_clustering_files/embedding_clustering_29_0.png)
    



```python

```
