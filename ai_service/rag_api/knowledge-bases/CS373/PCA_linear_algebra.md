## CS37300 - Data Mining & Machine Learning
## Fall 2024
##### Instructor: Bruno Ribeiro
##### Slides: Bruno Ribeiro

----
## PCA and ICA (Unsupervised Learning)

### Recap: Linear Algebra Basics

1. Matrix multiplication is *not commutative*:
$$\left[\begin{array}{cc} 0 & 1 \\ 0 & 0 \end{array}\right] \left[\begin{array}{cc} 0 & 0 \\ 1 & 0 \end{array}\right] = \left[\begin{array}{cc} 1 & 0  \\ 0 & 0 \end{array}\right]$$
$$\neq$$
$$\left[\begin{array}{cc} 0 & 0 \\ 1 & 0 \end{array}\right] \left[\begin{array}{cc} 0 & 1 \\ 0 & 0 \end{array}\right] = \left[\begin{array}{cc} 0 & 0 \\ 0 & 1 \end{array}\right]$$

2. Inner product $\langle {\bf x},{\bf y} \rangle = {\bf x} {\bf y}^T = \sum_i x_i y_i$, where ${\bf y}^T$ is the transpose of vector ${\bf y}$.
Consequences
    1. $\langle {\bf x},{\bf x} \rangle \geq 0$
    2. $\Vert x \Vert^2 = \langle {\bf x},{\bf x} \rangle$
    3. $\langle {\bf x},{\bf y} \rangle = 0$ if an only if ${\bf x} \perp {\bf y}$ (that is, ${\bf x}$ and ${\bf y}$ are orthogonal).
    4. $\langle {\bf x},{\bf y} \rangle = \Vert {\bf x} \Vert \Vert {\bf y} \Vert \cos \theta$, thus ${\bf y} \langle {\bf x},{\bf y} \rangle = \Vert {\bf x} \Vert {\bf u}$, where ${\bf u}={\bf y}/\Vert {\bf y} \Vert.$
    
    
3. Notation: 
    - We will denote ${\bf A}_{i,\cdot}$ as the $i$-th row of matrix ${\bf A}$
    - We will denote ${\bf A}_{\cdot,j}$ as the $j$-th column of matrix ${\bf A}$

### Orthogonal vectors

Consider row vectors ${\bf u}_1,\ldots,{\bf u}_k \in \mathbb{R}^k$

- Vector ${\bf u}_i$ is **normalized** if $\langle {\bf u}_i, {\bf u}_i \rangle = 1$, also defined as $\Vert {\bf u}_i \Vert = 1$.
- Vectors ${\bf u}_i$ and ${\bf u}_j$ are **ortogona**l if $\langle {\bf u}_i, {\bf u}_j \rangle = 0$ also defined as ${\bf u}_i \perp {\bf u}_j$.
- Vectors ${\bf u}_i$ and ${\bf u}_j$ are **orthonormal** if they are both orthogonal and normalized.
    - If ${\bf U}$ is a matrix $${\bf U} = \left[ \begin{array}{c} {\bf u}_1 \\ \vdots \\ {\bf u}_k \end{array} \right]$$ then ${\bf U}{\bf U}^T = I$, where $I$ is the identity matrix.
    
    

### Orthogonal projections

For any ${\bf a} \in \mathbb{R}^k$,  $${\bf a} = \sum_{i=1}^k ({\bf a} {\bf u}_i^T) {\bf u}_i$$

<center><img src="projection.png" width=300px></center>

This means that ${\bf U}$ is a basis for $\mathbb{R}^k$ (see figure for an example on $\mathbb{R}^2$).


### Non-orthonormal basis

Can we have a non-orthonormal basis?

Yes.

Let $${\bf U} = \left[ \begin{array}{c} {\bf u}_1 \\ {\bf u}_2 \end{array} \right]$$

- ${\bf v}_1 = 2 {\bf u}_1 + {\bf u}_2$
- ${\bf v}_2 = {\bf u}_1 +  2 {\bf u}_2$

The vectors ${\bf v}_1$ and ${\bf v}_2$ are not orthogonal:
$$
\langle {\bf v}_1, {\bf v}_2 \rangle = 4,
$$
but $${\bf V} = \left[ \begin{array}{c} {\bf v}_1 \\ {\bf v}_2 \end{array} \right]$$ is still a basis for $\mathbb{R}^2$.

### Eigenvalues and Eigenvectors

Let ${\bf A} \in \mathbb{R}^{n \times n}$ be a $n \times n$ matrix and ${\bf v} \in \mathbb{R}^{1\times n}$ be a row vector.

Then, ${\bf v}$ is called a (left) eigenvector of ${\bf A}$ if
$$
{\bf v} {\bf A}  = \lambda {\bf v},
$$
and ${\bf v}$ is non-trivial (e.g., ${\bf v} \neq 0$) and $\lambda \in \mathbb{R}$.
We generally assume $\Vert {\bf v} \Vert=1$.

<center><img src="eigenvectors.png" width=500px></center>

- For simplicity, we will **assume the eigenvalues are all real to simplify our exposition**.

- Assume ${\bf A}$ is diagonalizable (nondefective). Then, ${\bf A}$ has $n$ linearly independent eigenvectors ${\bf v}_1,\ldots,{\bf v}_n$.
- Let $${\bf V} = \left[ \begin{array}{c} {\bf v}_1 \\ \vdots \\ {\bf v}_n \end{array} \right]$$ be a set of $n$ distinct eigenvectors of ${\bf A}$.

#### Properties of eigenvectors (for a diagonalizable ${\bf A}$):
- ${\bf V} A = \Lambda {\bf V}$, where $$ \Lambda = \left[ \begin{array}{cccc} ~{\bf \lambda}_1 & 0 & \cdots & 0 \\ 0 & \lambda_2 & \cdots & 0 \\ \vdots & \vdots & \cdots & \vdots \\ 0 & 0 & \cdots & \lambda_n \end{array} \right]$$
- The above implies $A = {\bf V}^{-1} \Lambda {\bf V} $.
- Matrix powers are now easy to compute: $${\bf A}^t = {\bf V}^{-1} \Lambda {\bf V}  {\bf A}^{t-1} = {\bf V}^{-1} \Lambda {\bf V} {\bf V}^{-1} \Lambda {\bf V} {\bf A}^{t-2} = {\bf V}^{-1} \Lambda^2 {\bf V} {\bf A}^{t-2} = \cdots =  {\bf V}^{-1} \Lambda^t {\bf V}.$$
- Matrix inversion is also easy to compute $${\bf A}^{-1} = {\bf V}^{-1} \Lambda^{-1} {\bf V}.$$ 
- The real challenge remains finding ${\bf V}$ and inverting it (${\bf V}^{-1}$).

#### Positive and Nonnegative Matrices and Vectors

We say a matrix or vector is
- **positive** (or elementwise positive) if all its entries are positive. We will denote ${\bf A} > 0$
- **nonnegative** (or elementwise nonnegative) if all its entries are nonnegative. We will denote ${\bf A} \geq 0$

A matrix is called **regular** if for some $k \geq 1$, $ {\bf A}^k > 0$.

#### (Detour) Covariance
- We start defining covariance: 
    - Measures how two random variables $X$ and $Y$ vary together
    - Let ${\bf x}$ be a vector with $n$ elements, where $x_i$ is an independent sample of $p(X)$
    - Let ${\bf y}$ be a vector with $n$ elements, where $y_i$ is an independent sample of $p(Y)$
    - Let $\bar{\bf x}$ be the empirical average values of ${\bf x}$
    - Let $\bar{\bf y}$ be the empirical average values of ${\bf y}$
 

$$\text{COV}({\bf x},{\bf y}) = \frac{1}{n-1} \sum_{i=1}^n ({\bf x}_i - \bar{\bf x})({\bf y}_i - \bar{\bf y})$$
- Positive if large values of X are linearly associated with large values of Y
- Negative if large values of X are linearly associated with small values of Y
        
<center><img src="COV.png" width=500px></center>


```python
%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np

# Create Data:
x = np.random.uniform(0,10,(25,))
y = x + np.random.standard_normal((25,))
z = np.column_stack((x,y))
# Scatter Plot
plt.scatter(x,y)

```




    <matplotlib.collections.PathCollection at 0x115633cd0>




    
![png](PCA_linear_algebra_files/PCA_linear_algebra_12_1.png)
    



```python
# Compute covariance (as a matrix, variance shows in the diagonal, off-diagonal is the covariance):
np.cov(x,y)
```




    array([[5.19866829, 5.04982654],
           [5.04982654, 6.06748839]])



#### (Detour) Correlation Coefficient
- Covariance depends on ranges of X and Y
- Correlation standardizes covariance by dividing through standard deviations
- Let $\hat{\sigma}_{\bf x}$ be the empirical standard deviation of $X$ 
- Let $\hat{\sigma}_{\bf y}$ be the empirical standard deviation of $Y$

$$\rho({\bf x},{\bf y}) = \frac{\text{COV}({\bf x},{\bf y})}{\hat{\sigma}_{\bf x} \hat{\sigma}_{\bf y}}$$


```python
# Compute correlation (as a matrix, diagonal are ones, off-diagonal is the correlation):
np.corrcoef(x,y)
```




    array([[1.        , 0.89913712],
           [0.89913712, 1.        ]])



### Recap: Correlation Matrix
- $p \times p$ symmetric matrix of correlations for p random variables
- What values are on the diagonal?
<center><img src="CORMATRIX.png" width=300px></center>

#### Covariance matrix ($\Sigma$)

- Covariance matrix is the same as the correlation matrix but for the covariance rather than the correlation

- Input data: Matrix ${\bf D}$ with $n$ rows and $p$ columns (number of attributes):
    - Columns are attributes, the different random variables (e.g., sepal length, sepal width, ...)
    - Rows are data points, the samples (e.g., the flowers in our garden)


- Creating the covariance matrix:
    - Preprocess ${\bf D}$ so that the mean of each column is 0, call this matrix ${\bf X}$
        - That is, for each row $i$ of ${\bf D}$ define a row of ${\bf X}$ as ${\bf X}_{i,\cdot} = ({\bf D}_{i,\cdot} - \bar{\bf D})$, where $\bar{\bf D} = \frac{1}{n}\sum_{i=1}^n {\bf D}_{i,\cdot}$.
    - Compute the $p \times p$ covariance matrix:
    $$
    \Sigma =\frac{1}{n-1} {\bf X}^T {\bf X}
    $$
    - Each element $\Sigma_{i,j} = \text{COV}({\bf X}_{\cdot,i},{\bf X}_{\cdot,j})$ is the covariance of the $i$-th column vector ${\bf X}_{\cdot,i}$ with the $j$-th column vector ${\bf X}_{\cdot,j}$. 

    
## Low Dimensional Projections

- We want to identify and describe the “real dimensions” that underlie the data

- Reduce dimensionality of modeling problem
    - Benefit is simplification, it reduces the number of variables you have to deal with in modeling

- Can identify set of variables with similar behavior

- The idea is to project the data from its original high-dimensional space into a lower dimensional space (something more manageable)

### Dimensionality reduction methods

- **Principal component analysis (PCA)**
    - Linear transformation, minimizes unexplained variance

- **Independent Component Analysis (ICA)**
    - Projects into low-dimensional subspace by finding components that are statistically independent and non-Gaussian

- **Manifold methods** (t-SNE, UMAP)
    - Data point distances only defined between points considered *close*
    - We will see these when we talk about clustering

### Principal Component Analysis (PCA)

- Developed by Harold Hotelling (1933) and independently by Pearson
- It is based on the covariance matrix

## Principal Component Analysis (PCA)

**Goal:** Find a linear projection that maximizes the variance of the projected data

- Given a $p$-dimensional vector ${\bf x} \in \mathbb{R}^p$, find an orthonormal basis (matrix) ${\bf V} \in \mathbb{R}^{p \times k}$ and a vector ${\bf z} \in \mathbb{R}^k$, $k \leq p$, such that 
$$ {\bf x} = {\bf V}{\bf z} $$
and ${\bf z}$ has uncorrelated components ${\bf z}_i$.

**Model space:** set of $k$ orthonormal basis vectors ${\bf V}$
- All basis vectors have norm of 1
- Any pair of basis vectors have dot-product of 0

#### Finding ${\bf V}$
- Compute eigenvectors & eigenvalues of the covariance matrix $\Sigma$:
$$
{\bf V} \Sigma = \Lambda {\bf V}
$$
    - Eigenvectors ${\bf V}$ are the principal component vectors, where each is a $k \times 1$ column vector
    - Since any two eigenvectors ${\bf v}_i$ and ${\bf v}_j$ are orthogonal, they have 0 covariance, i.e., $\langle {\bf v}_i, {\bf v}_j \rangle = {\bf v}_i^T {\bf v}_j = 0$, $\forall i,j \in \{1,\ldots,k\}, i\neq j$.

E.g., for orthogonal vectors  ${\bf v}_1$ and ${\bf v}_2$
- 1st basis (eg. ${\bf v}_1$) maximizes variance of projected data
- 2nd basis (eg. ${\bf v}_2$) again maximizes variance of projected data, but has to be orthogonal to previous bases, ...
  
<center><img src="PCA2.png" width=300px></center>

#### Eigenvalues and Variance
- $\Lambda$ is the eigenvalue diagonal matrix 
    - Convention is to order $\lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_k$.
    - **The variance of dimension $i$ is** $\lambda_i$ (i-th largest eigenvalue)

- Sum of eigenvalues is equal to the sum of the variances of the original dimensions $$
\sum_{j=1}^p \hat{\sigma}_j^2 = \sum_{j=1}^k \lambda_j
$$

    -  Solving eigensystem corresponds to finding the orthonormal basis that maximizes variance $$
    {\bf V} \Sigma{\bf V}^{T} = \Lambda 
$$
        - Because $\Sigma$ is positive semidefinite, hence ${\bf V}^{-1}={\bf V}^T$.
        -  A matrix is positive semidefinite if for all row vector $\forall {\bf z} \in \mathbb{R}^{1\times k}$, then ${\bf z} \Sigma {\bf z}^T \geq 0$.

- PCA complexity $O(np^2+p^3)$

### Applying PCA for dimensionality reduction

Given a new $p$-dimensional vector ${\bf x}' \in \mathbb{R}^p$, we choose the first $k' \leq k \leq p$ eigenvectors in ${\bf v}_1,\ldots,{\bf v}_{k'}$ and project ${\bf x}'$ into this new basis $${\bf z}_i = \langle{\bf x}',{\bf v}_i\rangle, \qquad i \in \{1,\ldots,k'\}.$$

- Now we can describe ${\bf x}'$ approximately as the vector ${\bf z} = ({\bf z}_1,\ldots,{\bf z}_{k'})$ in the new basis $\{{\bf v}_1,\ldots,{\bf v}_{k'}\}$
    - If $k'$ is chosen such that the basis captures most of the variance in the data. That is, $\sum_{i=1}^{k'} \lambda_i \gg \sum_{i=k'+1}^{k} \lambda_i$ (see example below)

<center><img src="PCA_components.png" width=300px></center>
    

### GPU  & CPU Implementation of the PCA  Algorithm


```python
## First, let's look at the dataset
# Load iris dataset
from sklearn import datasets

iris = datasets.load_iris()

# Copy original data
D = iris.data
# Center the data
X = D - np.mean(D,axis=0)
# Normalize the data
X = X/np.std(X,axis=0)

```


```python
# Plot feature values of original IRIS data
fig = plt.figure(1, figsize=(9, 6))
ax = fig.add_subplot(111)
bp = ax.boxplot(iris.data)
plt.ylabel('Feature value',size=16)
plt.title('Iris original data',size=18)
labels = ['Sepal length', 'Sepal width', 'Petal length', 'Petal width']
x_pos = [i for i in range(1,len(labels)+1)]
plt.xticks(x_pos, labels, rotation=45,size=16)
#fig.savefig('fig1.png', bbox_inches='tight')
```




    ([<matplotlib.axis.XTick at 0x137dfca30>,
      <matplotlib.axis.XTick at 0x137dfca00>,
      <matplotlib.axis.XTick at 0x137e229d0>,
      <matplotlib.axis.XTick at 0x137e76040>],
     [Text(1, 0, 'Sepal length'),
      Text(2, 0, 'Sepal width'),
      Text(3, 0, 'Petal length'),
      Text(4, 0, 'Petal width')])




    
![png](PCA_linear_algebra_files/PCA_linear_algebra_34_1.png)
    



```python
# Plot feature values of centered + normalized IRIS data
fig = plt.figure(1, figsize=(9, 6))
ax = fig.add_subplot(111)
bp = ax.boxplot(X)
plt.ylabel('Feature value',size=16)
plt.title('Normalized Iris data',size=18)
labels = ['Sepal length', 'Sepal width', 'Petal length', 'Petal width']
x_pos = [i for i in range(1,len(labels)+1)]
plt.xticks(x_pos, labels, rotation=45,size=16)
#fig.savefig('fig1.png', bbox_inches='tight')
```




    ([<matplotlib.axis.XTick at 0x137ebba00>,
      <matplotlib.axis.XTick at 0x137ebb9d0>,
      <matplotlib.axis.XTick at 0x137e22a00>,
      <matplotlib.axis.XTick at 0x137f2f1f0>],
     [Text(1, 0, 'Sepal length'),
      Text(2, 0, 'Sepal width'),
      Text(3, 0, 'Petal length'),
      Text(4, 0, 'Petal width')])




    
![png](PCA_linear_algebra_files/PCA_linear_algebra_35_1.png)
    



```python
## PCA Implementation using PyTorch for GPU & CPU

# Based on implementation by https://medium.com/@ravikalia/pca-done-from-scratch-with-python-2b5eb2790bfc
# (c) Bruno Ribeiro
#  Implemented cuda version and improved overall performance

import torch

def PCA_torch(X,k, device, center=True, scale=False):
    # Gets the size of X
    n,p = X.size()
    
    # Sends X to the appropriate memory (CPU or GPU) for our computations
    #  Note that it makes a copy of X
    X_new = X.to(device=device,dtype=torch.float32) 
    
    print(f'X is in GPU = {X_new.is_cuda}')
    
    if center:
        # Mean of each column
        mean = X_new.mean(axis=0,keepdim=True)
        # Subtract each row in X by the column mean
        X_new = X_new - mean

    # Computes covariance matrix.
    covariance = 1/(n-1) * (X_new.T @ X_new)

    if scale:
        # If we beed ti scale
        scaling =  torch.sqrt(1/torch.diag(covariance))
        covariance = torch.diag(scaling).view(p,p) @ covariance

    eigenvalues, eigenvectors = torch.linalg.eig(covariance)
    # Cast complex vectors as real (these eigenvalues & eigenvectors have no imaginary component)
    eigenvalues = eigenvalues.real
    eigenvectors = eigenvectors.real
    
    components = (eigenvectors[:, :k]).T
    explained_variance = eigenvalues[:k]
    
    return {'k':k, 'components':components.cpu(),'explained_variance':explained_variance.cpu()}
```

### Applying PCA

Let's apply PCA to reduce the dimensionality of the Iris dataset:
- The Iris dataset represents flowers with 4 attributes: sepal length, sepal width, petal length and petal width. 

- The Principal Component Analysis (PCA) applied to this data identifies the combination of attributes (principal components, or directions in the feature space) that account for the most variance in the data.
    - The dataset contains 3 kind of flowers (Setosa,Versicolor,Virginica) but we will not use the type of flower in our analysis (we will assume it is hidden from us)

- Here we will plot the different samples on the 2 first principal components.


```python
%matplotlib inline
import matplotlib.pyplot as plt
import torch

iris = datasets.load_iris()
iris_data = torch.from_numpy(iris.data)
n, p = iris_data.size()

# Returns 2 components
k = 4

print(f'p={p}, k={k}')

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

PCA_output = PCA_torch(iris_data, k, device)

# Percentage of variance explained for each components
print(f'Explained variance ratio (first two components): {PCA_output["explained_variance"]}\n\n')

print(f'PCA basis={PCA_output["components"]}')

```

    p=4, k=4
    X is in GPU = False
    Explained variance ratio (first two components): tensor([4.2282, 0.2427, 0.0782, 0.0238])
    
    
    PCA basis=tensor([[-0.3614,  0.0845, -0.8567, -0.3583],
            [-0.6566, -0.7302,  0.1734,  0.0755],
            [-0.5820,  0.5979,  0.0762,  0.5458],
            [ 0.3155, -0.3197, -0.4798,  0.7537]])


Let's now project the flowers (originally in 4 dimensions: sepal length, sepal width, petal length and petal width) into two dimension using PCA: 


```python
%matplotlib inline
plt.figure()
colors = ['navy', 'turquoise', 'darkorange']
lw = 2

y = iris.target
target_names = iris.target_names

for color, i, target_name in zip(colors, [0, 1, 2], target_names):
    # Projects all data for a given color into the two new bases
    x_1 = iris_data[y==i,:].float() @ PCA_output["components"][0]
    x_2 = iris_data[y==i,:].float() @ PCA_output["components"][1]
    # Draw output points
    plt.scatter(x_1, x_2, color=color, alpha=.8, lw=lw, label=target_name)
    
plt.legend(loc='best', shadow=False, scatterpoints=1)
plt.title('PCA of IRIS dataset')

```




    Text(0.5, 1.0, 'PCA of IRIS dataset')




    
![png](PCA_linear_algebra_files/PCA_linear_algebra_42_1.png)
    


How much do these two dimensions explain the variance in the data?



```python
x = range(0,PCA_output['explained_variance'].shape[0])
y = PCA_output['explained_variance'] #The amount of variance explained by each of the selected components.
plt.bar(x, y)
#plt.xlabel('x axis label')
plt.ylabel('variance',size=16)
plt.title('PCA',size=18)
labels = ['Component 1', 'Component 2', 'Component 3', 'Component 4']

x_pos = [float(i)-0.3 for i in x]
plt.xticks(x_pos, labels, rotation=45,size=16)
```




    ([<matplotlib.axis.XTick at 0x14634caf0>,
      <matplotlib.axis.XTick at 0x14634cac0>,
      <matplotlib.axis.XTick at 0x14634c9a0>,
      <matplotlib.axis.XTick at 0x1463827c0>],
     [Text(-0.3, 0, 'Component 1'),
      Text(0.7, 0, 'Component 2'),
      Text(1.7, 0, 'Component 3'),
      Text(2.7, 0, 'Component 4')])




    
![png](PCA_linear_algebra_files/PCA_linear_algebra_44_1.png)
    


# (Extra) Independent Component Analysis (ICA)

Given a $p$-dimensional vector ${\bf x} \in \mathbb{R}^p$, find a matrix ${\bf H} \in \mathbb{R}^{p\times k}$ and a vector ${\bf s}\mathbb{R}^k$ such that $${\bf x} = {\bf H} {\bf s}$$ and ${\bf s}$ has mutually statistically independent components ${\bf s}_i$

- Known as "blind source separation" problem or "cocktail party problem"
