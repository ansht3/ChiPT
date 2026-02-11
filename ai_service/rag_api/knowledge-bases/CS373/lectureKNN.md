# Data Mining & Machine Learning  
### CS37300 — Purdue University  
### Instructor & Copyright: Bruno Ribeiro

# Lecture: K-Nearest Neighbors (kNN)

In this lecture we will introduce **$k$-Nearest Neighbors (kNN)**.

**Learning goals**
- Understand instance-based learning and how kNN defines decision boundaries.
- Compare discriminative vs probabilistic classification viewpoints.
- Reason about distance metrics ($L_1$, $L_2$, Mahalanobis) and scaling/standardization.
- See how sparsity affects binary similarity (Matching vs Jaccard).
- Build geometric intuition via Voronoi regions for 1NN.
- Recognize bias–variance trade-offs as $k$ varies and practical indexing options.

## Quiz

Which type of hypothesis is stronger?

- (a) Directional Relational Hypothesis  
- (b) Directional Causal Hypothesis  
- (c) Descriptive Hypothesis  
- (d) Non-Directional Relational Hypothesis

## k-Nearest Neighbors Components

### 1. Task Specification
- Supervised classification of instances
- In our example the **instances** will be ads served to users

### 2. Data Representation
- $n \times (p+1)$ tabular data with class label ($Y$) and $p$ *normalized* real-valued attributes ($X$)

### 3. Knowledge Representation
- k-NN, choosing $k$ neighbors to classify new instance
- **Model space:** All possible Voronoi tesselations of training data for $k$ neighbors
    - Depends on distance measure
    - Output depends on summarization function

### 4. Search + Scoring
- Store training data and delays processing until a new instance must be classified
- Assumes that all instances are represented in $p$-dimensional space
- Score is a distance measure (often a metric)
- Implicit search: choice of $k$ (number of neighbors), $d$ (distance measure), and $g$ (label summarization function) uniquely define a tessellation

### 5. Prediction and/or Interpretation
- Predicts a new instance by measuring its distance to training instances, chooses top $k$
- Function $g$ is used to predict new instance label

# k-Nearest Neighbors (k-NN) Algorithm

## 1. Discriminative classification

* **Idea:** Predict the label of a new point \$x\$ by looking at the labels of its \$k\$ closest training examples.
* **Step 1:** Compute distances from \$x\$ to all training points ($L_1$, $L_2$, Mahalanobis, ...).
* **Step 2:** Select the \$k\$ nearest neighbors.
* **Step 3:** Output the majority class among those neighbors (for regression, output the average value or a distribution defined over the $k$ values).
* **Observation:** The classifier’s decision boundary is not explicit but *emerges* from the neighborhoods defined by distance.


## 2. Discriminative vs Probabilistic Classification

- **Discriminative**: Directly learns $\hat{y} = \arg\!\max_y p(y\mid x)$ by creating a decision boundaries over the input space, disregarding probabilities.
- **Probabilistic**: model the distribution $p(y\mid x)$.
- k-NN is discriminative and **lazy**: it does not fit parameters for $p(y\mid x)$; it uses distances of the new instance $x$ to existing training points to infer labels.

## 3. Classification Setup
* Input: $n$ training examples: $X = \{x^{(1)}, \dots, x^{(n)}\}$, $x^{(i)} \in \mathbb{R}^p$, $p\geq 1$, $n \geq 1$.
* Output: $y \in \{1, 2, \dots, C\}$ where $C \geq 2$ is the number of classes.
* A classifier induces decision boundaries $h$ partitioning feature space into at least $C$ regions; for k-NN, these boundaries follow the local geometry of the training data and form Voronoi-like tessellations around training points of each class.

## 4. $L_1$ vs $L_2$ Distances

The **distance** between two points \${\bf x}^{(i)}, {\bf x}^{(j)} \in \mathbb{R}^p\$ is:

$$
\text{Euclidean:}\qquad L_2({\bf x}^{(i)}, {\bf x}^{(j)}) \;=\; \sqrt{\sum_{d=1}^p \Big(x^{(i)}_d - x^{(j)}_d\Big)^2}
$$

$$
\text{Manhattan:}\qquad L_1({\bf x}^{(i)}, {\bf x}^{(j)}) \;=\; \sum_{d=1}^p \Big|x^{(i)}_d - x^{(j)}_d\Big|
$$

The **unit ball** under a distance shows how neighborhoods look:

$$
\textbf{$L_2$ (Euclidean) unit ball of } {\bf x}' = {\bf x}^{(i)} - {\bf x}^{(j)} = \quad \big\{ {\bf x}' \in \mathbb{R}^p \; : \; \sum_{d=1}^p (x'_d)^2 \leq 1 \big\}
$$

$$
\textbf{$L_1$ (Manhattan) unit ball of }{\bf x}' = {\bf x}^{(i)} - {\bf x}^{(j)} = \quad \big\{ {\bf x}' \in \mathbb{R}^p \; : \; \sum_{d=1}^p |x'_d| \leq 1 \big\}
$$

* The \$L\_2\$ ball is a \$p\$-dimensional sphere (a circle if \$p=2\$), rotationally symmetric.
* The \$L\_1\$ ball is a \$p\$-dimensional diamond (rotated cube), aligned with the coordinate axes.


```python
# L1 diamond vs L2 circle
import numpy as np, matplotlib.pyplot as plt

theta = np.linspace(0, 2*np.pi, 400)
x2 = np.cos(theta); y2 = np.sin(theta)   # L2 unit circle

# L1 unit ball boundary: |x|+|y|=1 (draw as polygon)
t = np.linspace(-1, 1, 200)
diamond = np.vstack([
    np.c_[ t, 1-np.abs(t)],
    np.c_[ t[::-1], -(1-np.abs(t))],
    np.c_[ -(1-np.abs(t)), t],
    np.c_[  (1-np.abs(t)), t[::-1]]
])

plt.figure(figsize=(4,4))
plt.plot(x2, y2, label="$L_2$ unit circle")
plt.plot(diamond[:,0], diamond[:,1], label="$L_1$ unit ball")
plt.axhline(0, lw=0.5); plt.axvline(0, lw=0.5)
plt.gca().set_aspect("equal")
plt.legend(); plt.title("$L_1$ vs $L_2$ geometry")
plt.xlabel("$x_1$"); plt.ylabel("$x_2$")
plt.tight_layout(); plt.show()
```


    
![png](lectureKNN_files/lectureKNN_8_0.png)
    


## 5. Voronoi Intuition for 1-NN

1-NN assigns each point in $\mathbb{R}^2$ to its nearest training instance. The **Voronoi cell** of a training point is the set of locations closer to it than to any other point. Decision boundaries are the union of **bisectors** between neighboring training points.


```python
# 1-NN Voronoi tessellation in 2D
import numpy as np, matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from sklearn.datasets import make_blobs
from sklearn.metrics import pairwise_distances

# Data
X, y = make_blobs(n_samples=25, centers=4, cluster_std=1.5,
                  center_box=(-5.0, 5.0), random_state=42)
X[y == 2] *= 1.3  # spread class 2 a bit

# Grid & 1-NN labels on grid
x0, x1 = X[:,0], X[:,1]
xx, yy = np.meshgrid(np.linspace(x0.min()-1.5, x0.max()+1.5, 400),
                     np.linspace(x1.min()-1.5, x1.max()+1.5, 400))
G = np.c_[xx.ravel(), yy.ravel()]
nn_idx = pairwise_distances(G, X, metric="euclidean").argmin(axis=1)
labels = y[nn_idx].reshape(xx.shape)

# Discrete colormap + shared categorical normalization
n_classes = int(y.max()) + 1
base = plt.get_cmap("Set3")
cmap = ListedColormap(base.colors[:n_classes])
levels = np.arange(-0.5, n_classes + 0.5, 1)
norm = BoundaryNorm(levels, cmap.N)

# Plot
plt.figure(figsize=(8,6))
plt.contourf(xx, yy, labels, levels=levels, cmap=cmap, norm=norm, alpha=0.35)
plt.contour(xx, yy, labels, levels=levels, colors='black', linewidths=1.2, alpha=0.8)
plt.scatter(x0, x1, c=y, cmap=cmap, norm=norm, s=100, edgecolor='black', linewidth=1.2)
plt.title("1-NN Voronoi Tessellation (Euclidean)", fontsize=14)
plt.xlabel("$x_1$"); plt.ylabel("$x_2$")
plt.tight_layout(); plt.show()

from IPython.display import display, Markdown
display(Markdown(
"**Connection to decision boundaries:**  \n"
"- The 1-NN decision boundary between two training points lies along their perpendicular bisector.  \n"
"- In multi-class settings, boundaries are piecewise-linear segments separating Voronoi cells of different labels; "
"each cell contains points closer to its generator than to any other."
))

```


    
![png](lectureKNN_files/lectureKNN_10_0.png)
    



**Connection to decision boundaries:**  
- The 1-NN decision boundary between two training points lies along their perpendicular bisector.  
- In multi-class settings, boundaries are piecewise-linear segments separating Voronoi cells of different labels; each cell contains points closer to its generator than to any other.



```python
# Enhanced 1-NN Voronoi tessellation in 2D (Manhattan distance)
import numpy as np, matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from sklearn.datasets import make_blobs
from sklearn.metrics import pairwise_distances

# Data
X, y = make_blobs(n_samples=25, centers=4, cluster_std=1.5,
                  center_box=(-5.0, 5.0), random_state=42)
X[y == 2] *= 1.3  # spread class 2 a bit

# Grid & 1-NN labels on grid (Manhattan distance)
x0, x1 = X[:,0], X[:,1]
xx, yy = np.meshgrid(np.linspace(x0.min()-1.5, x0.max()+1.5, 400),
                     np.linspace(x1.min()-1.5, x1.max()+1.5, 400))
G = np.c_[xx.ravel(), yy.ravel()]
nn_idx = pairwise_distances(G, X, metric="manhattan").argmin(axis=1)
labels = y[nn_idx].reshape(xx.shape)

# Discrete colormap + shared categorical normalization
n_classes = int(y.max()) + 1
base = plt.get_cmap("Set3")
cmap = ListedColormap(base.colors[:n_classes])
levels = np.arange(-0.5, n_classes + 0.5, 1)
norm = BoundaryNorm(levels, cmap.N)

# Plot
plt.figure(figsize=(8,6))
plt.contourf(xx, yy, labels, levels=levels, cmap=cmap, norm=norm, alpha=0.35)
plt.contour(xx, yy, labels, levels=levels, colors='black', linewidths=1.2, alpha=0.8)
plt.scatter(x0, x1, c=y, cmap=cmap, norm=norm, s=100, edgecolor='black', linewidth=1.2)
plt.title("1-NN Voronoi Tessellation (Manhattan)", fontsize=14)
plt.xlabel("$x_1$"); plt.ylabel("$x_2$")
plt.tight_layout(); plt.show()

from IPython.display import display, Markdown
display(Markdown(
"**Connection to decision boundaries (Manhattan):**  \n"
"- The 1-NN decision boundary under Manhattan distance lies along lines where the $L_1$ distance to two points is equal.  \n"
"- Unlike Euclidean, these boundaries form rectilinear (axis-aligned) shapes, producing diamond-like Voronoi regions."
))

```


    
![png](lectureKNN_files/lectureKNN_11_0.png)
    



**Connection to decision boundaries (Manhattan):**  
- The 1-NN decision boundary under Manhattan distance lies along lines where the $L_1$ distance to two points is equal.  
- Unlike Euclidean, these boundaries form rectilinear (axis-aligned) shapes, producing diamond-like Voronoi regions.


## 6. Decision Boundaries as $k$ Varies (Two Moons)
**Why this matters.**  
- Small $k$ (e.g., $k=1$) yields low bias but high variance: the boundary tracks the training set closely and is sensitive to noise.  
- Larger $k$ (e.g., $k=15$) smooths idiosyncrasies at the cost of increased bias: the boundary is more stable but may underfit.

**What the code does.**  
- Generates a two-moons dataset.  
- Trains k-NN for $k\in\{1,15\}$.  
- Plots predicted labels over a dense grid to visualize the induced boundary.


```python
# Compact k-NN decision boundaries: original data, k=1, k=15
import numpy as np, matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.neighbors import KNeighborsClassifier

X, y = make_moons(n_samples=800, noise=0.25, random_state=45)

def plot_panel(ax, k=None):
    if k is None:  # just plot data
        ax.scatter(X[:,0], X[:,1], c=y, s=10)
        ax.set_title("Original Data")
    else:          # plot decision boundary
        clf = KNeighborsClassifier(n_neighbors=k).fit(X, y)
        xx, yy = np.meshgrid(
            np.linspace(X[:,0].min()-0.5, X[:,0].max()+0.5, 400),
            np.linspace(X[:,1].min()-0.5, X[:,1].max()+0.5, 400)
        )
        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
        ax.contourf(xx, yy, Z, alpha=0.25)
        ax.scatter(X[:,0], X[:,1], c=y, s=10)
        ax.set_title(f"k-NN (k={k})")
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")

fig, axs = plt.subplots(1, 3, figsize=(12, 4))
for ax, k in zip(axs, [None, 1, 400]):
    plot_panel(ax, k)
plt.tight_layout(); plt.show()
```


    
![png](lectureKNN_files/lectureKNN_13_0.png)
    



```python
import numpy as np
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import zero_one_loss

# Generate data
X, y = make_moons(n_samples=800, noise=0.25, random_state=45)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)

# Evaluate for k=1 and k=15
for k in [1, 15]:
    clf = KNeighborsClassifier(n_neighbors=k).fit(Xtr, ytr)
    ypred = clf.predict(Xte)
    err = zero_one_loss(yte, ypred)   # fraction misclassified
    print(f"k={k}, test error = {err*100:.3f}%")

```

    k=1, test error = 7.083%
    k=15, test error = 4.583%


**Takeaways.**  
- How well **kNN overfits** the training data is controlled by $k$: later we will see how to tune it via cross-validation (we will revisit this later).
- In high-noise settings, increasing $k$ often improves generalization; in clean, complex boundaries, small $k$ may be preferable.

### Evaluation Approach??

Testing a classifier on the **training data** can be misleading, since it does not measure generalization.

#### Quiz

* Between $k$-NN with $k=1$ and $k=15$, which one would appear to perform **best if evaluated only on the training set**?

(a) $k=1$

(b) $k=15$

Testing a model's accuracy on training data is a bit like saying Prof. Ribeiro can amazingly guess the Powerball numbers on Sept 8th:

<center><img src="powerball.png" width=200px/></center>

## 7. Why Feature Standardization Often Improves k-NN

k-NN depends on a distance $d(x,x')$. If features have different scales, one dimension can dominate $d_E$ (Euclidean), distorting neighborhoods.

- **Standardize** each feature:
$$
x'_k = \frac{x_k - \bar{x}_k}{\hat{\sigma}_k},
$$
where $\bar{x}\_k$ is the mean of feature $k$ and $\hat{\sigma}_k$ is its standard deviation.

- This transformation centers features at zero mean and scales them to unit variance.
  
- After standardization, features contribute comparably; this often yields more faithful neighborhoods and better accuracy.



```python
# k-NN with/without standardization
import numpy as np, matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from IPython.display import display, Markdown

# Print example description
markdown_output = """## **Example**: Consider the following code with different attribute scales."""
display(Markdown(markdown_output))


X, y = make_classification(n_samples=600, n_features=2, n_redundant=0,
                           n_informative=2, n_clusters_per_class=1,
                           class_sep=1.2, random_state=1)
# exaggerate scale disparity
X[:,0] *= 20.0

def decision_surface(ax, X_, y_, title):
    knn = KNeighborsClassifier(n_neighbors=7).fit(X_, y_)
    x0, x1 = X_[:,0], X_[:,1]
    xx, yy = np.meshgrid(np.linspace(x0.min()-1, x0.max()+1, 400),
                         np.linspace(x1.min()-1, x1.max()+1, 400))
    Z = knn.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    ax.contourf(xx, yy, Z, alpha=0.25)
    ax.scatter(x0, x1, c=y_, s=10, edgecolor="none")
    ax.set_title(title); ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")

fig, axs = plt.subplots(1,2, figsize=(10,4))
decision_surface(axs[0], X, y, "k-NN on unscaled features")
Xs = StandardScaler().fit_transform(X)
decision_surface(axs[1], Xs, y, "k-NN after standardization")
plt.tight_layout(); plt.show()

# Print explanation

markdown_output = """
**Interpretation.** - Left: $x_1$ dominates the distance; neighborhoods stretch along $x_2$.  
- Right: after standardization, the boundary better reflects both axes.  
- If features are correlated, consider **Mahalanobis** distance (described below) to account for covariance."""
display(Markdown(markdown_output))
```


## **Example**: Consider the following code with different attribute scales.



    
![png](lectureKNN_files/lectureKNN_19_1.png)
    




**Interpretation.** - Left: $x_1$ dominates the distance; neighborhoods stretch along $x_2$.  
- Right: after standardization, the boundary better reflects both axes.  
- If features are correlated, consider **Mahalanobis** distance (described below) to account for covariance.


## 8. Mahalanobis Distance: Accounting for Feature Covariance

If features are correlated, Euclidean distance can mis-measure proximity.
Mahalanobis rescales and de-correlates via the **inverse covariance matrix** \$\Sigma^{-1}\$:

$$
d_{MH}({\bf x}^{(i)},{\bf x}^{(j)})=\sqrt{({\bf x}^{(i)} - {\bf x}^{(j)})^\top \Sigma^{-1} ({\bf x}^{(i)} - {\bf x}^{(j)})}.
$$

Here, \$\Sigma\$ is the \$p \times p\$ covariance matrix of the feature vectors, with entries
$$
\Sigma_{ab} = \mathrm{Cov}(x_a, x_b), \quad \text{where $a,b \in \{1,\ldots,p\}$ are feature dimensions}
$$

The **inverse covariance matrix** $\Sigma^{-1}$ reweights directions according to variance and correlation: high-variance directions are downweighted, while correlations are removed.

Contours of constant distance become **ellipses** aligned with covariance eigenvectors.


```python
# Mahalanobis contours for a correlated Gaussian
import numpy as np, matplotlib.pyplot as plt
from numpy.linalg import inv

mu = np.array([0., 0.])
Sigma = np.array([[3.0, 2.4],
                  [2.4, 3.0]])  # positively correlated
Sinv = inv(Sigma)

x = np.linspace(-5, 5, 300)
y = np.linspace(-5, 5, 300)
xx, yy = np.meshgrid(x, y)
X = np.stack([xx - mu[0], yy - mu[1]], axis=-1)   # (H,W,2)

# squared Mahalanobis distance
d2 = np.einsum("...i,ij,...j->...", X, Sinv, X)

plt.figure(figsize=(5,4))
cs = plt.contour(xx, yy, np.sqrt(d2), levels=[1,2,3], linewidths=1.5)
plt.clabel(cs, inline=True, fontsize=8)
plt.title("Mahalanobis distance contours")
plt.xlabel("$x_1$"); plt.ylabel("$x_2$")
plt.gca().set_aspect("equal")
plt.tight_layout(); plt.show()

from IPython.display import display, Markdown
markdown_output = """
**Note:**  
- Estimating $\Sigma$ well can be hard in small $n$, large $p$. Consider shrinkage.  
- Complexity grows with $p^2$ to form $\Sigma$; inverses add cost."""
display(Markdown(markdown_output))
```


    
![png](lectureKNN_files/lectureKNN_21_0.png)
    




**Note:**  
- Estimating $\Sigma$ well can be hard in small $n$, large $p$. Consider shrinkage.  
- Complexity grows with $p^2$ to form $\Sigma$; inverses add cost.


## 9. Binary Similarity "Distance": Matching vs Jaccard

For binary vectors with counts $n_{11}, n_{10}, n_{01}, n_{00}$:

- **Matching coefficient** (treats $0$–$0$ as agreement):  
  $\dfrac{n_{11}+n_{00}}{n_{11}+n_{10}+n_{01}+n_{00}}$  
- **Jaccard** (ignores $0$–$0$ matches):  
  $\dfrac{n_{11}}{n_{11}+n_{10}+n_{01}}$  

In **sparse** settings (few ones), Jaccard is typically more informative.


```python
# Binary vectors: Matching coefficient vs Jaccard across a sweep
import numpy as np, matplotlib.pyplot as plt

p = 200
rng = np.random.default_rng(0)
ps = np.linspace(0.01, 0.99, 60)  # Bernoulli probs for x and y (same for simplicity)

mc, jc = [], []
for q in ps:
    x = rng.binomial(1, q, size=(2000, p))
    y = rng.binomial(1, q, size=(2000, p))
    n11 = (x & y).sum(axis=1)
    n10 = (x & (~y)).sum(axis=1)
    n01 = ((~x) & y).sum(axis=1)
    n00 = ((~x) & (~y)).sum(axis=1)

    match = (n11 + n00) / (n11 + n10 + n01 + n00)
    jacc  = n11 / np.maximum(1, (n11 + n10 + n01))
    mc.append(match.mean()); jc.append(jacc.mean())

plt.figure(figsize=(5,4))
plt.plot(ps, mc, label="Matching coefficient")
plt.plot(ps, jc, label="Jaccard coefficient")
plt.xlabel("Sparsity parameter (probability of 1)")
plt.ylabel("Expected similarity")
plt.title("Binary similarity vs sparsity")
plt.legend(); plt.tight_layout(); plt.show()


markdown_output = """**Example (sparse binary data):**
Suppose two users’ movie-rating vectors (1 = watched, 0 = not watched) over \$1000\$ movies:
* \$n\_{11} = 5\$ (both watched 5 movies)
* \$n\_{10} = 15\$ (user A only)
* \$n\_{01} = 10\$ (user B only)
* \$n\_{00} = 970\$ (neither watched)
* Matching coefficient:
  \$\$
  \\frac{5+970}{1000} = 0.975
  \$\$
  (appears very high due to shared zeros).

* Jaccard coefficient:
  \$\$
  \\frac{5}{5+15+10} = 0.143
  \$\$
  (more reflective of actual overlap in watched movies).
  
**Observation.**  
- As vectors become sparser (small probability of 1), Matching is inflated by the many $0$–$0$ matches; Jaccard stays sensitive to shared 1s.
"""
display(Markdown(markdown_output))
```


    
![png](lectureKNN_files/lectureKNN_23_0.png)
    



**Example (sparse binary data):**
Suppose two users’ movie-rating vectors (1 = watched, 0 = not watched) over \$1000\$ movies:
* \$n\_{11} = 5\$ (both watched 5 movies)
* \$n\_{10} = 15\$ (user A only)
* \$n\_{01} = 10\$ (user B only)
* \$n\_{00} = 970\$ (neither watched)
* Matching coefficient:
  \$\$
  \frac{5+970}{1000} = 0.975
  \$\$
  (appears very high due to shared zeros).

* Jaccard coefficient:
  \$\$
  \frac{5}{5+15+10} = 0.143
  \$\$
  (more reflective of actual overlap in watched movies).
  
**Observation.**  
- As vectors become sparser (small probability of 1), Matching is inflated by the many $0$–$0$ matches; Jaccard stays sensitive to shared 1s.



## 9. Practical Challenges

- **Complexity**:  
  - Training: $O(1)$ (storing data).  
  - Inference: naive $O(n)$ per query; with indices (KD-tree/Ball-tree), average-case $O(\log n)$ in low/moderate $p$; in high $p$, trees degrade.  
  - Search trees (e.g., KD, Ball, Cover trees) partition space hierarchically, enabling efficient pruning of candidate neighbors, but their effectiveness drops as dimensionality increases.  
  - For very large $n$, consider **Approximate NN** (e.g., locality-sensitive hashing, product quantization).

- **Choosing $k$**:  
  - Use cross-validation.  
  - Odd $k$ helps avoid ties in binary classification.  
  - Optionally **distance-weight** neighbors (e.g., weight by $1/(d+\epsilon)$) to emphasize closer points.

- **Feature engineering**:  
  - Standardization is often essential; consider PCA or whitening if strong correlations exist.  
  - For **mixed data types** (numeric + categorical), design composite distances or use embeddings.
  

## References

- Cover, T. & Hart, P. (1967). Nearest neighbor pattern classification. *IEEE Transactions on Information Theory*, 13(1), 21–27.  
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning* (2nd ed.). Springer (Chs. 2–13).  
- *scikit-learn* User Guide: Nearest Neighbors; Preprocessing (Standardization).
