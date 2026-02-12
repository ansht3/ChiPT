# CS37300 - Data Mining and Machine Learning
### Instructor & Copyright: Bruno Ribeiro
### Notes: Bruno Ribeiro

## Learning Objectives
In this lecture, we will cover:
1. Review least squares regression.
2. Least squares knowledge representation.
3. Least squares score.
4. Least squares search.
5. Recursive least squares

# Linear Regression Familiarity Quiz  

Please select the option that best describes your familiarity with **linear regression**:  

**(a)** I am familiar with linear regression and can explain its key concepts (e.g., least squares, optimization).  

**(b)** I have seen linear regression before but need a refresher on its mechanics and applications.  

**(c)** I have no prior exposure to linear regression.  


### Notation
1. Bold letters ${\bf a}$ are vectors
2. Bold capital letters ${\bf X}$ are matrices.
3. Lower case letters $y, x$ are observations.
4. Capital letters $X$, $Y$ will be random variables.
5. $\langle {\bf a},{\bf b}\rangle$ is the inner product between ${\bf a}$ and ${\bf b}$.
6. $\|\mathbf{a} - \mathbf{b}\|_2^2$ is the L2 norm of the difference between vectors ${\bf a}$ and ${\bf b}$, i.e., $\|\mathbf{a} - \mathbf{b}\|_2^2 = \sum_{i} (\mathbf{a}_i - \mathbf{b}_i)^2$.

## 1. Least Squares Linear Regression Recap

Today we analyze one of the simplest types of hypothesis from data.

- Input data: Column vectors $X \in \mathbb{R}^{p}$ and $Y \in \mathbb{R}^{d}$, where $p,d > 0$.
    - Observations sampled from an unknown distribution $P(X,Y)$
    - We will assume $Y = X^T {\bf W} + b + {\bf e}$, where
        - ${\bf e} \in \mathbb{R}^{d}$ is a multivariate Gaussian with mean zero $(0,\ldots,0)$ and variance $\sigma^2 I$, where $\sigma$ is unknown to us. That is, ${\bf e} \sim \text{Normal}({\bf 0},\sigma^2 I)$.
        - ${\bf W} \in \mathbb{R}^{p \times d}$ is a set of unknown parameters
        - $b \in \mathbb{R}^{d}$ is an unknown parameter
- Task: Predict $Y$ from $X$.

Consider a set of points $\{(y_i,x_i)\}_{i=1}^n$, where $x_i \in \mathbb{R}^{p \times 1}$, $y_i \in \mathbb{R}$ for $i=1,\ldots,n$ representing:
- $y_i \in \mathbb{R}$ can be the stock price at day $i \geq 1$. Note that $y$ is a scalar $d=1$.
- ${\bf x}_i \in \mathbb{R}^p$ are $p$ numerical feature about day $i$ (weather, news, tweets by important people, etc.).

<center><img src="stockprices.jpg" width=40% /></center>

In **matrix form**, the regression over the $(y_1,{\bf x}_1),\ldots,(y_n,{\bf x}_n)$ data can be described as:
$$
{\bf y} = {\bf X'}^T {\bf w} + {\bf e},
$$
where $${\bf X'} = \begin{bmatrix} x_{11} & x_{12} & \ldots & x_{1p} & 1 \\ x_{21} & x_{22} & \ldots & x_{2p} & 1 \\ \vdots &\vdots & \ldots & \vdots & \vdots \\ x_{n1} & x_{n2} & \ldots & x_{np}& 1 \\ \end{bmatrix},$$
or, expanding it:
$$\begin{bmatrix} {y}_1 \\ {y}_2\\ \vdots \\ {y}_n \end{bmatrix}  = \begin{bmatrix} x_{11} & x_{12} & \ldots & x_{1p} & 1 \\ x_{21} & x_{22} & \ldots & x_{2p} & 1 \\ \vdots &\vdots & \ldots & \vdots & \vdots \\ x_{n1} & x_{n2} & \ldots & x_{np}& 1 \\ \end{bmatrix}  \cdot \begin{bmatrix} w_1 \\ w_2\\ \vdots \\ w_p  \\ w_{p+1} \end{bmatrix} + \begin{bmatrix} e_1 \\ e_2\\ \vdots \\ e_n \end{bmatrix},$$
where $b = w_{p+1}$ and $e_i \sim \text{Normal}(0,\sigma^2)$ are sampled independently for all $i=1,\ldots,n$.

#### Statistical assumption
The equations above relate to the original target variables $y_1,\ldots, y_n $ as:
$$
{\bf y} = {\bf X'}^T {\bf w} + {\bf e},
$$
where 
- $${\bf y} = \left[ \begin{array}{cccc} {y}_1 \\ {y}_2\\ \vdots \\ {y}_n \end{array} \right].$$
- ${\bf e}$ a zero-mean multivariate Gaussian noise with covariance matrix $\sigma^2 I$, that is, ${\bf e} \sim \text{Normal}({\bf 0},\sigma^2 I)$, where $I$ is a $n \times n$ identity matrix and
- $\sigma$ is an unknown value that **we will NOT try to estimate**. That is, $\sigma$ is not a parameter of our model for now.

### 1.1. Least-Squares Linear Regression
- Goal: fit slope and intercept so that the linear regression fit (here: "line") minimizes the sum of the square of the residuals (vertical offsets or distances)

<img src="linear_regression.png" width="450" />

#### Review of Classical Least-squares Regression

Let's first refresh the classical linear regression task.

Consider a set of points $\{(y_i,x_i)\}_{i=1}^n$, where $x_i \in \mathbb{R}^{p \times 1}$, $y_i \in \mathbb{R}$ for $i=1,\ldots,n$. 

In linear regression we want to approximate $y_i$ with 
$$
\hat{y}_i =  {\bf x}_i^T \hat{\bf w}  + \hat{b}
$$
where $\hat{\bf w}$ is a column vector and  $\hat{b}$ is a scalar such that
$$\hat{\bf w},\hat{b}= \arg\!\min_{{\bf w},b}   \sum_{i=1}^{n} \big(y_i - \hat{y}_i\big)^2 = \arg\!\min_{{\bf w},b}  \sum_{i=1}^{n} \big(y_i -  {\bf x}_i^T {\bf w} - b \big)^2$$

We can already make one simplification:
$$ {\bf x}'_i = \begin{bmatrix}{\bf x}_i\\1\end{bmatrix}, \quad i=1,\ldots,n $$
Now we are only looking for ${\bf w} \in \mathbb{R}^{p+1}$:
$$\hat{\bf w} =  \arg\!\min_{\bf w}  \sum_{i=1}^{n} \big(y_i -  {\bf x'}_i^T {\bf w}\big)^2 = \arg\!\min_{\bf w} \|\mathbf{y} - \mathbf{X'}^T \mathbf{w}\|_2^2,$$
where ${\bf X'}$ is an $n\times (p+1)$ matrix where all the rows are the data examples:
$$
{\bf X'} = \begin{bmatrix}{\bf x}'_1 \\ \vdots \\ {\bf x}'_n \end{bmatrix},
$$
and the target variables ${y}_1,\ldots,{y}_n$ are also arranged in vector form:
$$
{\bf y} = \begin{bmatrix} y_1 \\ \vdots \\ y_n \end{bmatrix}.
$$

## 2. Knowledge representation: Least-squares Error is a Negative Log-Likelihood Score

The above model can be interpreted as a **multivariate Gaussian**
- The output vector $\mathbf{y}$ is modeled as a linear function of the input data $\mathbf{X}'$ with additive Gaussian noise ${\bf e}$. 
    - That is, each dimension value $y_i$ is a linear combination of the input features $\mathbf{x}_i$ weighted by $\mathbf{w}$, plus noise ${\bf e}_i \sim \mathcal{N}(0, \sigma^2)$. 
    - The model assumes the conditional distribution of $\mathbf{y}$, given $\mathbf{x}'$, follows a multivariate Gaussian distribution:
$$
\mathbf{y} \mid \mathbf{X}', \mathbf{w}, \sigma^2 \sim \text{Normal}(\mathbf{X'}^T \mathbf{w}, \sigma^2 \mathbf{I}),
$$
where $\mathbf{I}$ is the identity matrix and $\sigma^2$ represents the noise variance.
- **This assumes $y_1,\ldots,y_n$ are independent.**

### 2.1. Linear regression score: Negative Log-Likelihood Function

The likelihood using the above multivariate Gaussian density is:
$$
p(\mathbf{y} \mid \mathbf{X}', \mathbf{w}, \sigma^2) = \frac{1}{(2\pi\sigma^2)^{n/2}} \exp\left(-\frac{1}{2\sigma^2} \|\mathbf{y} - \mathbf{X'}^T \mathbf{w}\|_2^2\right)
$$

The log-likelihood for the multivariate Gaussian distribution of $\mathbf{y}$ is:
$$
\log p(\mathbf{y} \mid \mathbf{X}', \mathbf{w}, \sigma^2) = -\frac{n}{2} \log(2\pi\sigma^2) - \frac{1}{2\sigma^2} \|\mathbf{y} - \mathbf{X'}^T \mathbf{w}\|_2^2.
$$
To obtain the negative log-likelihood, we simply negate this expression:
$$
-\log p(\mathbf{y} \mid \mathbf{X}', \mathbf{w}, \sigma^2) = \frac{n}{2} \log(2\pi\sigma^2) + \frac{1}{2\sigma^2} \|\mathbf{y} - \mathbf{X'}^T \mathbf{w}\|_2^2.
$$

Since we do not care for $\sigma$, as it is not a parameter in our model, we want ot find  
$$\hat{\bf w} =  \arg\!\min_{\bf w} \|\mathbf{y} - \mathbf{X'}^T \mathbf{w}\|_2^2,$$
which is **the same as the least-squares objective.**

## Quiz

With respect to ${\bf w}_1$, is the linear regression score $$ \sum_{i=1}^{n} \big(y_i -  x_{i,1} {\bf w}_1 - x_{i,2} {\bf w}_2 - b \big)^2$$

- (a) Concave
- (b) Convex
- (c) Neither

1. Hint 1: Collapse all terms that don't depend or multiply ${\bf w}_1$ into a single constant $c_i$: $\frac{1}{n} \sum_{i=1}^{n} \big(c_i -  x_{i,1} {\bf w}_1 \big)^2$.
2. Hint 2: Compute the second derivative of the above score with respect to ${\bf w}_1$.

### 2.2. Search: Maximum Likelihood Estimate in Closed-form

Since ${\bf X'}^T$ may not be invertible (and may not even be a square matrix), solving for ${\bf w}$ needs to resort to ${\bf X'}^+$, which is the pseudo-inverse (Moore–Penrose inverse) of ${\bf X'}^T$:
$$ \hat{\bf w}= {\bf X'}^+ {\bf Y} = ({\bf X'} {\bf X'}^T)^{-1}({\bf X'}^T {\bf y}),$$
which requires to **store all the $n$ data points**.

- Often $n$ is much too large to store
- Or the data comes in a streamming fashion (e.g., every millisecond) the linear regression too expensive to be redone at each new data point

### (Extra) Derivation of pseudo-inverse solution
The derivation of pseudo-inverse solution needs vector calculus.

$$\hat{\bf w} = \arg\!\min_{{\bf w}}  \frac{1}{n} \sum_{i=1}^{n} \big(y_i -  ({\bf x}')_i^T {\bf w} \big)^2 = \arg\!\min_{{\bf w}}  ({\bf y} - {\bf X}'^T {\bf w})^T ({\bf y} - {\bf X}'^T {\bf w}) $$

Since score is convex, equating the derivatives to zero gives our solution:
$$\begin{align*}{\bf 0} &= \frac{\partial}{\partial {\bf w}} ({\bf y} - {\bf X}'^T {\bf w})^T ({\bf y} - {\bf X}'^T {\bf w}) \\
&= \frac{\partial}{\partial {\bf w}} ({\bf y}^T {\bf y} - 2 {\bf w}^T {\bf X'}^T {\bf y} + {\bf w}^T {\bf X'}^T {\bf X'} {\bf w}) \\
&= -2{\bf X'}^T {\bf y} + 2 {\bf X'}^T {\bf X'} {\bf w}\end{align*}$$

Hence, $$ \hat{\bf w}=({\bf X'} {\bf X'}^T)^{-1}({\bf X'}^T {\bf y}).$$



### Example of standard least squares regression


```python
### Example

import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
%matplotlib inline

rng = np.random.RandomState(123)
mean = [100, 1000]
cov = [[1, 0.9], [0.9, 1]]
sample = rng.multivariate_normal(mean, cov, size=100)
x, y = sample[:, 0], sample[:, 1]

plt.scatter(x, y)
plt.xlabel('x')
plt.ylabel('y')
plt.show()
```


    
![png](linear_regression_files/linear_regression_18_0.png)
    



```python
X = x[:, np.newaxis]

# adding a column vector of "ones" to X as its last column
Xb = np.hstack((X,np.ones((X.shape[0], 1))))

# Gets w by computing the pseudo-inverse of X and multiply it by y
w = np.linalg.inv(Xb.T @ Xb) @ Xb.T @ y

b, w1 = w[1], w[0]
print('slope: %.2f' % w1)
print('y-intercept: %.2f' % b)

extremes = np.array([np.min(x), np.max(x)])
predict = extremes*w1 + b

plt.plot(x, y, marker='o', linestyle='')
plt.plot(extremes, predict)
plt.xlabel('x')
plt.ylabel('y')
plt.show()
```

    slope: 0.84
    y-intercept: 915.59



    
![png](linear_regression_files/linear_regression_19_1.png)
    


## 3. Feature Selection in Regression

* Suppose ${\bf x}_i = [0,80,3,4,\ldots]^T$ is a 50,000 dimensional column vector where
    * ${\bf x}_{ij}$ is the frequency of word $j$ in product review $i$
        * For instance, j = 1 is the word “good”, j = 2 is the word “product”
    * The task is to predict a star rating for the review ($y \in \{1,2,3,4,5\}$ stars)
* Then the regression parameters are: The coefficients ${\bf w} \in \mathbb{R}^{50000\times 1}$ and the bias $b \in \mathbb{R}$
    * The model outputs $f({\bf x}) = {\bf x}^T {\bf w} + b$.
    
* Note that most words do not matter for predicting the star review
    * Words like "bad", "good", "best" matter a lot.
    * Words like "box" and "grass" do not matter as much

### 3.1. Feature Selection Task

* Training data: ${\bf X},{\bf y}$
* Given an $n\times p$ table with $n$ reviews in a vocabulary of $p$ words: 
$${\bf X} = \begin{bmatrix} {\bf x}_{1,1} & {\bf x}_{1,2} & \cdots & {\bf x}_{1,p} \\ 
 {\bf x}_{2,1} & {\bf x}_{2,2} & \cdots & {\bf x}_{2,p} \\ 
     \vdots & \vdots & \ddots & \vdots \\ 
 {\bf x}_{n,1} & {\bf x}_{n,2} & \cdots & {\bf x}_{n,p} \\ 
     \end{bmatrix}$$
* Given an $n \times 1$ table with $n$ review ratings $$ {\bf y} = \begin{bmatrix} y_1\\ y_2 \\ \vdots \\ y_n      \end{bmatrix}$$

* **Goal:** Find the features (columns) of ${\bf X}$ that are important for predicting ${\bf y}$

### 3.2. Naive Approach
- A simple/common way to do feature selection:
    - For each feature $j$, compute empirical correlation between feature values in column vector ${\bf X}_{\cdot,j}$ and the vector ${\bf y}$.
    - We will say that ‘j’ is relevant if correlation is above a threshold $t$ or below $-t$
    - Usually gives unsatisfactory results as it ignores variable interactions:
        - Includes irrelevant variables: “Excruciating Pain”
        - If pain is associated with bad review, it will say "excruciating" is associated with bad review, while excruciating is really just associated with "pain"
    - Excludes relevant variables: “Diet Coke + Mentos”
        - Diet coke and Mentos are not remarkable on their own, but together they can explode.

### 3.3. A Regression Approach to Feature Selection

- A simple/common approach to feature selection:
    - Fit regression weights ${\bf w}$ based on all features using **L1 regularization** (we will come back to this later)
    - Take all features $j$ where weight ${\bf w}_j$ is greater than a threshold

- For example: you fit a least squares model with 5 (normalized) features and get: $$ {\bf w} = \begin{bmatrix} 0.01\\ -0.4 \\ 11 \\ -0.7 \\ 0.0001  \\ b   \end{bmatrix}$$
    - Feature $j=3$ looks the most relevant, while feature $j=5$ seems irrelevant

#### 3.3.1. Standardization: Dealing with Features in Different Scales
- Consider continuous features with different scales:
    - Word “the” appears 100 times in review
    - Word “bad” appears only once in review
    - Should we convert to some standard ‘unit’?
    - It is common to standardize continuous features.
    - For each feature $j$:
        1. Compute empirical mean $\hat{\mu}_j$ and standard deviation $\hat{\sigma}_j$ of column $j$ of ${\bf X}$ (${\bf X}_{\cdot,j}$)
        2. For all $i$, compute the standardized feature value: ${\bf X}_{i,j} \leftarrow ({\bf X}_{i,j} - \hat{\mu}_j)/\hat{\sigma}_j$
- **Important:** Remeber to standardized the test with the same $\hat{\mu}_j$ and $\hat{\sigma}_j$ used in training before applying the regression

#### 3.3.2. Changing the Score to Prefer Solutions with Fewer Features
- We can achieve the above using a penalty in our score:
$$\hat{\bf w},b =  \arg\!\min_{\bf w}  \sum_{i=1}^{n} \big(y_i -  {\bf x'}_i^T {\bf w}\big)^2 + \frac{1}{\lambda} K ,$$
where $K$ is the number of non-zero values in ${\bf w}$, $\lambda > 0$.

- This penalty $K$ is often also denoted as  
$$\hat{\bf w},b =  \arg\!\min_{\bf w}   \sum_{i=1}^{n} \big(y_i -  {\bf x'}_i^T {\bf w} \big)^2 + \frac{1}{\lambda} \Vert {\bf w}\Vert_0 ,$$
where $\Vert {\bf w} \Vert_0$ is the $L_0$ “norm”, the number of non-zero values in ${\bf w}$
    - Not actually a true norm
    - If ${\bf w}$ has a small $L_0$-norm, then it doesn’t use many features
    - Hard to optimize since it is not continuous

### 3.3.3. $L_1$-regularization: Alternative to $L_0$ penalty

- An alternative to $L_0$ regularization is the $L_1$ regularization
$$\hat{\bf w},b =  \arg\!\min_{\bf w}  \frac{1}{n} \sum_{i=1}^{n} \big(y_i -  {\bf x'}_i^T {\bf w} + b\big)^2 + \frac{1}{\lambda} \Vert {\bf w}\Vert_1 ,$$
where $\Vert {\bf w} \Vert_1 = \sum_{j=1}^p |{\bf w}_j|$ and $|a|$ is the absolute value of $a$, and $\lambda > 0$.
- Like the $L_0$-norm, it encourages elements of ${\bf w}$ to be exactly zero
- The regularization is convex (barely) and generally improves our test error
- $L_1$-regularization simultaneously regularizes and selects features
- $L_1$-regularized linear regression is also known as **“LASSO” regression**.

### 3.3.4. $L_2$-regularization

- An alternative to $L_1$ and $L_0$ regularizations is the $L_2$ regularization
$$\hat{\bf w},b =  \arg\!\min_{\bf w}  \frac{1}{n} \sum_{i=1}^{n} \big(y_i -  {\bf x'}_i^T {\bf w} + b\big)^2 + \frac{1}{\lambda} \Vert {\bf w}\Vert_2^2 ,$$
where $\Vert {\bf w} \Vert_2^2 = \sum_{j=1}^p ({\bf w}_j)^2$ and $\lambda > 0$.

- Unlike $L_1$-regularization, it will not find many zero values of ${\bf w}$.
    - It will find values of $\Vert {\bf w} \Vert_2$ that are small, which means that ${\bf w}$ is in the surface of a small hypersphere
    - This also “simplifies” the model, since we are looking for models inside small hyperspheres. But it is less effective than $L_1$-regularization at feature selection
    - $L_2$-regularized linear regression is also known as ridge regression

## 4. (Advanced) But what if we can't store all the data?
- Assume data arrives over time, but we can't store it
- How can we do the same regression?

### 4.1. Recursive Least Squares Regression

Consider a stream of data points $({\bf x}_1,y_1),\ldots,({\bf x}_t,y_t),\ldots,({\bf x}_n,y_n)$.

At time $t \in \{1,\ldots,n\}$, 
let 
$$
{\bf X}_t = \left[ \begin{array}{cccc} x_{11} & x_{12} & \ldots & x_{1p} & 1 \\ x_{21} & x_{22} & \ldots & x_{2p} & 1 \\ \vdots &\vdots & \ldots & \vdots & \vdots \\ x_{t1} & x_{t2} & \ldots & x_{tp}& 1 \\ \end{array} \right] 
$$
with
$$\Phi_t = {\bf X}_t {\bf X}_t^T$$ and $$\theta_t= {\bf X}_t {\bf y}$$.

The original least squares solution with all the data is $$\hat{\bf w} = \Phi_n^{-1} \theta_n.$$

### 4.2. Original Least Square is not Scalable
- Matrix ${\bf X}$ grows over time and needs matrix inversion
- $O(n  p^2 + p^3)$ computation

- $O(n p)$ storage 
    - Time series example: Measured every millisecond, a **single** time series will produce 4.32e+8 data points in 5 days
        - For $p=1$, ${\bf X}$ requires 1.6 TB of RAM memory if stored in FP32 or int32 (4 bytes)
        - For $p=1000$, ${\bf X}$ requires 1600 TB = 1.6PB of RAM memory if stored in FP32 or int32 (4 bytes)

### 4.3. Recursive Least Squares Solution

Now, let's write $\Phi_{t+1}^{-1}$ as a function of
- $\Phi_{t}^{-1}$ the previous inverse of $\Phi_{t}$,  and 
- ${\bf x}_{t+1}$: the new data item $t+1$ 

Note that $$\Phi_{t+1}  = \Phi_t + {\bf x}_{t+1}{\bf x}^T_{t+1}.$$ 

We can now use the [Sherman–Morrison](https://en.wikipedia.org/wiki/Sherman%E2%80%93Morrison_formula) (1949) formula for the update:

$$
(\Phi_t + {\bf x}_{t+1}{\bf x}^T_{t+1})^{-1} = \Phi_t^{-1} - \frac{\Phi_t^{-1}{\bf x}_{t+1}{\bf x}^T_{t+1}\Phi_t^{-1} }{1 + {\bf x}^T_{t+1}\Phi_t^{-1}{\bf x}_{t+1}},
$$
noting that
$$
\Phi_{t+1}^{-1} = (\Phi_t + {\bf x}_{t+1}{\bf x}^T_{t+1})^{-1}.
$$

Also note that
$$
\theta_{t+1} = \theta_t + {\bf x}^T_{t+1} y_{t+1}
$$

Finally, we obtain
$$
\hat{\bf w}_{t+1} = \Phi_{t+1}^{-1} \theta_{t+1}.
$$

We can use the above formula to compute least squares recursivelly:
- At each new data point ${\bf x}_{t+1}$, we compute $\Phi_{t+1}^{-1}$ and $\theta_{t+1}$ and keep these values.
    - $\Phi_{t+1}^{-1}$ is a $p \times p$ matrix (if $t \gg p$, $\Phi_{t+1}^{-1}$ is a lot smaller than ${\bf X}$)
    - $\theta_{t+1}$ is a $1 \times p$ vector.
- We can now throw ${\bf x}_{t+1}$, $y_{t+1}$, away. We don't need them for the regression anymore.
- $\hat{\bf w}_{t+1}$ is the correct linear regression parameters for all the observed data up to time $t+1$.
    - After we see all $n$ items, we will have $\hat{\bf w} = \hat{\bf w}_n$ of our original least squares problem.

### 4.4. Recursive LS Complexity

**Original Least Squares (LS) not scalable:**
- Matrix ${\bf X}$ grows over time and needs matrix inversion
- $O(n  p^2 + p^3)$ computation
- $O(n p)$ storage

**Recursive Least Squares (RLS):**
- Storage: Need much smaller, fixed size matrix and vector $O(p^2)$
- Fast, incremental computation $O(p^2)$ (at each step) and no matrix inversion
    - The total computing time will still be $O(n p^2)$
    - Drawback is precision. Error in earlier inverse will propagate to later ones.
