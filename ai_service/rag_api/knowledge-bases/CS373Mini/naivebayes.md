# Data Mining & Machine Learning
### CS37300 – Purdue University  
### Instructor & Copyright: Bruno Ribeiro
September 22, 2025  



## Classification

- **Classification is a supervised learning task**
  - Input data: $\{x_i, y_i\}_{i=1}^n$ sampled independently from distribution $P(X, Y)$
  - where $X$ is the input and $Y$ is the (discrete) predicted label

- In its simplest form, a classification model defines a decision boundary (h) and labels for each side of the boundary

- Input: $x = \{x_1, x_2, ..., x_p\}$ is a set of attributes, function $f$ assigns a label $y$ to input $x$, where $y$ is a discrete variable with a finite number of values

<div style="text-align: center;">
    <img src="nbc1.png" style="width: 30%; height: auto;"/>
</div>

## Predictive Modeling: Learning

## Learning Predictive Models

- **Choose a data representation**
- **Select a knowledge representation** (a "model")
  - Defines a space of possible models $M = \{M_1, M_2, ..., M_k\}$
- **Use search to identify "best" model(s)**
  - Search the space of models (i.e., with alternative structures and/or parameters)
  - Evaluate possible models with **scoring function** to determine the model which best fits the data

## Scoring Functions

- Given a model $M$ and dataset $D$, we would like to "score" model $M$ with respect to $D$
- Goal is to rank the models in terms of their utility (for capturing $D$) and choose the "best" model
- Score function can be used to search over **parameters** and/or **model structure**

### Score functions can be different for:
- Models vs. patterns
- Predictive vs. descriptive functions
- Models with varying complexity (i.e., number parameters)

## Predictive Scoring Functions

Assess the quality of predictions for a set of instances

Measures difference between the prediction $M$ makes for an instance $i$ and the true class label value of $i$

$$S(M) = \sum_{i=1}^{N_{test}} d[f(x^{(i)}; M), y^{(i)}]$$

- Predicted class label for item $i$: $f(x^{(i)}; M)$
- True class label for item $i$: $y^{(i)}$
- Distance between predicted and true: $d[\cdot, \cdot]$
- Sum over examples

## Predictive Scoring Functions (cont.)

### Common score functions:

**Zero-one loss:**
$$S_{0/1}(M) = \frac{1}{N_{test}} \sum_{i=1}^{N_{test}} I[f(x^{(i)}; M), y^{(i)}]$$

where $I(a, b) = \begin{cases} 1 & a \neq b \\ 0 & \text{otherwise} \end{cases}$

**Squared loss:**
$$S_{sq}(M) = \frac{1}{N_{test}} \sum_{i=1}^{N_{test}} [f(x^{(i)}; M) - y^{(i)}]^2$$

**Do we minimize or maximize these functions?**

## Scoring Functions - Uses

- **Guide search inside of algorithms**
  - Select path in heuristic search
  - Decide when to stop
  - Identify whether to include model or pattern in output

- **Evaluate results outside of algorithms**
  - Measure the absolute quality of model or pattern
  - Compare the relative quality of different algorithms or outputs

## Where's the Search?

## What Space Are We Searching?

**Scenario: Assume goal is to maximize the score**

Learned model ≈ $(θ_0 = 0.8, θ_1 = 0.4)$

<div style="text-align: center;">
    <img src="nbc2.png" style="width: 50%; height: auto;"/>
</div>

## Searching Over Models/Patterns

Consider a **space** of possible models $M = \{M_1, M_2, ..., M_k\}$ with parameters $θ$

Search could be over model structures or parameters, e.g.:

- **Parameters**: In a linear regression model, find the regression coefficients ($β$) that minimize squared loss on the training data

- **Model structure**: In decision trees, find the tree structure that maximizes accuracy on the training data

## Quiz

In decision trees, if we are worried that the amount of data on a tree child is not enough to accurately measure the true split performance, we should (more than one can be correct):

- (c) Use the Gini gain score
- (d) Use the Chi-Square score
- (e) Use the Gini gain score but perform post-pruning using validation data

## Today's Class: Naive Bayes Classifiers

## 1. Classification as Probability Estimation

- Instead of learning a function $f$ that assigns labels given input $Y ← X$
- Learn the conditional probability distribution

$$P(Y = y | X = x) = P(Y = y | X = (x_1, x_2, ..., x_p))$$

- Can use probabilities for the tasks:
  - Classification
  - Regression (with uncertainty)
  - Ranking

## 2. Knowledge Representation and Model Space

## 2.1. Bayes Rule for Probabilistic Classifier

$$P(Y|X) = \frac{P(X|Y)P(Y)}{P(X)}$$

$$= \frac{P(X|Y)P(Y)}{[P(X|Y=+)P(Y=+)] + [P(X|Y=-)P(Y=-)]}$$

Random variables $X = (X_1, ..., X_p)$, $Y ∈ \{-, +\}$

where $\propto$ means proportional to.

**Denominator**: normalizing factor to make probabilities sum to 1 (can be computed from numerators)

## 2.2. Naive Bayes Classifier

**Bayes rule**: $P(Y|X) \propto P(X|Y)P(Y)$

**Naive assumption**: (IMPORTANT) *Attributes are conditionally independent given the class:*

$$P(Y|X_1,\ldots,X_p) \propto P(X_1,\ldots,X_p|Y)P(Y) \underset{\text{(naive independence)}}{\overset{}{=}} \prod_{i=1}^p P(X_i|Y)P(Y)$$

Random variables $X = (X_1, ..., X_p)$, $Y ∈ \{-, +\}$

## 2.2. Naive Bayes Classifier (cont.)

Define $p(y, x) = P(Y = y, X = x)$

$$p(y|x) = \frac{p(x|y)p(y)}{p(x)} = \frac{\prod_i p(x_i|y) p(y)}{\sum_j p(x|y_j)p(y_j)}$$

**Model space:**
- Parameters in conditional probability distributions (CPD) $p(x_i|y)$, $i \in \{1,\ldots,p\}$.
- Parameters in prior distribution (PD) $p(y)$.



## 2.3. NBC Learning

### Training Dataset

| age    | income | student | credit_rating | buys_computer |
|--------|--------|---------|---------------|---------------|
| ≤30    | high   | no      | fair          | no            |
| ≤30    | high   | no      | excellent     | no            |
| 31..40 | high   | no      | fair          | yes           |
| >40    | medium | no      | fair          | yes           |
| >40    | low    | yes     | fair          | yes           |
| >40    | low    | yes     | excellent     | no            |
| 31..40 | low    | yes     | excellent     | yes           |
| ≤30    | medium | no      | fair          | no            |
| ≤30    | low    | yes     | fair          | yes           |
| >40    | medium | yes     | fair          | yes           |
| ≤30    | medium | yes     | excellent     | yes           |
| 31..40 | medium | no      | excellent     | yes           |
| 31..40 | high   | yes     | fair          | yes           |
| >40    | medium | no      | excellent     | no            |

$$P(BC|A,I,S,\text{CR}) = \frac{P(A,I,S,\text{CR}|\text{BC})P(\text{BC})}{P(A,I,S,\text{CR})}$$

$$= \frac{P(A|\text{BC})P(I|\text{BC})P(S|\text{BC})P(CR|\text{BC})P(\text{BC})}{P(A,I,S,\text{CR})}$$

$$\propto P(A|\text{BC})P(I|\text{BC})P(S|\text{BC})P(CR|\text{BC})P(\text{BC})$$

- **NBC parameters = Conditional Prob. Dist. (CPD), prior**
    - CPDs: $P(A|\text{BC})$, $P(I|\text{BC})$, $P(S|\text{BC})$, $P(\text{CR}|\text{BC})$
    - Prior: $P(\text{BC})$

## Learning CPDs from Examples

|     | Low | Medium | High |
|-----|-----|--------|------|
| No  | 2   | 13     | 0    |
| Yes | 10  | 13     | 17   |

$$P[X_1 = \text{Low} | Y = \text{Yes}] = \frac{10}{(10 + 13 + 17)}$$

$$P[Y = \text{No}] = \frac{(2 + 13)}{(2 + 13 + 10 + 13 + 17)}$$

## NBC Learning - Parameter Estimation

Estimate prior $P(BC)$ and conditional probability distributions $P(A|BC)$, $P(I|BC)$, $P(S|BC)$, $P(CR|BC)$ independently with maximum likelihood estimation

### $P(A|BC)$
| BC  | A      | θ   |
|-----|--------|-----|
| yes | ≤30    | 2/9 |
| yes | 31..40 | 4/9 |
| yes | >40    | 3/9 |
| no  | ≤30    | 3/5 |
| no  | 31..40 | 0/5 |
| no  | >40    | 2/5 |

### $P(I|BC)$
| BC  | I      | θ   |
|-----|--------|-----|
| yes | high   | 2/9 |
| yes | med    | 4/9 |
| yes | low    | 3/9 |
| no  | high   | 2/5 |
| no  | med    | 2/5 |
| no  | low    | 1/5 |

### $P(S|BC)$
| BC  | S   | θ   |
|-----|-----|-----|
| yes | yes | 6/9 |
| yes | no  | 3/9 |
| no  | yes | 1/5 |
| no  | no  | 4/5 |

### $P(CR|BC)$
| BC  | CR   | θ   |
|-----|------|-----|
| yes | exc  | 3/9 |
| yes | fair | 6/9 |
| no  | exc  | 4/5 |
| no  | fair | 1/5 |

### $P(BC)$
| BC  | θ    |
|-----|------|
| yes | 9/14 |
| no  | 5/14 |

## 2.4. NBC Prediction

**Question**: What is the probability that a new person will buy a computer?

**Solution:** Need to compute the following equation from the above CPDs and Prior: $$P(\text{BC} = \text{yes} |X_1,\ldots,X_p) = \frac{  \prod_{i=1}^p P(X_i|\text{BC}=\text{yes})P(\text{BC}=\text{yes}) }{\prod_{i=1}^p P(X_i|\text{BC}=\text{yes})P(\text{BC}=\text{yes}) + \prod_{i=1}^p P(X_i|\text{BC}=\text{no})P(\text{BC}=\text{no})}.$$ 


**New instance**: 31..40, high, no, excellent, ?

$$P(BC = \text{yes} | A = 31..40, I = \text{high}, S = \text{no}, CR = \text{exc})$$

$$\propto P(A = 31..40 | BC = \text{yes}) \cdot P(I = \text{high} | BC = \text{yes})$$
$$\cdot P(S = \text{no} | BC = \text{yes}) \cdot P(CR = \text{exc} | BC = \text{yes}) \cdot P(BC = \text{yes})$$

$$\propto \frac{4}{9} \cdot \frac{2}{9} \cdot \frac{3}{9} \cdot \frac{3}{9} \cdot \frac{9}{14}$$

<div style="text-align: center;">
    <img src="nbc3.png" style="width: 50%; height: auto;"/>
</div>

Then:

$$P(BC = \text{yes} | A, I, S, CR) = \frac{\prod_{i} P(X_i | BC = \text{yes}) \cdot P(BC = \text{yes})}{\sum_{bc \in \{\text{yes}, \text{no}\}} \prod_{i} P(X_i | BC = bc) \cdot P(BC = bc)}$$

where $X_i \in \{A = 31\text{--}40, I = \text{high}, S = \text{no}, CR = \text{exc}\}$.

**Quiz:** In the NBC model, which components need to be estimated from training data? Select all that apply.

a) P(Y) - the prior probability of each class

b) P(X) - the marginal probability of the features

c) P($X_i$|Y) - the conditional probability of each feature given the class

d) P(Y|X) - the posterior probability

## Zero Counts Are a Problem

- If an attribute value does not occur in training example, we assign zero probability to that value

- **How does that affect the conditional probability?**
  - It equals 0!!!

- **Why is this a problem?**
  - The entire product becomes 0, regardless of other evidence

- **Solution**: Adjust for zero counts by "smoothing" probability estimates

## Smoothing: Laplace Correction

|     | Low | Medium | High |
|-----|-----|--------|------|
| No  | 2   | 13     | 0    |
| Yes | 10  | 13     | 17   |

Without correction:
$$P[X_1 = \text{High} | Y = \text{No}] = \frac{0}{(2 + 13 + 0)}$$

**Laplace correction:**
$$P[X_1 = \text{High} | Y = \text{No}] = \frac{0 + 1}{(2 + 13 + 0) + 3}$$

- Numerator: add 1
- Denominator: add k, where k = number of possible values of X
- Equivalent to adding uniform prior over $P(θ)$

## Is Assuming Independence a Problem?

### What is the effect on probability estimates?
- Over-counting evidence, leads to overly confident probability estimates

### What is the effect on classification?
- Less clear...
- For a given input $x$, suppose $f(x) = \text{True}$
- Naive Bayes will correctly classify if $P[f(x) = \text{True} | x] > 0.5$
- ...thus it may not matter if probabilities are overestimated

## Gaussian Naive Bayes for Continuous Features

### Handling Continuous Attributes in NBC

### The Challenge
- Original NBC formulation assumes discrete/categorical features
- Real-world data often contains continuous features (height, weight, temperature, etc.)
- Need probability density functions instead of probability mass functions

### Gaussian Assumption
For continuous feature $X_i$, assume it follows a Gaussian (Normal) distribution given class $Y$:

$$P(X_i = x | Y = c) = \frac{1}{\sqrt{2\pi\sigma_{ic}^2}} \exp\left(-\frac{(x - \mu_{ic})^2}{2\sigma_{ic}^2}\right)$$

### Parameters to Estimate
For each continuous feature $i$ and class $c$:
- **Mean**: $\mu_{ic} = \frac{1}{N_c} \sum_{j \in \text{class } c} x_i^{(j)}$
- **Variance**: $\sigma_{ic}^2 = \frac{1}{N_c} \sum_{j \in \text{class } c} (x_i^{(j)} - \mu_{ic})^2$

where $N_c$ is the number of training examples in class $c$

### Classification Process
For a new instance with continuous features:
$$P(Y = c | X) \propto P(Y = c) \prod_{i=1}^{d} P(X_i | Y = c)$$

Where $P(X_i | Y = c)$ uses the Gaussian PDF with learned $\mu_{ic}$ and $\sigma_{ic}$

## Gaussian NBC: Example and Considerations

### Example: Iris Classification
Consider classifying iris flowers with continuous features (petal length, sepal width):

| Feature | Class | Mean (μ) | Std Dev (σ) |
|---------|-------|----------|-------------|
| Petal Length | Setosa | 1.46 | 0.17 |
| Petal Length | Versicolor | 4.26 | 0.47 |
| Petal Length | Virginica | 5.55 | 0.55 |
| Sepal Width | Setosa | 3.43 | 0.38 |
| Sepal Width | Versicolor | 2.77 | 0.31 |
| Sepal Width | Virginica | 2.97 | 0.32 |

**New flower**: Petal Length = 3.5, Sepal Width = 3.0

Calculate for each class $c$:
- $P(\text{PL}=3.5|c)$ using $\mathcal{N}(\mu_{\text{PL},c}, \sigma_{\text{PL},c}^2)$
- $P(\text{SW}=3.0|c)$ using $\mathcal{N}(\mu_{\text{SW},c}, \sigma_{\text{SW},c}^2)$
- Multiply with prior $P(c)$

### Advantages of Gaussian NBC
- **Simple parameter estimation**: Only need mean and variance
- **Efficient computation**: $O(nd)$ for $n$ samples, $d$ features
- **Works well when**: Features are approximately normal within each class
- **No binning required**: Avoids information loss from discretization

### Limitations and Considerations
- **Normality assumption**: May not hold for all continuous features
  - Solution: Transform features (log, Box-Cox) or use kernel density estimation (we will not cover this part)
- **Variance estimation issues**: 
  - Small sample sizes can lead to unreliable variance estimates
  - Solution: Use pooled variance or add smoothing term
- **Outlier sensitivity**: Gaussian parameters sensitive to extreme values. **Remove outliers first.**
- **Mixed feature types**: Can combine Gaussian NBC for continuous with standard NBC for categorical

## Naive Bayes Classifier Summary

### Simplifying (naive) assumption:
Attributes are conditionally independent given the class

### Strengths:
- Easy to implement
- Often performs well even when assumption is violated
- Can be learned incrementally

### Weaknesses:
- Class conditional assumption produces skewed probability estimates
- Dependencies among variables cannot be modeled

## NBC Learning - Summary

### Model space
- Parametric model with specific form (i.e., based on Bayes rule and assumption of conditional independence)
- Models vary based on parameter estimates in CPDs and prior

### Search algorithm
- Closed form: Posterior probability $P(Y|X_1,\ldots,X_p)$ has a unique exact solution (known in closed-form) via Bayes rule.

### Scoring function
- Posterior distribution of labels given the data.

# Naive Bayes classifier Example

We will now illustrate an implementation of the Naive Bayes classifier for multinomial data.

## Loading and preprocessing the dataset


```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import numpy as np
```


```python
# Load the IRIS dataset
iris = load_iris()
X = iris.data.copy()
y = np.array([iris.target_names[yi] for yi in iris.target])
n_quantiles = 3
print(iris['DESCR'])
```

    .. _iris_dataset:
    
    Iris plants dataset
    --------------------
    
    **Data Set Characteristics:**
    
        :Number of Instances: 150 (50 in each of three classes)
        :Number of Attributes: 4 numeric, predictive attributes and the class
        :Attribute Information:
            - sepal length in cm
            - sepal width in cm
            - petal length in cm
            - petal width in cm
            - class:
                    - Iris-Setosa
                    - Iris-Versicolour
                    - Iris-Virginica
                    
        :Summary Statistics:
    
        ============== ==== ==== ======= ===== ====================
                        Min  Max   Mean    SD   Class Correlation
        ============== ==== ==== ======= ===== ====================
        sepal length:   4.3  7.9   5.84   0.83    0.7826
        sepal width:    2.0  4.4   3.05   0.43   -0.4194
        petal length:   1.0  6.9   3.76   1.76    0.9490  (high!)
        petal width:    0.1  2.5   1.20   0.76    0.9565  (high!)
        ============== ==== ==== ======= ===== ====================
    
        :Missing Attribute Values: None
        :Class Distribution: 33.3% for each of 3 classes.
        :Creator: R.A. Fisher
        :Donor: Michael Marshall (MARSHALL%PLU@io.arc.nasa.gov)
        :Date: July, 1988
    
    The famous Iris database, first used by Sir R.A. Fisher. The dataset is taken
    from Fisher's paper. Note that it's the same as in R, but not as in the UCI
    Machine Learning Repository, which has two wrong data points.
    
    This is perhaps the best known database to be found in the
    pattern recognition literature.  Fisher's paper is a classic in the field and
    is referenced frequently to this day.  (See Duda & Hart, for example.)  The
    data set contains 3 classes of 50 instances each, where each class refers to a
    type of iris plant.  One class is linearly separable from the other 2; the
    latter are NOT linearly separable from each other.
    
    .. topic:: References
    
       - Fisher, R.A. "The use of multiple measurements in taxonomic problems"
         Annual Eugenics, 7, Part II, 179-188 (1936); also in "Contributions to
         Mathematical Statistics" (John Wiley, NY, 1950).
       - Duda, R.O., & Hart, P.E. (1973) Pattern Classification and Scene Analysis.
         (Q327.D83) John Wiley & Sons.  ISBN 0-471-22361-1.  See page 218.
       - Dasarathy, B.V. (1980) "Nosing Around the Neighborhood: A New System
         Structure and Classification Rule for Recognition in Partially Exposed
         Environments".  IEEE Transactions on Pattern Analysis and Machine
         Intelligence, Vol. PAMI-2, No. 1, 67-71.
       - Gates, G.W. (1972) "The Reduced Nearest Neighbor Rule".  IEEE Transactions
         on Information Theory, May 1972, 431-433.
       - See also: 1988 MLC Proceedings, 54-64.  Cheeseman et al"s AUTOCLASS II
         conceptual clustering system finds 3 classes in the data.
       - Many, many more ...



```python
# Simple quantization, maps each value to which quantile it belongs
def quantize(x, n_intervals=3):
    p = np.percentile(x, np.linspace(0, 100, num=(n_intervals+1)))
    return np.array([max(sum(xi > p), 1) for xi in x])
```


```python
# Discretize features using simple quantile encoding, since we are
# implementing a multinomial version of the naive Bayes
for feature in range(X.shape[1]):
    X[:, feature] = quantize(X[:, feature], n_quantiles)
X = X.astype(int)
```


```python
# Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
print("Num. train instances:", len(X_train))
print("Num. test instances:", len(X_test))
print("Num. features:", X.shape[1])
```

    Num. train instances: 100
    Num. test instances: 50
    Num. features: 4



```python
# Num. insances, num. features and num. classes
classes = np.unique(y)
n, d, C = X_train.shape[0], X_train.shape[1], len(classes)

# Laplace smoothing factor
alpha = 1
```

## Training

We first compute the class distribution:

$$P(y_i = c) = \frac{n_c + \alpha}{n + C\alpha}$$

Where $c \in \{1, \dots, C\}$, $n_c$ is the number of examples in class $c$, $n$ is the total number of instances and $\alpha$ is the Laplace smoothing factor.


```python
# We store the class probabilites in this dictionary
class_probs = {}

# We compute each probability according to the formula above
for c in classes:
    class_probs[c] = (np.array(y_train == c).sum() + alpha) / (n + C*alpha)
```

Now, we compute the feature probabilities given the class:

$$P(X_{i, j} = x \mid y_i = c) = \frac{n_{j,x,c} + \alpha}{n_{c} + Q_j\alpha}$$

Where the feature $X_{i,j}$ is the $j$-th feature for the $i$-th instance, $y_i = c$ means the $i$-th instance is of class $c$, $n_{j,x,c}$ is the count of how many times the $j$-th feature had the value $x$ among instances of class $c$; $n_{c}$ is the number of instances in class $c$ and $Q_j$ is the number of possible values for the $j$-th feature.


```python
# First, we get the list of possible values for each feature:
possible_values = [set(X_train[:, feature]) for feature in range(d)]

# We will store these probabilities in this dictionary
# The key of the dictionary is a pair of (feature, class) such that:
#   feature_probs[j, c]  
# gives a dictionary which maps each possible value of the j-th feature to 
# its probability, given each class, as we saw in the formula above, i.e.
# P(X_{i,j} = x | y_i = c) can be obtained from: feature_probs[j, c][k]
feature_probs = {(j, c): {v: 0 for v in possible_values[j]} 
                 for c in classes for j in range(d)}

# Now, we compute the above probabilites, for each feature, given each class
for j in range(d):
    for c in classes:
        # This gives us the j-th feature of instances in class c
        in_class_c = X_train[y_train == c, j]
        for x in possible_values[j]:
            numerator = sum(in_class_c == x) + alpha
            denominator = len(in_class_c) + len(possible_values[j])*alpha
            feature_probs[j, c][x] = numerator / denominator
```

This completes the training process. Now, we move to the testing!

## Testing

To test, we have to find the class for a new instance, given its features:

$$
P(y_i = c \mid \boldsymbol X_i) = \frac{P(y_i = c)P(\boldsymbol X_i \mid y_i = c)}{P(\boldsymbol X_i)}
$$

Which, thanks to the "naive" independence assumption is given as (where $\propto$ means "proportional to"):
$$
P(y_i = c \mid \boldsymbol X_i) \propto P(y_i = c)\prod_{j=1}^{d}P(X_{i,j} \mid y_i = c)
$$

We can use the *maximum a posteriori* (MAP) estimator to get our class prediction:

$$
\hat{y_i} = \underset{c \in \{1, \dots, C\}}{\operatorname{argmax}} P(y_i = c \mid \boldsymbol X_i)  = \underset{c \in \{1, \dots, C\}}{\operatorname{argmax}}
P(y_i = c)\prod_{j=1}^{d}P(X_{i,j} \mid y_i = c)
$$


```python
test_size = len(X_test)
y_pred = []

for i in range(test_size):
    posterior_prob = {c: 0 for c in classes}
    y_max = classes[0]
    
    for c in classes:
        # Compute the posterior prob. for class c
        posterior_prob[c] = class_probs[c]
        for j in range(d):
            x = X_test[i, j]
            posterior_prob[c] *= feature_probs[j, c][x]
            
        # Update which class has the max posterior
        if posterior_prob[c] >= posterior_prob[y_max]:
            y_max = c
    y_pred.append(y_max)
```


```python
print(classification_report(y_test, y_pred))
```

                  precision    recall  f1-score   support
    
          setosa       1.00      1.00      1.00        15
      versicolor       0.80      0.92      0.86        13
       virginica       0.95      0.86      0.90        22
    
        accuracy                           0.92        50
       macro avg       0.92      0.93      0.92        50
    weighted avg       0.93      0.92      0.92        50
    

