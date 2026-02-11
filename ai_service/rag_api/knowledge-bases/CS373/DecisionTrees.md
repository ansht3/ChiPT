## CS37300 - Data Mining and Machine Learning

### Fall 2025

##### Instructor: Bruno Ribeiro

----
## Introduction to Decision Trees

# 1. Decision Tree Elements

## 1.1. Tree Models

- Easy to understand knowledge representation  
- Handle mixed variables (discrete/continuous)  
- Recursive divide-and-conquer learning method  
- Efficient inference  
- Not ideal for unstructured data (text, images)  


Data:
| Outlook   | Temperature | Humidity | Windy | Play      |
|-----------|-------------|----------|-------|-----------|
| Sunny     | Hot         | High     | False | Don’t Play |
| Sunny     | Hot         | High     | True  | Don’t Play |
| Overcast  | Hot         | High     | False | Play      |
| Rain      | Mild        | High     | False | Play      |
| Rain      | Cool        | Normal   | False | Play      |
| Rain      | Cool        | Normal   | True  | Don’t Play |
| Overcast  | Cool        | Normal   | True  | Play      |
| Sunny     | Mild        | High     | False | Don’t Play |
| Sunny     | Cool        | Normal   | False | Play      |
| Rain      | Mild        | Normal   | False | Play      |
| Sunny     | Mild        | Normal   | True  | Play      |
| Overcast  | Mild        | High     | True  | Play      |
| Overcast  | Hot         | Normal   | False | Play      |
| Rain      | Mild        | High     | True  | Don’t Play |


Decision tree:
<center><img src="DTexample1.png" width=600px/></center>

**Example**

We have data on customers applying for loans, with attributes like income, amount requested, credit score, and employment status. We can build a decision tree to predict whether a new applicant will be approved or denied. The tree might look something like this:

```
                              Income > 50K?
                              /            \ 
                            /                \
                          /                    \ 
               Amount requested < 1000        Employed?
                 /          \                  /      \ 
               /             \               /          \ 
       {Paid,Paid,Paid}    {Paid}   {Unpaid,Unpaid}    {Paid,Paid,Unpaid}
```

**Advantages of Decision Trees**
- Easy to understand and interpret
- Can handle both numerical and categorical data
- Require little data preparation
- Can handle non-linear relationships between the features $X$ and target variable $Y$

**Disadvantages of Decision Trees**
- Prone to overfitting (memorizing the training data)
- Can be unstable (small changes in data can lead to big changes in the tree)
- Can create biased trees if some classes dominate

## 1.2. Model Space

How large is the space of trees?  

Assumptions:  
- Binary tree  
- Fixed depth  
- 10 binary attributes  

| Tree depth | Number of trees         |
|------------|--------------------------|
| 1          | $10$                     |
| 2          | $8 \times 10^2$          |
| 3          | $3 \times 10^6$          |
| 4          | $2 \times 10^{13}$       |
| 5          | $5 \times 10^{25}$       |

---

## 1.3. Tree Learning

**Top-down recursive (greedy) algorithm**  

1. Start with all examples at the root.  
2. Select best attribute/feature.  
3. Partition examples by attribute.  
4. Recurse on each subset.  

**Other issues:**  
- How to construct features?  
- When to stop growing?  
- How to prune irrelevant parts?  

## 1.4. Example: Choosing Splits

Dataset fragment:

| Fraud | Age | Degree | StartYr | Series7 |
|-------|-----|--------|---------|---------|
| +     | 22  | Y      | 2005    | N       |
| +     | 24  | N      | 2006    | N       |
| -     | 29  | N      | 2003    | N       |
| -     | 25  | N      | 2003    | Y       |
| -     | 31  | Y      | 1995    | Y       |
| -     | 27  | Y      | 1999    | Y       |

- Candidate splits: **Age, Degree, StartYr, Series7**  

<center><img src="DTexample2.png" width=1600px/></center>

## Pseudocode for Decision Tree

```python
DecisionTree(examples, classLabel, attributes):

    features = {}
    for attribute in attributes:
        for value in attribute.values:
            features.add(makeFeature(attribute, value))

    root = Node()
    growTree(root, examples, features)

def growTree(node, examples, features):
    maxScore, maxFeature = 0, None
    for f in features:
        score = evaluate(f, examples)
        if score > maxScore:
            maxFeature, maxScore = f, score

    if maxFeature is None:
        node.classDist = distribution(examples, classLabel)
        return

    node.feature = maxFeature
    left, right = partition(examples, maxFeature)
    growTree(node.left, left, features)
    growTree(node.right, right, features)
````

## 1.5. Widely-used Tree Models

* **CART** (Breiman, Friedman, Olshen, Stone)
* **ID3, C4.5** (Quinlan)

Differences:

* **Split scoring function** (main one)
* Stopping criterion
* Pruning mechanism
* Predictions in leaf nodes

# 2. Splitting Criteria


- Local split value
- **Basic idea:** a good feature splits the examples into subsets that distinguish among the class labels as much as possible... ideally into pure sets of "all positive” (green) or "all negative” (red)

<center><img src="DTexample3.png" width=900px/></center>


**Quiz:**

Is it better to split by Patrons or Type?

(a) Patrons

(b) Type

Answer: (a) Patrons because it better split the classes into different children.

## 2.1. Association between attribute and class label

<center><img src="DTexample4.png" width=1600px/></center>

## 2.2. Information Gain (Entropy Gain)

**Entropy** measures the uncertainty (or impurity) of a probability distribution.  
For a discrete random variable $Y$:

$$
H(Y) = - \sum_{y} p(Y=y) \log_2 p(Y=y)
$$

- If the distribution is **perfectly balanced**, the uncertainty is maximum.  
- If the distribution is **all one class**, the uncertainty is zero.  
- Intermediate cases fall in between.

### Entropy of a random variable

- The entropy of a probability distribution $P(Y)$ **expresses the amount of uncertainty** that we have about the values of $Y$

1. **Random binary variable** $[0.5, 0.5]$  

$$
H(Y) = - (0.5 \log_2 0.5 + 0.5 \log_2 0.5) = 1
$$  

Interpretation: completely unpredictable (like a fair coin).

---

2. **Deterministic binary variable** $[1, 0]$  

$$
H(Y) = - (1 \log_2 1 + 0 \log_2 0) = 0
$$  

Interpretation: no uncertainty at all (always the same outcome).

---

3. **Biased binary variable** $[0.75, 0.25]$  

$$
H(Y) = - (0.75 \log_2 0.75 + 0.25 \log_2 0.25) \approx 0.811
$$  

Interpretation: some uncertainty, but less than a fair coin.

### 2.2.1. Information gain example
- How much does a feature split decrease the entropy?
<center><img src="DTexample5.png" width=1200px/></center>

Entropy of dataset:

$$
Entropy(D) = -\tfrac{9}{14}\log_2\tfrac{9}{14} - \tfrac{5}{14}\log_2\tfrac{5}{14} = 0.940
$$

### 2.2.1. Information gain example (cont)
<center><img src="DTexample6.png" width=600px/></center>

Splitting on **Income**:

* High: \$Entropy = 1.0\$
* Medium: \$Entropy = 0.918\$
* Low: \$Entropy = 0.811\$

Gain:

$$
Gain(D, Income) = 0.940 - \Big( \tfrac{4}{14}[1.0] + \tfrac{6}{14}[0.918] + \tfrac{4}{14}[0.811] \Big) = 0.029
$$

## 2.3. Gini Index

$$
Gini(Y) = 1 - \sum_y P(Y=y)^2
$$

* Similar to information gain.
* Measures decrease in impurity after split.

## 2.4 Chi-Square Test for Splits

- **Purpose**: test independence between two categorical attributes  
  (e.g., attribute vs. class label).  

- **Relation to Gini**: similar idea, but  
  - works **only** with categorical variables,  
  - cannot be used directly for continuous targets.  

- **Interpretation**:  
  The Chi-square score measures **how much the observed split deviates from what we would expect if the data were random**.  

### Key Insight

- **Small $\chi^2$ score** ⟹ The split does **not** add significant information.  
- **Large $\chi^2$ score** ⟹ The split is **statistically significant**.  


### Visual Intuition

Suppose we have $N$ data points:  
<center><img src="DTexample7.png" width=600px/></center>

- $N_L$: data points going to the **left child**  
- $N_R$: data points going to the **right child**  

We compare **observed class counts** in $N_L$ and $N_R$ with the **expected counts under independence**.  

Chi-square score is small if either:
- Target label is unrelated to attribute we want to split on
- $N$, $N_L$, $N_R$ are too small for good statistical significance.  
- Do not perform splits that are lower than a chi-square threshold $< t$. 

### Formula

The Chi-square score is:

$$
\chi^2 = \sum_{i,j} \frac{(O_{ij} - E_{ij})^2}{E_{ij}}
$$

- $O_{ij}$ = observed number of points from class $i$ in child $j$  
- $E_{ij}$ = expected number of points from class $i$ in child $j$ if labels were independent of the attribute  
- Large $\chi^2$: split is useful  
- Small $\chi^2$: split is not meaningful  

<center><img src="DTexample8.png" width=600px/></center>

### Example with Buy/Not Buy dataset

<center><img src="DTexample9.png" width=600px/></center>
<center><img src="DTexample10.png" width=600px/></center>

### Rule of Thumb

- Compare $\chi^2$ value to a **critical value** from the Chi-square distribution.  
- Example: For a $2 \times 2$ table, the **95% significance threshold** is **3.84**.  
- If $\chi^2 < 3.84$ ⟹ **do not split**.  

# 3. Stopping and Pruning

- Top-down recursive divide and conquer algorithm
- Start with all examples at root
- Select best attribute/feature 
- Partition examples by selected attribute
- Recurse and repeat

Other issues:
- How to construct features
- **When to stop growing**
- **Pruning irrelevant parts of the tree**


## 3.1. When to Stop Growing

* All samples at node have same class
* No attributes left
* No samples left


**Problem**: Trees overfit → test accuracy decreases.

**Solution**: **Pruning**.


## 3.2. Pruning Methods

* **Postpruning**

  * Grow full tree
  * Use validation set to prune (a.k.a. **pruning set** (separate from training data) to evaluate whether pruning improves accuracy).

  
* **Prepruning**

  * Stop early if best split not statistically significant
  * Use chi-square or MDL to penalize large trees

## 3.3. Algorithm Comparison

| Aspect    | CART                          | C4.5                  |
| --------- | ----------------------------- | --------------------- |
| Criterion | Gini index                    | Information gain      |
| Search    | Hill-climbing, simple→complex | Same                  |
| Stopping  | Pure leaves                   | Pure leaves           |
| Pruning   | Cross-validation              | Reduced-error pruning |

### 3.2.1. Pre-pruning methods

- Stop growing tree at some point during top-down construction when there is no longer sufficient data to make reliable decisions

**Approach:**
- Choose threshold on feature score
- Stop splitting if the best feature score is below threshold

### 3.2.2. Postpruning

### Step 1: Define the Subtree

Let **T** be a subtree rooted at node $v$:  

```text
        (v)
       /   \
   (child) (child)
     ...      ...
     Subtree T


### Step 2: Compute Pruning Gain

The **gain from pruning at $v$** is:

$$
Gain(v) = \#\text{errors in } T \;-\; \#\text{errors if $v$ is a leaf}
$$

- If $Gain(v) > 0$: pruning improves accuracy.  
- If $Gain(v) \leq 0$: keep the subtree.  

### Step 3: Pruning Procedure

1. Evaluate all candidate nodes $v$.  
2. Pick the node with the **largest gain**.  
3. Replace the subtree $T$ with a **leaf node** labeled by the majority class at $v$.  
4. Repeat until no positive-gain nodes remain.  

### Step 4: Bottom-Up Restriction

- A subtree $T$ can only be pruned if it does **not** contain a smaller subtree with lower error than $T$.  

---

**Before pruning:**  

```text
        (v)
       /   \
   (child) (child)
     ...      ...
     Subtree T
````

**After pruning:**

```text
        (v)
       [Leaf]
 Majority class of v
```

````


### Key Idea

- **Pruning reduces complexity** by replacing unnecessary branches with a single leaf.  
- The trade-off: **slightly less fit to training data** but **better generalization**.  

# Python Example: Decision tree implementation from scratch


```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
import numpy as np
```

## Loading the Data


```python
# Load the IRIS dataset
iris = load_iris()
# Features
X = iris.data.copy() 
# Classes
y = iris.target.reshape(150,1)
# Splitting the dataset into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
# Horizontally stacking the train_dataset together
train_dataset = np.hstack((X_train,y_train))
```

## Scoring Function
As you've seen in class there are various scoring functions that can be used for splitting. 
Here we use the **Gini Index**.


```python
# Calculate the Gini index for a split dataset
def gini_index(groups, classes):
    # count all samples at split point
    n_instances = float(sum([len(group) for group in groups]))
    # sum weighted Gini index for each group
    gini = 0.0
    for group in groups:
        size = float(len(group))
        # avoid divide by zero
        if size == 0:
            continue
        score = 0.0
        # score the group based on the score for each class
        for class_val in classes:
            p = [row[-1] for row in group].count(class_val) / size
            score += p * p
        # weight the group score by its relative size
        gini += (1.0 - score) * (size / n_instances)
    return gini
```

## Splitting the data
We split the data into a left and a right group.


```python
def split_data(index, value, dataset):
    left, right = list(), list()
    for row in dataset:
        if row[index] < value:
            left.append(row)
        else:
            right.append(row)
    return left, right
```

## Best Split
Now that we have a scoring function and a method to split the data, we can eveluate the best possible split. Each node of our tree will contain: the index of the features used for the split, the value of the feature and the left and right groups (or subtrees).


```python
# Select the best split point for a dataset
def get_split(dataset):
    class_values = list(set(row[-1] for row in dataset))
    b_index, b_value, b_score, b_groups = 999, 999, 999, None
    for index in range(len(dataset[0])-1):
        for row in dataset:
            groups = split_data(index, row[index], dataset)
            gini = gini_index(groups, class_values)
            if gini < b_score:
                b_index, b_value, b_score, b_groups = index, row[index], gini, groups
    return {'index':b_index, 'value':b_value, 'groups':b_groups}
```

##  Leaf node
Returns the most common label in a list of rows.


```python
def to_leaf(group):
    outcomes = [row[-1] for row in group]
    return max(set(outcomes), key=outcomes.count)
```

## Recursive Splitting


```python
# Create child splits for a node or make terminal
def split(node, max_depth, min_size, depth):
    left, right = node['groups']
    del(node['groups'])
    # check for a no split
    if not left or not right:
        node['left'] = node['right'] = to_leaf(left + right)
        return
    # check for max depth
    if depth >= max_depth:
        node['left'], node['right'] = to_leaf(left), to_leaf(right)
        return
    # process left child
    if len(left) <= min_size:
        node['left'] = to_leaf(left)
    else:
        node['left'] = get_split(left)
        split(node['left'], max_depth, min_size, depth+1)
    # process right child
    if len(right) <= min_size:
        node['right'] = to_leaf(right)
    else:
        node['right'] = get_split(right)
        split(node['right'], max_depth, min_size, depth+1)
```

## Build the Tree


```python
def build_tree(train, max_depth, min_size):
    root = get_split(train)
    split(root, max_depth, min_size, 1)
    return root
```


```python
tree = build_tree(train_dataset, 2, 1)
```

## Visualize the tree


```python
def print_tree(node, depth=0):
    if isinstance(node, dict):
        print('%s[%s < %.3f]' % ((depth*'  ', (iris.feature_names[node['index']]), node['value'])))
        print_tree(node['left'], depth+1)
        print_tree(node['right'], depth+1)
    else:
        print('%s[%s]' % ((depth*'  ', node)))
```


```python
print_tree(tree)
```

    [petal length (cm) < 3.000]
      [sepal length (cm) < 4.600]
        [0.0]
        [0.0]
      [petal width (cm) < 1.700]
        [1.0]
        [2.0]


## Making Predictions


```python
def predict(node, row):
    if row[node['index']] < node['value']:
        if isinstance(node['left'], dict):
            return predict(node['left'], row)
        else:
            return node['left']
    else:
        if isinstance(node['right'], dict):
            return predict(node['right'], row)
        else:
            return node['right']
```

## Testing


```python
y_pred = list()
for row in X_test:
    prediction = predict(tree, row)
    y_pred.append(prediction)
print(accuracy_score(y_test, y_pred))
```

    0.94



```python
print(classification_report(y_test, y_pred))
```

                  precision    recall  f1-score   support
    
               0       1.00      1.00      1.00        18
               1       0.89      0.94      0.91        17
               2       0.93      0.87      0.90        15
    
        accuracy                           0.94        50
       macro avg       0.94      0.94      0.94        50
    weighted avg       0.94      0.94      0.94        50
    

