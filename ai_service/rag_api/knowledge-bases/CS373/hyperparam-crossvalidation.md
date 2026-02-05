# CS37300 - Data Mining and Machine Learning
### Instructor: Bruno Ribeiro
### Notes: Bruno Ribeiro and Bonan Kou

# Model Selection Concepts (Part 1)


## Learning Objectives
In this lecture, we will cover:
1. Empirical evaluation of models
2. **Hyperparameter search with cross-validation.**
3. Testing model performance.
4. Working with data in python.
5. Featurizing a dataset for k-NN

## Empirical Evaluation

* How well does observed accuracy generalize to new data?
* If one model outperforms another on some sample, is it better in general?
* With limited data, how should we best use it to **both learn and evaluate** a model?

## Validation & Test Data
<center><img src="validationtest.png"/></center>

## Evaluating Classifiers

* Goal: Estimate model's **true error** on new data.
* Challenge: limited data.

### Evaluation Approach??

Testing a classifier on the **training data** can be misleading, since it does not measure generalization.

## Quiz 1:

* Between $k$-NN with $k=1$ and $k=15$, which one would appear to perform **best if evaluated only on the training set**?

(a) $k=1$

(b) $k=15$

Answer: Always (a), but that is misleading since the error in new data may be really bad.


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
for ax, k in zip(axs, [None, 1, 15]):
    plot_panel(ax, k)
plt.tight_layout(); plt.show()
```


    
![png](hyperparam-crossvalidation_files/hyperparam-crossvalidation_7_0.png)
    



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


# Overfitting

## Definition
**Overfitting occurs when a model learns the training data too well, including noise and irrelevant patterns, leading to poor generalization.**

## Formal Setup
- **True distribution**: $D$ (unknown)
- **Training sample**: $D_S \subset D$ (finite sample we observe)
- **Model space**: $M$ (set of possible models)
- **Learning algorithm**: Returns model $m \in M$
- **Score function** $S(m, D')$: performance of model $m$ on data $D'$ (higher = better)

## Mathematical Characterization
Model $m$ overfits relative to model $m'$ if:
$$S(m, D_S) > S(m', D_S) \quad \text{but} \quad S(m, D) < S(m', D)$$

**Interpretation**: 
- $m$ performs better on training data
- $m'$ would perform better on the true distribution (unseen data)

## Key Intuition
- **Training performance**: How well the model fits the observed data
- **Generalization gap**: Difference between training and true performance
- **Overfitting**: Large generalization gap due to memorizing training-specific patterns

## Visual Example: Decision Boundaries
<center><img src="boundary.png" width=400px/></center>

- **Black curve**: Appropriate model complexity
- **Green curve**: Complex boundary following noise (overfitting)

## Practical Implications
- More complex models are more prone to overfitting but tend to have lower training error (bias($E_\text{train}$)-variance($E_\text{approx}$) trade-off)
    - Overfitting becomes worse with smaller training sets
- Small models are less prone to overfitting but have large training errors (bias($E_\text{train}$)-variance($E_\text{approx}$) trade-off)
- Hyperparameter search helps prevent overfitting while keeping bias (training error small)


## Generalization Error

* Gap between **training performance** vs **test performance**.
* Generalization gap = \$E\_\text{test} - E\_\text{train}\$.
* Caused by limited data, complex models.

## Learning Theory

* Expected train error \$E\_\text{train}\$
* Expected test error \$E\_\text{test}\$

$$
E_\text{test} = (E_\text{test} - E_\text{train}) + E_\text{train}
$$

* **Decomposition**:
  * $E_\text{approx} = (E_\text{test} - E_\text{train})$: approximation error
  * $E_\text{approx}$ shows the amount of overfitting. 
     * Overfitting depends on data size & model complexity.

- Why is this decomposition useful?
    - If $E_\text{approx}$ is small, then $E_\text{train}$ is a good approximation to $E_\text{test}$.
    - What does $E_\text{approx}$ (“amount of overfitting”) depend on?
        - It tends to get smaller as amount of data gets larger.
        - It tends to grow as model get more “complicated” (e.g., $K=1$ (complex) in kNN vs $K=15$ (simpler)).

## Trade-Off

* Small models (large $K$ for kNNs): \$E\_\text{train}\$ high, \$E\_\text{approx}\$ low.
* Complex models (small $K$ for kNNs): \$E\_\text{train}\$ low, \$E\_\text{approx}\$ high.
* Test error curve: U-shape vs model complexity.

## Evaluation Approach 1: Learning Curves

* Sample subsets of training data.
* Train models, evaluate on train/validation.
* Plot accuracy vs training set size.


- Learning curve plot
    - **x-axis:** Amount of training data
    - **y-axis:** Error/Accuracy metric

Insights:

* Training accuracy upper-bounds validation/test.
* Gap = generalization error.
<center><img src="learningcurve1.png" witdh=300px/></center>
* B = training data
* A = test data

### 1.1. Learning Curve Relationship with $E_\text{approx}$
- Let y-axis be accuracy
- x-axis is the amount of training data
- For a given amount of training data (`training data size`), the gap between the two curves shows 
    - $E_\text{approx} = (1 - \text{Accuracy}_\text{Test}) - (1 - \text{Accuracy}_\text{Train}) = \text{Accuracy}_\text{Train} - \text{Accuracy}_\text{Test}$


<center><img src="learningcurve3.png" witdh=300px/></center>

<center><img src="learningcurve2.png" witdh=300px/></center>

## Bias-Variance Trade-Off

* As data increases: \$E\_\text{approx} \downarrow\$.
* Small data: variance dominates.
* kNN for $K$ large → high bias, low variance.
* kNN for $K$ small → low bias, high variance.

## Avoiding Overfitting

* Regularization (Laplace correction, penalty terms). 
    - We will see these later in the course
* Hold-out validation sets.
* Pre/post pruning in decision trees.
* Statistical significance tests.

## Evaluation Approach 2: Hold-Out Test

* Partition dataset into **train/test** (disjoint).
* Estimate error only once.
* Do not reuse test set for model tuning!

## Cross-Validation (CV)

* Partition training data into \$k\$ folds.
* Train on \$k-1\$ folds, test on 1 fold.
* Repeat \$k\$ times, average results.
* Eliminates dependency from overlapping test sets.

Applications:

* Hyperparameter tuning.
* Empirical model comparison.

## Full ML Process

1. Data input & representation.
2. Train/validation/test split.
3. Feature construction.
4. Learn model (e.g., kNN, Naive Bayes).
5. Apply model.
6. Evaluate predictions on validation data (0/1 loss, squared loss).
7. Repeat 3 with change of hyperparameters if needed
8. Evaluate predictions on test data (0/1 loss, squared loss).

## Key Rule of ML

* Test data cannot influence model selection.
* Never change test set to obtain better results.
* Same principle applies to hypothesis testing in science.

## Quiz 2

What contributes to prediction error on test data?

* (A) Model bias (\$E\_\text{train}\$)
* (B) Model variance / generalization gap (\$E\_\text{approx}\$)
* (C) Both A and B

## Putting It All Together

### Task in our example

- Ad placement based on user's age, salary, and location (Indiana or Hawaii). 
- We can only post one ad per user. 
    - There are six brands to choose from:
        1. Work Boots: Affordable, durable boots designed for everyday work and practical use.
        2. Designer Boots: Expensive and trendy boots that follow the latest fashion trends.
        3. Vintage Leather Boots: Expensive, high-quality boots with a classic, retro style that never goes out of fashion.
        4. Basic Sunglasses: Affordable, everyday sunglasses designed for casual use.
        5. Fashion Sunglasses: Expensive and trendy sunglasses that follow the latest fashion trends.
        6. Retro Sunglasses: Expensive, high-quality sunglasses with a classic, vintage design.

### Data preparation
- Our first step is to read the training data. 
    - We are given two files, `train.csv` and `test.csv`, containg the train and test data respectively. 
    
- First, let's inspect the data.


```python
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

train = pd.read_csv("train.csv")
train.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Age</th>
      <th>EstimatedSalary</th>
      <th>State</th>
      <th>Product</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>42</td>
      <td>117456</td>
      <td>Hawaii</td>
      <td>Basic Sunglasses</td>
    </tr>
    <tr>
      <th>1</th>
      <td>36</td>
      <td>101269</td>
      <td>Indiana</td>
      <td>Work Boots</td>
    </tr>
    <tr>
      <th>2</th>
      <td>44</td>
      <td>71775</td>
      <td>Hawaii</td>
      <td>Basic Sunglasses</td>
    </tr>
    <tr>
      <th>3</th>
      <td>53</td>
      <td>47683</td>
      <td>Indiana</td>
      <td>Work Boots</td>
    </tr>
    <tr>
      <th>4</th>
      <td>35</td>
      <td>93549</td>
      <td>Indiana</td>
      <td>Work Boots</td>
    </tr>
  </tbody>
</table>
</div>



### Feature normalization
We notice that EstimatedSalary and Age have different ranges. In order to build KNN model, we need to normalize these two features. An easy way to do it, is to calculate the mean and standard deviation for each feature in our training data. If $X_k$ is the value of feature $k$, we will apply the z-score formula to normalize the data:
$$
Z_k = \frac{X_k - \hat{\mu}_k}{\hat{\sigma}_k},
$$
where $\hat{\mu}_k \approx E[X_k]$ is the empirical average of $X_k$ in our training data, and $\hat{\sigma}_k \approx \sqrt{E[(X_k-E[X_k])^2]}$ is the empirical standard deviation of $X_k$ in the training data.

We must save the normalization used in training to apply that to the test examples.
- **VERY IMPORTANT**: The test data MUST be normalized according to the normalization used in training (mean and standard deviation of the **training data**).


```python
def data_normalization(data, train_normalization=None):
    """
    Normalizes the 'Age' and 'EstimatedSalary' columns of the input data to have zero mean and unit variance.

    This function is designed to standardize the 'Age' and 'EstimatedSalary' features in a dataset.
    If normalization parameters (mean and standard deviation) are not provided, it calculates them
    from the input data. If the normalization parameters *are provided* (e.g., taken from the training dataset), 
    they are applied to the input data to ensure consistent scaling between training and test sets.

    Parameters:
    -----------
    data : pandas.DataFrame
        The data containing 'Age' and 'EstimatedSalary' columns to be normalized.

    train_normalization : dict or None, default=None
        A dictionary containing the mean and standard deviation used for normalization. Expected keys
        are 'age_mean', 'age_std', 'salary_mean', and 'salary_std'. If None, the function calculates these
        values from the input data.

    Returns:
    --------
    data : pandas.DataFrame
        The normalized data where the 'Age' and 'EstimatedSalary' columns have zero mean and unit variance.

    train_normalization : dict
        A dictionary containing the mean and standard deviation used for normalization. This can be stored
        and used later to normalize other datasets (e.g., a test set) in the same way as the training normalization.
    """
    if not train_normalization:
        train_normalization = {}
        train_normalization['age_mean'] = data['Age'].mean()
        train_normalization['age_std'] = data['Age'].std()
        train_normalization['salary_mean'] = data['EstimatedSalary'].mean()
        train_normalization['salary_std'] = data['EstimatedSalary'].std()
    data['Age'] = (data['Age'] - train_normalization['age_mean']) / train_normalization['age_std']
    data['EstimatedSalary'] = (data['EstimatedSalary'] - train_normalization['salary_mean']) / train_normalization['salary_std']
    return data,train_normalization

# Return the normalized training data, along with the normalization dictionary of the mean and standard deviations
train,train_normalization = data_normalization(train)

```

#### Converting categorical data
- Because the computer cannot compute a distance between the strings `Hawaii` and `Indiana`, we need to convert these categorical features into numbers. 
    - For instance, we will assign 0 to "Hawaii" and 1 to "Indiana".


```python
state_mapping = {'Hawaii': 0, 'Indiana': 1}
train['State'] = train['State'].map(state_mapping)
train.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Age</th>
      <th>EstimatedSalary</th>
      <th>State</th>
      <th>Product</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.465614</td>
      <td>1.388795</td>
      <td>0</td>
      <td>Basic Sunglasses</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-0.140391</td>
      <td>0.885692</td>
      <td>1</td>
      <td>Work Boots</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.667616</td>
      <td>-0.031002</td>
      <td>0</td>
      <td>Basic Sunglasses</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1.576623</td>
      <td>-0.779799</td>
      <td>1</td>
      <td>Work Boots</td>
    </tr>
    <tr>
      <th>4</th>
      <td>-0.241392</td>
      <td>0.645749</td>
      <td>1</td>
      <td>Work Boots</td>
    </tr>
  </tbody>
</table>
</div>



## 1. Cross-validation: Splitting the dataset into train and validation for hyperparameter search
- Note that to find the best model in k-NNs we must perform a search over
    - $k$ - the number of neighbors
    - $d$ - the distance measure
    - $g$ - the label summarization function
- Since this search is over a discrete search space
    - We need to perform `hyperparameter search`, which is a search over discrete model parameters.
    - In order to perform this hyperparameter search, we need to **split the training data into a `train` and a `validation` datasets**.
- Since the `test.csv` data should be reserved for evaluating the final model:
    - We will split the train data into a `train` and `validation` sets. 
    - Below we split `train.csv` into 80% for `train` and 20% for `validation`.
    - This split is `pseudorandom`, that is, `random_state` determines the random seed used to split the data.
        - Ensure we always split the same way if we ran the code multiple times.
    - Random splits are important since training and validation data must have the same distribution 
        - That is, if the file is ordered in some way (e.g., all ads for sunglasses come at the end of the file) splitting the file into the first 80% entries and the bottom 20% entries would not have the same distribution


```python
from sklearn.model_selection import train_test_split

X = train.drop(columns=['Product'])
y = train['Product']

X_train, X_validation, y_train, y_validation = train_test_split(X, y, test_size=0.2, random_state=4)

print('Train set:', X_train.shape, y_train.shape)
print('Validation set:', X_validation.shape, y_validation.shape)
```

    Train set: (800, 3) (800,)
    Validation set: (200, 3) (200,)


## 2. Hyperparameter search of k-NN model
Now we define our k-NN model. 
- To enable hyperparameter search, our class allows us to define different $k$ values, distance calculation functions $d$, and label summarization functions $g$.


```python
import numpy as np

class NearestNeighbor(object):
    """
    This is a simple implementation of the k-nearest neighbors (KNN) algorithm for classification or regression tasks.
    
    A professional-grade algorithm would use something like k-d trees for faster inference speed.

    This class allows for flexibility in choosing the distance metric, voting strategy, 
    and whether to apply distance-weighted voting. It can be used to make predictions 
    based on the nearest neighbors in the training set.

    Attributes:
    -----------
    K : int
        The number of nearest neighbors to consider for making predictions. Default is 1.

    distance_function : callable
        A function that computes the distance between two points. This can be any 
        distance metric (e.g., Euclidean, Manhattan, etc.).

    vote_function : callable
        A function that determines the final predicted label based on the labels of 
        the nearest neighbors. This can be a simple majority vote or a more complex 
        function, such as distance-weighted voting.

    d_weighted : bool
        A Boolean indicating whether to perform distance-weighted voting. If True, the 
        vote_function will take into account the distances to the neighbors, giving 
        more influence to closer neighbors. Default is False.

    Methods:
    --------
    train(X, y):
        Stores the training data and labels for later use in prediction. 
        The training phase in KNN is just storing the data, as the actual 
        computation happens during prediction.

    predict(X):
        Predicts the labels for the input test data based on the K nearest neighbors 
        in the training set. Uses the specified distance_function to find the nearest 
        neighbors and the vote_function to determine the final prediction. If 
        d_weighted is True, the voting process considers the distances to the neighbors. 
        d_weighted is False, the voting process considers only the majority of the labels, breaking ties arbitrarily. 
    """
    def __init__(self, K=1, distance_function=None, vote_function=None, d_weighted=False):
        self.K = K
        self.distance_function = distance_function
        self.vote_function = vote_function
        self.d_weighted = d_weighted

    def train(self, X, y):
        self.Xtr = X
        self.ytr = y

    def predict(self, X):
        num_test = X.shape[0]
        Ypred = np.zeros(num_test, dtype=self.ytr.dtype)

        for i in range(num_test):
            distances = self.distance_function(self.Xtr, X[i, :])
            nearest_indices = np.argsort(distances)[:self.K]
            nearest_labels = self.ytr[nearest_indices]
            if self.d_weighted:
                Ypred[i] = self.vote_function(nearest_labels, distances[nearest_indices])
            else:
                Ypred[i] = self.vote_function(nearest_labels)
        return Ypred
```

## Quiz 3

Consider 
- $k=1$
- $d$ is the L1 (Manhattan) distance metric
- $g$ makes a label prediction based on majority vote. 
- assume points of different classes don't overlap
    
Mark the only correct answer:

(a) 1-NN is guaranteed to predict test data labels perfectly.

(b) 1-NN is guaranteed to predict training data labels perfectly.

(c) 1-NN is guaranteed to predict training and test data labels perfectly.


The answer is B. For 1-NN, each data point in train set will find a perfect match (itself), thus the perfect performance if points don't overlap.


```python
def manhattan_distance(Xtr, x):
    """
    Computes the Manhattan distance between a set of instances Xtr and a single instance x.

    Parameters:
    Xtr: array-like, shape (n_samples, n_features)
        The set of instances for which the Manhattan distance will be calculated.
    
    x: array-like, shape (n_features,)
        The reference instance from which the Manhattan distance will be measured against.

    Returns:
    distances: array-like, shape (n_samples,)
        The Manhattan distances between each instance in Xtr and the instance x.
    """
    return np.sum(np.abs(Xtr - x), axis=1)

def majority_vote(labels):
    """
    Determine the majority label from a list of labels.

    Parameters:
    labels: array-like, shape (n_samples,)
        A list of labels from which to determine the majority label.

    Returns:
    majority_label:
        The label that appears most frequently in the list.
        If there is a tie, one of the majority labels is returned.
    """
    values, counts = np.unique(labels, return_counts=True)
    return values[np.argmax(counts)]
```


```python
knn = NearestNeighbor(K=1000, distance_function=manhattan_distance, vote_function=majority_vote)
knn.train(X_train.to_numpy(), y_train.values)
prediction = knn.predict(X_validation.values)

print(f'Predictions in validation are: {prediction}')
```

    Predictions in validation are: ['Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots'
     'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots' 'Work Boots']


Why are all the predictions above "`Work Boots`"?

### F1 Score: Evaluating the performance of **binary** classifiers

The F1 score is a metric used to evaluate the performance of a classification model by balancing two important concepts: precision and recall. It is particularly useful when dealing with imbalanced datasets, where one class significantly outnumbers the others.

- **F1 is defined for binary classifiers**: The classes in the definition below are {positive, negative} but could be {0,1}, {True, False}.

- **Harmonic Mean**: The F1 score is calculated as the harmonic mean of precision and recall, providing a single metric that accounts for both false positives and false negatives.
    - If either precision or recall is 0, the F1 score will be 0, indicating the worst possible performance.
    - The best F1 score is 1, indicating perfect precision and recall.

$$
F1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}
$$

### Precision and Recall Definitions

- **Precision** measures how many of the predicted positive instances are actually positive:
$$
\text{Precision} = \frac{\text{True Positives (TP)}}{\text{True Positives (TP)} + \text{False Positives (FP)}}
$$

- **Recall** (also known as sensitivity) measures how many of the actual positive instances are correctly identified by the model:
$$
\text{Recall} = \frac{\text{True Positives (TP)}}{\text{True Positives (TP)} + \text{False Negatives (FN)}}
$$

### Key Terminology:
1. **True Positives (TP)**: Instances correctly predicted as positive.
2. **False Positives (FP)**: Instances incorrectly predicted as positive (also known as Type I errors).
3. **False Negatives (FN)**: Instances incorrectly predicted as negative (also known as Type II errors).
4. **True Negatives (TN)**: Instances correctly predicted as negative.

Using the F1 score helps ensure that your model performs well not just on the majority class but also on the minority class in your data.

## F1 for multiple classes: F1-Weighted, F1-micro, F1-macro

For multi-class classification, where the goal is to classify instances into one of several categories, the F1 score can be computed in different ways to evaluate the overall performance of the model.

### F1 Weighted
- **F1-weighted** calculates the F1 score for each class individually, but weights each class’s F1 score by the number of instances in that class.
- This approach ensures that the F1 score reflects both the performance of the model on each class and the importance of that class based on its prevalence in the dataset.

- **Calculation:**
    1. **Compute Class-Specific F1 Scores**:
       - First, the F1 score is computed for each class $i$ independently: Treats class $i$ as the `positive` class and all other classes as the `negative` class:
   $$
   \text{F1}_i = 2 \times \frac{\text{Precision}_i \times \text{Recall}_i}{\text{Precision}_i + \text{Recall}_i}
   $$
   where precision and recall are calculated using the true positives, false positives, and false negatives specific to class \( i \).

    2. **Weight F1 by Class Size**:
       - Each class’s F1 score is then weighted by the proportion of instances belonging to that class:
   $$
   \text{Weighted F1} = \sum_{i=1}^{N} w_i \times \text{F1}_i
   $$
   where $w_i = \frac{\text{Number of instances in class } i}{\text{Total number of instances in the dataset}}$.

    3. **F1-Weighted Calculation**:
       - Finally, the F1-weighted score is the sum of these weighted F1 scores across all classes.

### F1 Micro
- **Definition**: F1 Micro calculates precision and recall globally by counting the total true positives across all classes, false positives across all classes, and false negatives accross all classes. It treats each instance equally, regardless of its class.
- **Use Case**: F1 Micro is useful when you want to evaluate the overall performance of your model without giving extra weight to any particular class. It’s especially good when the classes are balanced or when the focus is on the overall accuracy of the model.
- **Calculation**: 
    $$ 
    \text{F1 Micro} = \frac{2 \times \text{Global Precision} \times \text{Global Recall}}{\text{Global Precision} + \text{Global Recall}} 
    $$
    where global precision and recall are computed from the sum of TP, FP, and FN across all classes.

### F1 Macro
- **Definition**: F1-Macro is F1-Weighted when all class weights are set to the 1/(number of classes)
- **Calculation**: 
    $$
    \text{F1 Macro} = \frac{1}{N} \sum_{i=1}^{N} \text{F1}_i 
    $$
    where \( N \) is the number of classes and $\text{F1}_i$ is the F1 score of class \( i \)

### Summary:
- **F1 Weighted** assigns weights to each class based on its frequency, giving more influence to classes with more instances, which makes it a better reflection of the model's performance on the entire dataset.
- **F1 Micro** treats all instances equally, calculating the overall performance across all classes, making it ideal for assessing general accuracy when class distribution is not a concern.
- **F1 Macro** calculates the F1 score for each class independently and then averages them, ensuring that minority classes are given equal importance, making it particularly sensitive to poor performance in  classes with fewer instances in the data.


```python
import numpy as np
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
from sklearn.preprocessing import LabelEncoder

def calculate_metrics(true_labels, predicted_labels, k, distance, vote):
    """
    Calculate F1-micro performance metrics of a classifier.

    Parameters:
    true_labels: array-like, shape (n_samples,)
        The actual labels of the dataset.

    predicted_labels: array-like, shape (n_samples,)
        The labels predicted by the model.

    k: int
        The number of nearest neighbors used in the model.

    distance: str
        The type of distance metric used in the model (e.g., 'euclidean', 'manhattan').

    vote: str
        The type of voting method used (e.g., 'majority', 'd_weighted').

    Returns:
    setting: dict
        A dictionary containing the knowledge representation (k, d, g).
    f1: the F1 score 
    """
    label_encoder = LabelEncoder()
    true_labels_encoded = label_encoder.fit_transform(true_labels)
    predicted_labels_encoded = label_encoder.transform(predicted_labels)
    
    f1 = f1_score(true_labels_encoded, predicted_labels_encoded, average='weighted')
    accuracy = accuracy_score(true_labels_encoded, predicted_labels_encoded)
    precision = precision_score(true_labels_encoded, predicted_labels_encoded, average='weighted')
    recall = recall_score(true_labels_encoded, predicted_labels_encoded, average='weighted')
    
    print("====================")
    print(f"K value: {k}")
    print(f"Distance function: {distance}")
    print(f"Vote function: {vote}")
    print(f"F1 Score: {f1:.3f}")
    print(f"Accuracy: {accuracy:.3f}")
    print(f"Precision: {precision:.3f}")
    print(f"Recall: {recall:.3f}")
    print("====================\n")

    setting = f"{k}/{distance}/{vote}"
    return setting, f1

setting,f1 = calculate_metrics(y_validation, prediction, 1, "Manhattan distance", "Majority vote")
```

    ====================
    K value: 1
    Distance function: Manhattan distance
    Vote function: Majority vote
    F1 Score: 0.243
    Accuracy: 0.415
    Precision: 0.172
    Recall: 0.415
    ====================
    


### Hyperparameter search
We will now perform the hyperparameter search. 
- Specifically, we will search over the following model space:
    1. Different $k = \{1, 2, 4, 1000\}$
    2. Different $d = \{\text{Manhattan (L1)}, \text{Euclidean (L2)}, \text{Mahalanobis}\}$.
    3. Different $g \in \{\text{majority vote}, \text{distance-weighted vote}\}$.
- The model space has size $4 \times 3 \times 2=24$ models.
- Let's now define the diffent distance functions and vote functions.


```python
import math

def euclidean_distance(Xtr, x):
    """
    Computes the Euclidean distance between a set of instances X1 and a single instance x.
    
    Parameters:
    X1: array-like, shape (n_samples_X1, n_features)
    x: array-like, shape (1, n_features)
    
    Returns:
    distances: array-like, shape (n_samples_X1,1)
        The Euclidean distances between each instance of X1 and the instance x.
    """
    return np.sqrt(np.sum((Xtr - x)**2, axis=1))

def mahalanobis_distance(Xtr, x):
    """
    Computes the Mahalanobis distance between a set of instances Xtr and a single instance x.
    
    Parameters:
    X1: array-like, shape (n_samples_X1, n_features)
    x: array-like, shape (1, n_features)
    
    Returns:
    distances: array-like, shape (n_samples_X1,1)
        The Mahalanobis distances between the instances in Xtr and the instance x.
    """
    Xtr = np.array(Xtr)
    x = np.array(x)

    # Computes the covariance matrix of Xtr and get its inverse. 
    # The parameter rowvar=False enforces that the instances are in the rows of the matrix (this should be the default)
    cov_matrix = np.cov(Xtr, rowvar=False)
    inv_cov_matrix = np.linalg.inv(cov_matrix)
    
    diff = Xtr - x
    distances = np.sqrt(np.sum(diff @ inv_cov_matrix * diff, axis=1))
    # one could also use above: distances = np.sqrt(np.einsum('ij,jk,ik->i', diff, inv_cov_matrix, diff))
    return distances

def d_weighted_vote(nearest_labels, nearest_distances):
    """
    Perform a distance-weighted voting for classification.

    Parameters:
    nearest_labels: array-like, shape (n_neighbors,)
        The labels of the nearest neighbors.

    nearest_distances: array-like, shape (n_neighbors,)
        The distances of the nearest neighbors.

    Returns:
    predicted_label:
        The label predicted by distance-weighted voting.
    """
    unique_labels = np.unique(nearest_labels)
    d_weighted_votes = np.zeros(len(unique_labels))
    for i, label in enumerate(unique_labels):
        label_distances = nearest_distances[nearest_labels == label]
        d_weighted_votes[i] = np.sum(1 / (label_distances + 1e-5)) # 1e-5 avoids division by zero if all distances are zero
    return unique_labels[np.argmax(d_weighted_votes)]
```

Now we can peform the hyper-parameter search on the validation set.


```python
distance_functions = {"Manhattan distance": manhattan_distance, 
                      "Euclidean distance": euclidean_distance,
                      "Mahalanobis distance": mahalanobis_distance
                      }
vote_functions = {"Majority vote": majority_vote,
                  "Distance-weighted vote": d_weighted_vote}

f1_scores = {}

for k in [1, 2, 4, 1000]:
    for distance in distance_functions:
        for vote in vote_functions:
            knn = NearestNeighbor(K=k, distance_function=distance_functions[distance], vote_function=vote_functions[vote], d_weighted=(vote == "Distance-weighted vote"))
            knn.train(X_train.to_numpy(), y_train.values)
            prediction = knn.predict(X_validation.values)
            setting, f1 = calculate_metrics(y_validation, prediction, k, distance, vote)
            f1_scores[setting] = f1

```

    ====================
    K value: 1
    Distance function: Manhattan distance
    Vote function: Majority vote
    F1 Score: 0.984
    Accuracy: 0.985
    Precision: 0.985
    Recall: 0.985
    ====================
    
    ====================
    K value: 1
    Distance function: Manhattan distance
    Vote function: Distance-weighted vote
    F1 Score: 0.984
    Accuracy: 0.985
    Precision: 0.985
    Recall: 0.985
    ====================
    
    ====================
    K value: 1
    Distance function: Euclidean distance
    Vote function: Majority vote
    F1 Score: 0.984
    Accuracy: 0.985
    Precision: 0.985
    Recall: 0.985
    ====================
    
    ====================
    K value: 1
    Distance function: Euclidean distance
    Vote function: Distance-weighted vote
    F1 Score: 0.984
    Accuracy: 0.985
    Precision: 0.985
    Recall: 0.985
    ====================
    
    ====================
    K value: 1
    Distance function: Mahalanobis distance
    Vote function: Majority vote
    F1 Score: 0.984
    Accuracy: 0.985
    Precision: 0.985
    Recall: 0.985
    ====================
    
    ====================
    K value: 1
    Distance function: Mahalanobis distance
    Vote function: Distance-weighted vote
    F1 Score: 0.984
    Accuracy: 0.985
    Precision: 0.985
    Recall: 0.985
    ====================
    
    ====================
    K value: 2
    Distance function: Manhattan distance
    Vote function: Majority vote
    F1 Score: 0.974
    Accuracy: 0.975
    Precision: 0.978
    Recall: 0.975
    ====================
    
    ====================
    K value: 2
    Distance function: Manhattan distance
    Vote function: Distance-weighted vote
    F1 Score: 0.984
    Accuracy: 0.985
    Precision: 0.985
    Recall: 0.985
    ====================
    
    ====================
    K value: 2
    Distance function: Euclidean distance
    Vote function: Majority vote
    F1 Score: 0.969
    Accuracy: 0.970
    Precision: 0.973
    Recall: 0.970
    ====================
    
    ====================
    K value: 2
    Distance function: Euclidean distance
    Vote function: Distance-weighted vote
    F1 Score: 0.984
    Accuracy: 0.985
    Precision: 0.985
    Recall: 0.985
    ====================
    
    ====================
    K value: 2
    Distance function: Mahalanobis distance
    Vote function: Majority vote
    F1 Score: 0.974
    Accuracy: 0.975
    Precision: 0.978
    Recall: 0.975
    ====================
    
    ====================
    K value: 2
    Distance function: Mahalanobis distance
    Vote function: Distance-weighted vote
    F1 Score: 0.984
    Accuracy: 0.985
    Precision: 0.985
    Recall: 0.985
    ====================
    
    ====================
    K value: 4
    Distance function: Manhattan distance
    Vote function: Majority vote
    F1 Score: 0.979
    Accuracy: 0.980
    Precision: 0.980
    Recall: 0.980
    ====================
    
    ====================
    K value: 4
    Distance function: Manhattan distance
    Vote function: Distance-weighted vote
    F1 Score: 0.984
    Accuracy: 0.985
    Precision: 0.985
    Recall: 0.985
    ====================
    
    ====================
    K value: 4
    Distance function: Euclidean distance
    Vote function: Majority vote
    F1 Score: 0.972
    Accuracy: 0.975
    Precision: 0.975
    Recall: 0.975
    ====================
    
    ====================
    K value: 4
    Distance function: Euclidean distance
    Vote function: Distance-weighted vote
    F1 Score: 0.989
    Accuracy: 0.990
    Precision: 0.990
    Recall: 0.990
    ====================
    
    ====================
    K value: 4
    Distance function: Mahalanobis distance
    Vote function: Majority vote
    F1 Score: 0.972
    Accuracy: 0.975
    Precision: 0.975
    Recall: 0.975
    ====================
    
    ====================
    K value: 4
    Distance function: Mahalanobis distance
    Vote function: Distance-weighted vote
    F1 Score: 0.989
    Accuracy: 0.990
    Precision: 0.990
    Recall: 0.990
    ====================
    
    ====================
    K value: 1000
    Distance function: Manhattan distance
    Vote function: Majority vote
    F1 Score: 0.243
    Accuracy: 0.415
    Precision: 0.172
    Recall: 0.415
    ====================
    
    ====================
    K value: 1000
    Distance function: Manhattan distance
    Vote function: Distance-weighted vote
    F1 Score: 0.783
    Accuracy: 0.845
    Precision: 0.845
    Recall: 0.845
    ====================
    
    ====================
    K value: 1000
    Distance function: Euclidean distance
    Vote function: Majority vote
    F1 Score: 0.243
    Accuracy: 0.415
    Precision: 0.172
    Recall: 0.415
    ====================
    
    ====================
    K value: 1000
    Distance function: Euclidean distance
    Vote function: Distance-weighted vote
    F1 Score: 0.771
    Accuracy: 0.840
    Precision: 0.761
    Recall: 0.840
    ====================
    
    ====================
    K value: 1000
    Distance function: Mahalanobis distance
    Vote function: Majority vote
    F1 Score: 0.243
    Accuracy: 0.415
    Precision: 0.172
    Recall: 0.415
    ====================
    
    ====================
    K value: 1000
    Distance function: Mahalanobis distance
    Vote function: Distance-weighted vote
    F1 Score: 0.771
    Accuracy: 0.840
    Precision: 0.761
    Recall: 0.840
    ====================
    


- Now let's find the hyperparameters with the best F-1 score in the validation data.


```python
max_key = max(f1_scores, key=f1_scores.get)
print(f"The key with the maximum F1 score is the model k/d/g: {max_key}")
```

    The key with the maximum F1 score is the model k/d/g: 4/Euclidean distance/Distance-weighted vote


- Finally, we can try these hyperparameters on the test data.


```python
test = pd.read_csv("test.csv")

# Separate the true classes from the rest of the data
test_product = test["Product"]
test = test.drop(columns=['Product'])

# Perform the state to number mapping
state_mapping = {'Hawaii': 0, 'Indiana': 1}
test['State'] = test['State'].map(state_mapping)

test,_ = data_normalization(test,train_normalization)

# Use our best method
knn = NearestNeighbor(4, euclidean_distance, d_weighted_vote, True)
# "Retrain" => For this k-NN method it means just storing the training data
knn.train(X_train.to_numpy(), y_train.values)

prediction = knn.predict(test.to_numpy())
calculate_metrics(test_product, prediction, 4, "Euclidean distance", "Distance-weighted vote")
```

    ====================
    K value: 4
    Distance function: Euclidean distance
    Vote function: Distance-weighted vote
    F1 Score: 0.969
    Accuracy: 0.970
    Precision: 0.974
    Recall: 0.970
    ====================
    





    ('4/Euclidean distance/Distance-weighted vote', 0.9688919769157337)


