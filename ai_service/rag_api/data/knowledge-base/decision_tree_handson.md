# CS37300 - Data Mining and Machine Learning
### Instructor: Bruno Ribeiro
### Notes: Bruno Ribeiro and Bonan Kou

# Hands-on: Decision Trees

## Learning Objectives
In this lecture, we will cover:
1. Working with data in python.
2. Featurizing a dataset for learning with decision trees.
3. Hyperparameter search with cross-validation.
4. Testing model performance.

## Key Components

* **Task Specification**
    * This is a **supervised classification** task. We have labeled examples (e.g., loan applications where we know if they were repaid or not) and we want to build a model to predict the class (repaid or not repaid) for new, unseen loan applications.
    * **Instances:** Each row in our data represents a customer applying for a loan.
    * **Features:** Customer features $X$ that we will be able to see in test.
    * **Target Variable:** Whether the customer repaid the loan ($Y=\{\text{yes},\text{no}\}$ or $Y=\{1,0\}$).

* **Data representation: Tabular data**
    * Each row is a customer (an instance).
    * Each column is a piece of information about them (an attribute or feature), like income, credit score, employment status, etc. 
    * We have 'p' such attributes.
    * The last column is the target variable (repaid or not).
* **Knowledge Representation: Decision Trees** 
    * Each internal node (box) is a question about an attribute (e.g., "Is income $> 50,000$?", "What is the FICO range?").
    * Each branch is an answer to the question (yes or no, "[660-664,665-669,670-674,...,835-840]")
    * Each leaf is a decision (repaid or not repaid).
    * **Model space is the set of all trees split over all possible attribute values**

* **Learning Method: Greedy Search**
    * We build the tree from the top down.
    * At each node, we find the best split based on our scoring function.
    * We're "greedy" because we make the best choice at each step, which could be suboptimal.
* **Search + Scoring**
    * **Score Functions:** These help us measure how good a question is at splitting the data. Popular choices are:
        * **Gini Gain:**  Favors splits that create groups where most instances belong to the same class (less "impure").
        * **Information Gain:** Favors splits that reduce uncertainty about the class.
    * **Greedy Search:** We try all possible questions on all attributes and pick the one with the highest score.
* **Prediction and Interpretation**
    * For a new loan application, we start at the top of the tree and follow the branches based on the customer's information until we reach a leaf, which gives a set of labels from which we will predict the outcome (repaid or not repaid).
    * Decision trees are interpretable because we can easily trace the path to understand *why* a certain prediction was made.

**Example**

We have data on customers applying for loans, with attributes like income, amount requested, credit score, and employment status. We can build a decision tree to predict whether a new applicant will be approved or denied. The tree might look something like this:

```text
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

### Data Preparation and Exploration

We've been provided with two CSV files:

* [Bank_Data_Train.csv](Bank_Data_Train.csv): This contains the data we will use to train (build) our decision tree.
* [Bank_Data_Test.csv](Bank_Data_Test.csv):  This contains the data we will use to evaluate how well our tree generalizes to new, unseen examples. 

**Let's inspect the data**


```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
import numpy as np
```


```python
import pandas as pd
train = pd.read_csv("Bank_Data_Train.csv")
test = pd.read_csv("Bank_Data_Test.csv")
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
      <th>Record Number</th>
      <th>Amount Requested</th>
      <th>Interest Rate Percentage</th>
      <th>Loan Length in Months</th>
      <th>Loan Title</th>
      <th>Loan Purpose</th>
      <th>Monthly PAYMENT</th>
      <th>Total Amount Funded</th>
      <th>Debt-To-Income Ratio Percentage</th>
      <th>FICO Range</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>1000</td>
      <td>17.49</td>
      <td>36</td>
      <td>Living</td>
      <td>moving</td>
      <td>35.90</td>
      <td>1000</td>
      <td>20.40</td>
      <td>680-684</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0</td>
      <td>1000</td>
      <td>14.09</td>
      <td>36</td>
      <td>PAY MY CREDIT CARD</td>
      <td>credit_card</td>
      <td>34.23</td>
      <td>1000</td>
      <td>1.37</td>
      <td>710-714</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0</td>
      <td>1000</td>
      <td>13.57</td>
      <td>36</td>
      <td>Apartment Initiative</td>
      <td>other</td>
      <td>33.97</td>
      <td>1000</td>
      <td>14.00</td>
      <td>680-684</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0</td>
      <td>1000</td>
      <td>11.48</td>
      <td>36</td>
      <td>meds</td>
      <td>medical</td>
      <td>32.97</td>
      <td>1000</td>
      <td>11.57</td>
      <td>700-704</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0</td>
      <td>1000</td>
      <td>11.99</td>
      <td>36</td>
      <td>Maine Getaway</td>
      <td>vacation</td>
      <td>33.21</td>
      <td>1000</td>
      <td>4.39</td>
      <td>685-689</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



#### Converting FICO ranges into two integer features.
- The FICO score of a person is a three-digit number, typically ranging from 300 to 850, that represents a person's creditworthiness based on their credit history.
- FICO scores are described in ranges in our dataset: [660-664,665-669,670-674,...,845-850]
- Trees can have nodes with multiple children.
    - That is, we do not necessarily need to make the FICO scores integer variables.
- But integers should help, since any decision for a FICO score in the range [800,805] should also be true for FICO scores $> 800$.
- Therefore, we want to convert FICO Range into two separate integer features, `FICO_range_upper` and `FICO_range_lower`.


```python
def convert_fico_range(data):
    data[['FICO_range_lower', 'FICO_range_upper']] = data['FICO Range'].str.split('-', expand=True)

    data['FICO_range_lower'] = data['FICO_range_lower'].astype(int)
    data['FICO_range_upper'] = data['FICO_range_upper'].astype(int)

    data = data.drop(columns=['FICO Range'])
    return data

train = convert_fico_range(train)
test = convert_fico_range(test)

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
      <th>Record Number</th>
      <th>Amount Requested</th>
      <th>Interest Rate Percentage</th>
      <th>Loan Length in Months</th>
      <th>Loan Title</th>
      <th>Loan Purpose</th>
      <th>Monthly PAYMENT</th>
      <th>Total Amount Funded</th>
      <th>Debt-To-Income Ratio Percentage</th>
      <th>Status</th>
      <th>FICO_range_lower</th>
      <th>FICO_range_upper</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>1000</td>
      <td>17.49</td>
      <td>36</td>
      <td>Living</td>
      <td>moving</td>
      <td>35.90</td>
      <td>1000</td>
      <td>20.40</td>
      <td>0</td>
      <td>680</td>
      <td>684</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0</td>
      <td>1000</td>
      <td>14.09</td>
      <td>36</td>
      <td>PAY MY CREDIT CARD</td>
      <td>credit_card</td>
      <td>34.23</td>
      <td>1000</td>
      <td>1.37</td>
      <td>0</td>
      <td>710</td>
      <td>714</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0</td>
      <td>1000</td>
      <td>13.57</td>
      <td>36</td>
      <td>Apartment Initiative</td>
      <td>other</td>
      <td>33.97</td>
      <td>1000</td>
      <td>14.00</td>
      <td>0</td>
      <td>680</td>
      <td>684</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0</td>
      <td>1000</td>
      <td>11.48</td>
      <td>36</td>
      <td>meds</td>
      <td>medical</td>
      <td>32.97</td>
      <td>1000</td>
      <td>11.57</td>
      <td>0</td>
      <td>700</td>
      <td>704</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0</td>
      <td>1000</td>
      <td>11.99</td>
      <td>36</td>
      <td>Maine Getaway</td>
      <td>vacation</td>
      <td>33.21</td>
      <td>1000</td>
      <td>4.39</td>
      <td>0</td>
      <td>685</td>
      <td>689</td>
    </tr>
  </tbody>
</table>
</div>



### Dataset split
Just like what we did in the previous hand-on lecture on KNN, we want to use 20% of train dataset as validation dataset.


```python
from sklearn.model_selection import train_test_split

train, validation = train_test_split(train, test_size=0.2, random_state=4)

print('Train set:', train.shape)
print('Validation set:', validation.shape)
```

    Train set: (2400, 12)
    Validation set: (600, 12)


## Score Functions: Guiding the Splits

A crucial step in training a decision tree is selecting the right feature to split the data at each node. 
- Score functions help us quantify how "good" a potential split is, guiding the tree's growth towards better predictive power. 
- We will implement three common score functions: **Information Gain**, **Weighted Gini Gain**, and **Chi-Square Score**.
<br><br>

### 1. Information Gain: Measuring Uncertainty Reduction
Information Gain measures how much a split reduces uncertainty about the class labels in the resulting branches. To understand it, we first need to grasp the concept of **Entropy**.

#### Entropy: Measuring Disorder

Entropy quantifies the impurity or disorder within a dataset. Think of it as how mixed up the different classes are. 

* **Formula**: 
$$
\text{Entropy}(S) = - \sum_{i=1}^{C} p_i \log_2(p_i)
$$

Where:
- $ S $ is the original dataset,
- $ p_i $ is the proportion of elements in class \( i \),
- $ C $ is the number of classes.

#### Information Gain

Information Gain calculates the decrease in entropy achieved by splitting the data on a particular attribute.

* **Formula**:
$$
\text{Information Gain}(S, A) = \text{Entropy}(S) - \sum_{v \in \text{Values}(A)} \frac{|S_v|}{|S|} \text{Entropy}(S_v),
$$
where:
- $ \text{Information Gain}(S, A) $ is the information gain after splitting on attribute $ A $,
- $ S_v $ is the subset of $ S $ where attribute $ A $ has value $ v $,
- $ \frac{|S_v|}{|S|} $ is the proportion of subset $ S_v $ to the total dataset $ S $,
- $ \text{Entropy}(S_v) $ is the entropy of the subset $ S_v $.
High entropy means the classes are well mixed; low entropy indicates a more homogenous set of instances.

**Summary:** 
- To measure the Information Gain of a split by calculating the weighted average entropy of the subsets created by the split and subtract it from the original entropy.
- A larger Information Gain indicates a more informative split. 


```python
# Suppose we are given an orignal dataset and a list of dataframes 
# that result from a split (if we always split the dataset into two 
# portions, this list will contain 2 elements).

def entropy(data):
    class_counts = data["Status"].value_counts(normalize=True)
    return -sum(class_counts * np.log2(class_counts))

def information_gain(original_dataset, groups):
    original_entropy = entropy(original_dataset)

    total_size = sum(len(group) for group in groups)
    weighted_entropy = 0

    for group in groups:
        group_size = len(group)
        if group_size == 0:
            continue
        group_entropy = entropy(group)
        weighted_entropy += (group_size / total_size) * group_entropy

    info_gain = original_entropy - weighted_entropy
    return info_gain
```

### 2. Weighted Gini Gain

Now, let's calculate the Gini Gain using the Weighted Gini Index. Before that, let's revisit the concept of Gini Impurity.

### Gini Impurity

Gini Impurity measures the probability of misclassifying a randomly chosen element in a dataset if it were randomly labeled according to the class distribution in the dataset.
$$
\text{Gini}(S) = 1 - \sum_{i=1}^{C} p_i^2
$$

Where:
- $p_i$ is the proportion of elements in class $i$,
- $C$ is the number of classes.

A Gini Impurity of 0 indicates a perfectly pure node (all instances belong to the same class), while a higher value signifies more impurity or disorder.

### Weighted Gini Index

After splitting the dataset on attribute 'A', we calculate the Weighted Gini Index to assess the overall impurity of the resulting groups, considering their sizes.
$$
\text{Weighted Gini}(S, A) = \sum_{v \in \text{Values}(A)} \frac{|S_v|}{|S|} \text{Gini}(S_v),
$$
where:
- $S$ is the original dataset,
- $A$ is the attribute you split on,
- $S_v$ is the subset of $S$ where attribute $A$ has value $v$,
- $\frac{|S_v|}{|S|}$ is the proportion of subset $S_v$ to the total dataset $S$,
- $\text{Gini}(S_v)$ is the Gini index of the subset $S_v$.

### Gini Gain

Finally, the Gini Gain quantifies the reduction in impurity achieved by the split.
$$
\text{Gini Gain}(S, A) = \text{Gini}(S) - \text{Weighted Gini}(S, A),
$$
where:
- $\text{Gini}(S)$ is the Gini impurity of the original dataset,
- $\text{Weighted Gini}(S, A)$ is the weighted Gini index of the groups after splitting on attribute $A$.

A higher Gini Gain implies a more effective split in terms of creating purer subsets.

**Summary:** 
- The Weighted Gini Index and Gini Gain provide a way to assess the quality of a split based on how much it reduces impurity in the resulting children.


```python
# Suppose we are given an orignal dataset and a list of dataframes 
# that result from a split (if we always split the dataset into two 
# portions, this list will contain 2 elements).

def gini_index(data):
    class_counts = data["Status"].value_counts(normalize=True)
    gini = 1 - sum(class_counts ** 2)
    return gini

def weighted_gini_index(original_dataset, groups):
    original_gini = gini_index(original_dataset)

    total_size = len(original_dataset)
    weighted_gini = 0

    for group in groups:
        group_size = len(group)
        if group_size == 0:
            continue
        group_gini = gini_index(group)
        weighted_gini += (group_size / total_size) * group_gini

    return original_gini - weighted_gini
```

### 3. Chi-Square Score: Measuring Statistical Significance

Finally, let's explore the Chi-Square Score as a criterion for splitting in decision trees. 
- The Chi-Square statistic quantifies the discrepancy between observed frequencies (in the split subsets) and expected frequencies (assuming independence between the attribute and the class), normalized by the expected frequencies.

**Chi-Square Statistic**
$$
\chi^2 = \sum \frac{(O_i - E_i)^2}{E_i},
$$
where:
- $O_i$ is the observed frequency for category $i$,
- $E_i$ is the expected frequency for category $i$ (the porportion of category $i$ in the original dataset),
- The sum is taken over all categories.

A high Chi-Square statistic suggests a strong association between the attribute and the target class, indicating a potentially informative split.

**Chi-Square Gain**
Now, we can calculate the Chi-Square Gain for the attribute $A$. The higher the Chi-Square value, the more significant the attribute $A$ is in predicting the target class, and therefore, a better split. 
$$
\text{Chi-Square Gain}(S, A) = \chi^2(S, A).
$$

**Testing Statistical Significance**

To determine if the observed Chi-Square value is statistically significant, we compare it to a critical value from the Chi-Square distribution with the appropriate degrees of freedom. The degrees of freedom are calculated as `df=(number of rows - 1) * (number of columns - 1)` in the contingency table representing the split.

* If the calculated Chi-Square value is greater than the critical value, we reject the null hypothesis (that the attribute and the class are independent) and conclude that the split is statistically significant.
* Otherwise, we fail to reject the null hypothesis and consider the split less informative.

**Summary:** 
- The Chi-Square Score provides a statistical approach to evaluate splits, favoring those that exhibit a strong association between the attribute and the target class. 
- By testing for statistical significance, we can further ensure that the selected splits are meaningful and contribute to a decision tree with improved predictive capabilities.


```python
# Suppose we are given an orignal dataset and a list of dataframes 
# that result from a split (if we always split the dataset into two 
# portions, this list will contain 2 elements).

def chi_square(original_dataset, groups):
    total_size = len(original_dataset)
    class_totals = original_dataset["Status"].value_counts(normalize=True)
    
    chi_square_stat = 0
    
    for group in groups:
        group_size = len(group)
        if group_size == 0:
            continue

        observed_counts = group.iloc[:, -1].value_counts()
        
        expected_counts = class_totals * group_size
        
        for class_value in class_totals.index:
            observed = observed_counts.get(class_value, 0)
            expected = expected_counts[class_value]
            
            if expected > 0:
                chi_square_stat += (observed - expected) ** 2 / expected
    
    return chi_square_stat
```

### Finding the p-value for Chi-Square Statistic

- A p-value is a key statistical measure that helps us assess the significance of our empirical metrics. 
- It essentially tells us the probability of observing an empirical metric (or even more extreme results) if the null hypothesis were true. 
- In the context of decision tree splits, the null hypothesis states:
    - **The feature used to split the data does not provide any meaningful information about the target variable (i.e., they are independent).**

- To calculate the p-value, we need to consider the degrees of freedom (`df`) in our data. 
    - `df` refers to the number of independent values that can vary in our statistical calculation. 
        - In a binary decision tree split, each split divides the data into two groups. Consequently, the degrees of freedom for the Chi-Square test in this scenario is typically 1.

**How to Calculate the p-value of a  Chi-Square Statistic**

1. **Calculate the Chi-Square Statistic:**  Use the formula mentioned previously to compute the Chi-Square statistic for the split.

2. **Determine Degrees of Freedom:** In most binary splits, df = 1. However, if you have more than two categories in the attribute being split, the `df=(number of rows - 1) * (number of columns - 1)` in the contingency table representing the split.

3. **Use a Chi-Square Distribution Table or Statistical Software:**  
   - With the calculated Chi-Square value and degrees of freedom, consult a Chi-Square distribution table or use statistical software (like Python's `scipy.stats.chi2.sf`) to find the corresponding p-value.

**Interpretation**

* **Small p-value (typically < 0.05):** This suggests strong evidence against the null hypothesis. We can conclude that the split is statistically significant, and the feature likely provides meaningful information about the target variable.

* **Large p-value:**  This indicates weak evidence against the null hypothesis. The split might not be statistically significant, suggesting the feature might not be very useful for predicting the target variable.


```python
from scipy.stats import chi2

def p_value(chi_square_score, degree_of_freedom):
    p_val = chi2.sf(chi_square_score, degree_of_freedom)
    return p_val
```

Let's perform a test. For the given dataframe below, let's calculate the different gains after splitting the dataset on feature 1.


```python
import pandas as pd
import numpy as np

data = pd.DataFrame({
    'Feature1': [1, 2, 1, 2, 1, 2, 1, 2],
    'Feature2': [5, 6, 7, 8, 9, 10, 11, 12],
    'Status': [0, 1, 0, 1, 0, 1, 0, 1]
})

group1 = data[data['Feature1'] == 1]
group2 = data[data['Feature1'] == 2]

groups = [group1, group2]

info_gain = information_gain(data, groups)
print(f"Information Gain: {info_gain:.4f}")

gini_gain = weighted_gini_index(data, groups)
print(f"Gini Gain: {gini_gain:.4f}")

chi_gain = chi_square(data, groups)
print(f"Chi-square Gain: {chi_gain:.4f}")

p_value = p_value(chi_gain, 1)
print(f"Chi-square score {chi_gain} has a p-value of {p_value}")
```

    Information Gain: 1.0000
    Gini Gain: 0.5000
    Chi-square Gain: 8.0000
    Chi-square score 8.0 has a p-value of 0.004677734981047265


# Quiz!
We performed a chi-square test after splitting on feature 1, resulting in a p-value of 0.0046. 
- A. The p-value is 0.46% means the feature is probably independent of the target "status" and we should NOT split on feature 1.
- B. The p-value is 0.46% means the feature is unlikely to be independent of the target "status" and we should split on feature 1.
- C. It does not tell us anything because p-values are not reliable.

### Building the tree
Now we can proceed to build the tree from the training dataset. 
- We will first define the `Tree` and `Node` classes.


```python
class Node():
    def __init__(self, feature=None, threshold=None, data=None, left=None, right=None, *, value=None):
        self.feature = feature
        self.threshold = threshold
        self.data = data
        self.left = left
        self.right = right
        self.value = value

    def is_leaf_node(self):
        return self.value is not None
```


```python
from sklearn.metrics import classification_report

class Tree():
    def __init__(self):
        self.root = None

    def split_numerical_dataset(self, dataset, feature, threshold):
        left = dataset[dataset[feature] <= threshold]
        right = dataset[dataset[feature] > threshold]
        return left, right

    def split_categorical_dataset(self, dataset, feature, category):
        left = dataset[dataset[feature] == category]
        right = dataset[dataset[feature] != category]
        return left, right

    def build_decision_tree(self, train_data, gain_function):
        best_feature = None
        best_threshold = None
        best_gain = -1
        best_split = None

        for feature in train_data.columns:
            if feature == 'Status':
                continue
            
            if pd.api.types.is_numeric_dtype(train_data[feature]):
                unique_values = train_data[feature].unique()
                for value in unique_values:
                    left, right = self.split_numerical_dataset(train_data, feature, value)
                    gain = gain_function(train_data, [left, right])

                    if gain > best_gain:
                        best_gain = gain
                        best_feature = feature
                        best_threshold = value
                        best_split = (left, right)
            else:
                unique_categories = train_data[feature].unique()
                for category in unique_categories:
                    left, right = self.split_categorical_dataset(train_data, feature, category)
                    gain = gain_function(train_data, [left, right])

                    if gain > best_gain:
                        best_gain = gain
                        best_feature = feature
                        best_threshold = category
                        best_split = (left, right)

        return best_feature, best_threshold, best_split

    def build(self, train, gain_function, depth=0, max_depth=None):
        X = train.drop(columns=['Status'])
        y = train["Status"]

        if len(y.unique()) == 1:
            return Node(value=y.mode().iloc[0], data=train)

        if max_depth is not None and depth >= max_depth:
            return Node(value=y.mode().iloc[0], data=train)
        
        best_feature, best_threshold, (left_dataset, right_dataset) = self.build_decision_tree(train, gain_function)
        
        left_child = self.build(left_dataset, gain_function, depth + 1, max_depth)
        right_child = self.build(right_dataset, gain_function, depth + 1, max_depth)

        return Node(feature=best_feature, threshold=best_threshold, data=train, left=left_child, right=right_child)

    def fit(self, train_data, gain_function, max_depth=None):
        self.root = self.build(train_data, gain_function, max_depth=max_depth)

    def predict_row(self, row, node):
        if node.is_leaf_node():
            return node.value
        
        if node.feature not in ["Loan Title", "Loan Purpose"]:
            if row[node.feature] <= node.threshold:
                return self.predict_row(row, node.left)
            else:
                return self.predict_row(row, node.right)
        else:
            if row[node.feature] == node.threshold:
                return self.predict_row(row, node.left)
            else:
                return self.predict_row(row, node.right)

    def predict(self, test, print_accuracy=True):
        X = test.drop(columns=['Status'])
        ground_truth = list(test["Status"])
        predictions = [self.predict_row(row, self.root) for _, row in X.iterrows()]
        if print_accuracy:
            print(classification_report(ground_truth, predictions))
        return ground_truth, predictions
```

Because training each decision tree takes about 3 minutes, we trained the models in advance and used the pickled version here. If you are interested, comment the following lines to run by yourself.


```python
import pickle

print("Building trees...",end="")

information_gain_decision_tree = Tree()
information_gain_decision_tree.fit(train, information_gain)
pickle.dump(information_gain_decision_tree, open("information_gain_decision_tree.pkl", "wb"))
#information_gain_decision_tree = pickle.load(open("information_gain_decision_tree.pkl", "rb"))

gini_gain_decision_tree = Tree()
gini_gain_decision_tree.fit(train, information_gain)
pickle.dump(gini_gain_decision_tree, open("gini_gain_decision_tree.pkl", "wb"))
#gini_gain_decision_tree = pickle.load(open("gini_gain_decision_tree.pkl", "rb"))

chi_square_decision_tree = Tree()
chi_square_decision_tree.fit(train, information_gain)
pickle.dump(chi_square_decision_tree, open("chi_square_decision_tree.pkl", "wb"))
#chi_square_decision_tree = pickle.load(open("chi_square_decision_tree.pkl", "rb"))

print("done.")
```

    Building trees...done.


#### Validate our trees
Now we can use the decision trees to predict for the validation set.


```python
print("Information gain...")
information_gain_tree_predictions = information_gain_decision_tree.predict(test)
print("Gini gain...")
gini_gain_tree_predictions = gini_gain_decision_tree.predict(test)
print("Chi-square...")
chi_square_tree_predictions = chi_square_decision_tree.predict(test)
```

    Information gain...
                  precision    recall  f1-score   support
    
               0       0.54      0.51      0.52       221
               1       0.60      0.63      0.62       261
    
        accuracy                           0.57       482
       macro avg       0.57      0.57      0.57       482
    weighted avg       0.57      0.57      0.57       482
    
    Gini gain...
                  precision    recall  f1-score   support
    
               0       0.54      0.51      0.52       221
               1       0.60      0.63      0.62       261
    
        accuracy                           0.57       482
       macro avg       0.57      0.57      0.57       482
    weighted avg       0.57      0.57      0.57       482
    
    Chi-square...
                  precision    recall  f1-score   support
    
               0       0.54      0.51      0.52       221
               1       0.60      0.63      0.62       261
    
        accuracy                           0.57       482
       macro avg       0.57      0.57      0.57       482
    weighted avg       0.57      0.57      0.57       482
    


### Tree Pruning
We can see that the trees are not very effective on validation data. This could be due to that we are overfitting the train set. Therefore, we want to prune the trees to make it more light-weight and generalize better.

#### Pruning the Gini tree
The first pruning method we are going to try is to prune the tree by setting a threshold for Gini index. For every node, we stop splitting when the Gini index is below a threshold. To determine the threshold, we are going to cross-validate on the validation set and try every Gini index we have seen while training the tree.

First, let's get all the gini indices we have seen by doing a pre-order traversal.


```python
all_gini_indices = []

def pre_order_traversal(node):
    if node.data is not None:
        gini_index_value = gini_index(node.data)
        all_gini_indices.append(gini_index_value)

    if node.value is None:
        pre_order_traversal(node.left)
        pre_order_traversal(node.right)

pre_order_traversal(gini_gain_decision_tree.root)
all_gini_indices = list(set(all_gini_indices))
```


```python
def prune_node_by_gini(node, threshold):
    if node.data is not None:
        gini_index_value = gini_index(node.data)

        if gini_index_value <= threshold:
            node.value = node.data["Status"].mode().iloc[0]
            node.left = None
            node.right = None

        if node.value is None:
            prune_node_by_gini(node.left, threshold)
            prune_node_by_gini(node.right, threshold)
```

This part of the code takes about 90 seconds to run.


```python
import copy
from sklearn.metrics import accuracy_score

def prune_by_gini(all_gini_indices, tree):
    best_accuracy = -1
    best_gini = 0
    best_tree = None
    
    for candidate in all_gini_indices:
        pruned_tree = copy.deepcopy(tree)
        prune_node_by_gini(pruned_tree.root, candidate)
        groundtruth, predictions = pruned_tree.predict(validation, False)
        validation_accuracy = accuracy_score(groundtruth, predictions)
        if validation_accuracy > best_accuracy:
            best_gini = candidate
            best_tree = pruned_tree
            best_accuracy = validation_accuracy
    
    groundtruth, predictions = best_tree.predict(test, False)
    test_accuracy = accuracy_score(groundtruth, predictions)

    groundtruth, predictions = tree.predict(validation, False)
    original_validation_accuracy = accuracy_score(groundtruth, predictions)

    groundtruth, predictions = tree.predict(test, False)
    original_test_accuracy = accuracy_score(groundtruth, predictions)

    print(f"Before pruning, achieved {original_validation_accuracy:.2f} accuracy on validation set, {original_test_accuracy:.2f} on test set.")
    print(f"Cross-validation results: Best Gini gain for prunning is {best_gini:.2f}. it achieves {best_accuracy:.2f} accuracy on validation set, and {test_accuracy:.2f} on test set.")

    return best_tree, best_gini, best_accuracy, test_accuracy

pruned_tree_by_gini, _, _, _ = prune_by_gini(all_gini_indices, gini_gain_decision_tree)
```

    Before pruning, achieved 0.56 accuracy on validation set, 0.57 on test set.
    Cross-validation results: Best Gini gain for prunning is 0.49. it achieves 0.64 accuracy on validation set, and 0.64 on test set.


#### Pruning the Information gain tree
The second pruning method we are going to try is to prune the tree by monitoring the error rate, i.e., whether the model is making less errors when some nodes are pruned. We are going to use the information gain tree to do this task.


```python
import copy

def prune_node_by_error(node, relevant_validation_data):
    common_vote = node.data["Status"].mode().iloc[0]
    error_if_remove_children = len(relevant_validation_data[relevant_validation_data['Status'] != common_vote])

    if node.value is not None:
        return error_if_remove_children
    else:
        if node.feature not in ["Loan Title", "Loan Purpose"]:
            left = relevant_validation_data[relevant_validation_data[node.feature] <= node.threshold]
            right = relevant_validation_data[relevant_validation_data[node.feature] > node.threshold]
        else:
            left = relevant_validation_data[relevant_validation_data[node.feature] == node.threshold]
            right = relevant_validation_data[relevant_validation_data[node.feature] != node.threshold]
        error_if_keep_children = prune_node_by_error(node.left, left) + prune_node_by_error(node.right, right)

    if error_if_remove_children <= error_if_keep_children:
        node.left = None
        node.right = None
        node.value = common_vote

    return min(error_if_remove_children, error_if_keep_children)

pruned_tree_by_error = copy.deepcopy(information_gain_decision_tree)
_ = prune_node_by_error(pruned_tree_by_error.root, validation)
```


```python
groundtruth, predictions = pruned_tree_by_error.predict(validation, False)
validation_accuracy = accuracy_score(groundtruth, predictions)

groundtruth, predictions = pruned_tree_by_error.predict(test, False)
test_accuracy = accuracy_score(groundtruth, predictions)

groundtruth, predictions = information_gain_decision_tree.predict(validation, False)
original_validation_accuracy = accuracy_score(groundtruth, predictions)

groundtruth, predictions = information_gain_decision_tree.predict(test, False)
original_test_accuracy = accuracy_score(groundtruth, predictions)

print(f"Before pruning, achieved {original_validation_accuracy:.2f} accuracy on validation set, {original_test_accuracy:.2f} on test set.")
print(f"After pruning, achieved {validation_accuracy:.2f} accuracy on validation set, {test_accuracy:.2f} on test set.")
```

    Before pruning, achieved 0.56 accuracy on validation set, 0.57 on test set.
    After pruning, achieved 0.68 accuracy on validation set, 0.60 on test set.


### Visualizing the tree
Finally, we want to visualize trees.


```python
def print_tree(node, depth=0):
    if node.value is None:
        if node.feature not in ["Loan Title", "Loan Purpose"]:
            print(f"{depth*'  '}[{node.feature} <= {node.threshold}]")
            print_tree(node.left, depth+1)
            print_tree(node.right, depth+1)
        else:
            print(f"{depth*'  '}[{node.feature} == {node.threshold}]")
            print_tree(node.left, depth+1)
            print_tree(node.right, depth+1)
    else:
        print(f'%s[%s]' % ((depth*'  ', node.value)))
```


```python
print("Original Gini tree:")
print_tree(gini_gain_decision_tree.root)
```

    Original Gini tree:
    [Interest Rate Percentage <= 10.74]
      [Debt-To-Income Ratio Percentage <= 10.97]
        [FICO_range_lower <= 760]
          [Debt-To-Income Ratio Percentage <= 10.54]
            [Loan Title == Debt consolidation]
              [0]
              [Amount Requested <= 20000]
                [Loan Title == personal loan]
                  [0]
                  [Monthly PAYMENT <= 324.07]
                    [Monthly PAYMENT <= 292.01]
                      [Interest Rate Percentage <= 10.62]
                        [FICO_range_lower <= 685]
                          [1]
                          [Monthly PAYMENT <= 286.4]
                            [FICO_range_lower <= 730]
                              [Monthly PAYMENT <= 195.27]
                                [Loan Purpose == other]
                                  [FICO_range_lower <= 700]
                                    [0]
                                    [FICO_range_lower <= 720]
                                      [1]
                                      [Amount Requested <= 4800]
                                        [0]
                                        [1]
                                  [Debt-To-Income Ratio Percentage <= 6.0]
                                    [Monthly PAYMENT <= 187.69]
                                      [Debt-To-Income Ratio Percentage <= 3.0]
                                        [1]
                                        [Loan Title == LoantoLee]
                                          [1]
                                          [0]
                                      [1]
                                    [1]
                                [Monthly PAYMENT <= 248.37]
                                  [FICO_range_lower <= 690]
                                    [1]
                                    [Loan Title == Debt Consolidation]
                                      [1]
                                      [Loan Title == Ring]
                                        [1]
                                        [0]
                                  [1]
                              [Debt-To-Income Ratio Percentage <= 10.48]
                                [Interest Rate Percentage <= 9.32]
                                  [Monthly PAYMENT <= 139.55]
                                    [Interest Rate Percentage <= 7.29]
                                      [FICO_range_lower <= 740]
                                        [Loan Title == needing to pay off credit cards]
                                          [1]
                                          [0]
                                        [Loan Title == Medical]
                                          [0]
                                          [1]
                                      [1]
                                    [Interest Rate Percentage <= 7.74]
                                      [Debt-To-Income Ratio Percentage <= 5.77]
                                        [FICO_range_lower <= 755]
                                          [Interest Rate Percentage <= 6.62]
                                            [1]
                                            [Amount Requested <= 8000]
                                              [Loan Title == Debt Consolidation]
                                                [0]
                                                [1]
                                              [0]
                                          [0]
                                        [1]
                                      [FICO_range_lower <= 755]
                                        [Loan Title == Home Equity Payoff for Refinance]
                                          [1]
                                          [Loan Title == Loan to buy a car]
                                            [1]
                                            [0]
                                        [1]
                                  [1]
                                [0]
                            [0]
                        [1]
                      [Loan Title == Consolidate Debt to Start Business]
                        [0]
                        [1]
                    [Amount Requested <= 11000]
                      [0]
                      [Debt-To-Income Ratio Percentage <= 9.13]
                        [Debt-To-Income Ratio Percentage <= 6.21]
                          [1]
                          [Interest Rate Percentage <= 9.88]
                            [Debt-To-Income Ratio Percentage <= 8.35]
                              [FICO_range_lower <= 735]
                                [0]
                                [Loan Title == Debt Consolidation]
                                  [0]
                                  [1]
                              [1]
                            [0]
                        [1]
                [1]
            [1]
          [Loan Purpose == small_business]
            [Debt-To-Income Ratio Percentage <= 2.14]
              [1]
              [Amount Requested <= 25000]
                [0]
                [1]
            [Loan Title == Scooter loan]
              [0]
              [Interest Rate Percentage <= 7.29]
                [Loan Title == paint loan]
                  [0]
                  [1]
                [FICO_range_lower <= 765]
                  [1]
                  [Loan Purpose == home_improvement]
                    [1]
                    [Amount Requested <= 2650]
                      [0]
                      [Total Amount Funded <= 9600]
                        [Monthly PAYMENT <= 140.31]
                          [Monthly PAYMENT <= 101.1]
                            [1]
                            [0]
                          [1]
                        [Loan Purpose == other]
                          [0]
                          [Interest Rate Percentage <= 7.88]
                            [Amount Requested <= 12000]
                              [0]
                              [1]
                            [Debt-To-Income Ratio Percentage <= 2.34]
                              [Interest Rate Percentage <= 8.07]
                                [1]
                                [0]
                              [1]
        [Loan Purpose == major_purchase]
          [Debt-To-Income Ratio Percentage <= 11.65]
            [0]
            [1]
          [Monthly PAYMENT <= 80.88]
            [Monthly PAYMENT <= 58.26]
              [Interest Rate Percentage <= 9.76]
                [Interest Rate Percentage <= 6.62]
                  [1]
                  [Loan Title == Premier Refinance]
                    [1]
                    [Loan Title == Personal Loan]
                      [1]
                      [0]
                [1]
              [Amount Requested <= 2400]
                [Amount Requested <= 2050]
                  [0]
                  [Interest Rate Percentage <= 9.63]
                    [Debt-To-Income Ratio Percentage <= 18.68]
                      [1]
                      [Amount Requested <= 2200]
                        [1]
                        [0]
                    [0]
                [0]
            [Debt-To-Income Ratio Percentage <= 12.34]
              [Debt-To-Income Ratio Percentage <= 12.24]
                [FICO_range_lower <= 770]
                  [FICO_range_lower <= 725]
                    [Interest Rate Percentage <= 10.39]
                      [Loan Title == GAC Credit Card]
                        [0]
                        [1]
                      [Loan Title == Credit Consolidation]
                        [1]
                        [0]
                    [Interest Rate Percentage <= 8.49]
                      [Debt-To-Income Ratio Percentage <= 11.13]
                        [0]
                        [Amount Requested <= 9000]
                          [Loan Title == Concolidation]
                            [1]
                            [0]
                          [1]
                      [0]
                  [1]
                [0]
              [Debt-To-Income Ratio Percentage <= 12.74]
                [1]
                [Loan Title == Debt Consolidation Loan]
                  [Interest Rate Percentage <= 9.99]
                    [0]
                    [Amount Requested <= 9200]
                      [1]
                      [0]
                  [Loan Purpose == house]
                    [1]
                    [Monthly PAYMENT <= 93.31]
                      [1]
                      [Loan Purpose == credit_card]
                        [Debt-To-Income Ratio Percentage <= 17.71]
                          [Interest Rate Percentage <= 5.79]
                            [0]
                            [1]
                          [Debt-To-Income Ratio Percentage <= 25.29]
                            [Amount Requested <= 6000]
                              [0]
                              [Amount Requested <= 7200]
                                [1]
                                [FICO_range_lower <= 740]
                                  [Amount Requested <= 21500]
                                    [0]
                                    [1]
                                  [Interest Rate Percentage <= 6.92]
                                    [1]
                                    [0]
                            [1]
                        [Amount Requested <= 23000]
                          [Amount Requested <= 17000]
                            [Debt-To-Income Ratio Percentage <= 14.5]
                              [FICO_range_lower <= 705]
                                [1]
                                [FICO_range_lower <= 715]
                                  [Interest Rate Percentage <= 9.91]
                                    [0]
                                    [1]
                                  [Total Amount Funded <= 6600]
                                    [1]
                                    [Debt-To-Income Ratio Percentage <= 13.99]
                                      [Interest Rate Percentage <= 9.88]
                                        [Loan Purpose == debt_consolidation]
                                          [1]
                                          [Debt-To-Income Ratio Percentage <= 13.34]
                                            [0]
                                            [Amount Requested <= 7000]
                                              [0]
                                              [1]
                                        [0]
                                      [1]
                              [Amount Requested <= 15600]
                                [Interest Rate Percentage <= 10.71]
                                  [Interest Rate Percentage <= 9.88]
                                    [Interest Rate Percentage <= 5.99]
                                      [0]
                                      [Debt-To-Income Ratio Percentage <= 28.39]
                                        [Interest Rate Percentage <= 6.03]
                                          [1]
                                          [FICO_range_lower <= 705]
                                            [Interest Rate Percentage <= 7.66]
                                              [1]
                                              [0]
                                            [Interest Rate Percentage <= 6.62]
                                              [Interest Rate Percentage <= 6.39]
                                                [Loan Title == debt_consolidation]
                                                  [0]
                                                  [1]
                                                [0]
                                              [Interest Rate Percentage <= 6.99]
                                                [1]
                                                [Monthly PAYMENT <= 371.3]
                                                  [Amount Requested <= 6950]
                                                    [Monthly PAYMENT <= 187.08]
                                                      [Debt-To-Income Ratio Percentage <= 16.73]
                                                        [Interest Rate Percentage <= 7.88]
                                                          [0]
                                                          [1]
                                                        [Monthly PAYMENT <= 134.55]
                                                          [Amount Requested <= 4000]
                                                            [Debt-To-Income Ratio Percentage <= 20.33]
                                                              [Interest Rate Percentage <= 7.51]
                                                                [1]
                                                                [0]
                                                              [1]
                                                            [0]
                                                          [1]
                                                      [1]
                                                    [Amount Requested <= 11000]
                                                      [Monthly PAYMENT <= 168.49]
                                                        [0]
                                                        [Loan Purpose == debt_consolidation]
                                                          [Amount Requested <= 10000]
                                                            [Monthly PAYMENT <= 311.8]
                                                              [Monthly PAYMENT <= 247.53]
                                                                [Interest Rate Percentage <= 7.51]
                                                                  [0]
                                                                  [Loan Title == Consolidate debt]
                                                                    [0]
                                                                    [1]
                                                                [1]
                                                              [0]
                                                            [1]
                                                          [Monthly PAYMENT <= 251.88]
                                                            [0]
                                                            [Amount Requested <= 8500]
                                                              [1]
                                                              [Loan Title == High Tech Business Startup]
                                                                [1]
                                                                [Loan Title == other]
                                                                  [1]
                                                                  [0]
                                                      [0]
                                                  [Loan Title == Small Business Loan]
                                                    [0]
                                                    [1]
                                        [0]
                                    [Interest Rate Percentage <= 9.91]
                                      [0]
                                      [Loan Title == consolidation]
                                        [1]
                                        [Loan Title == Debt Consolidation]
                                          [1]
                                          [Debt-To-Income Ratio Percentage <= 19.13]
                                            [Interest Rate Percentage <= 10.38]
                                              [FICO_range_lower <= 695]
                                                [0]
                                                [Debt-To-Income Ratio Percentage <= 18.28]
                                                  [1]
                                                  [0]
                                              [0]
                                            [Interest Rate Percentage <= 9.99]
                                              [0]
                                              [Amount Requested <= 8000]
                                                [1]
                                                [Total Amount Funded <= 9900]
                                                  [0]
                                                  [Monthly PAYMENT <= 390.54]
                                                    [1]
                                                    [Loan Title == Debt loan]
                                                      [1]
                                                      [0]
                                  [Loan Title == Debt Consolidation]
                                    [0]
                                    [Loan Title == Home Improvement]
                                      [Amount Requested <= 8000]
                                        [0]
                                        [1]
                                      [1]
                                [1]
                            [1]
                          [Loan Title == Debt consolidation]
                            [1]
                            [0]
      [Interest Rate Percentage <= 15.8]
        [Loan Purpose == small_business]
          [Monthly PAYMENT <= 102.42]
            [1]
            [Debt-To-Income Ratio Percentage <= 17.88]
              [Monthly PAYMENT <= 171.92]
                [0]
                [Debt-To-Income Ratio Percentage <= 15.87]
                  [Debt-To-Income Ratio Percentage <= 11.07]
                    [Monthly PAYMENT <= 194.15]
                      [1]
                      [Debt-To-Income Ratio Percentage <= 6.14]
                        [Loan Length in Months <= 36]
                          [Debt-To-Income Ratio Percentage <= 3.6]
                            [Debt-To-Income Ratio Percentage <= 2.87]
                              [1]
                              [0]
                            [Loan Title == Need cash flow for 3 month. ]
                              [0]
                              [1]
                          [0]
                        [Debt-To-Income Ratio Percentage <= 9.77]
                          [0]
                          [Loan Title == Working Capital for Brewery]
                            [0]
                            [1]
                    [0]
                  [Amount Requested <= 10000]
                    [0]
                    [Amount Requested <= 18000]
                      [1]
                      [Interest Rate Percentage <= 10.99]
                        [1]
                        [0]
              [Interest Rate Percentage <= 11.46]
                [1]
                [0]
          [FICO_range_lower <= 800]
            [Loan Length in Months <= 36]
              [FICO_range_lower <= 660]
                [Interest Rate Percentage <= 13.24]
                  [1]
                  [Debt-To-Income Ratio Percentage <= 24.44]
                    [Amount Requested <= 3600]
                      [0]
                      [Interest Rate Percentage <= 15.33]
                        [Amount Requested <= 8000]
                          [Loan Purpose == other]
                            [0]
                            [Interest Rate Percentage <= 14.11]
                              [Interest Rate Percentage <= 13.36]
                                [1]
                                [0]
                              [Loan Title == My Loan]
                                [0]
                                [Loan Title == Excavator 4 Hire]
                                  [0]
                                  [1]
                          [0]
                        [0]
                    [1]
                [Debt-To-Income Ratio Percentage <= 18.48]
                  [Debt-To-Income Ratio Percentage <= 18.39]
                    [Loan Title == personal]
                      [Interest Rate Percentage <= 14.74]
                        [0]
                        [1]
                      [Debt-To-Income Ratio Percentage <= 0.56]
                        [Loan Purpose == wedding]
                          [0]
                          [Interest Rate Percentage <= 12.69]
                            [1]
                            [Amount Requested <= 23600]
                              [FICO_range_lower <= 680]
                                [Interest Rate Percentage <= 14.11]
                                  [1]
                                  [0]
                                [1]
                              [0]
                        [Debt-To-Income Ratio Percentage <= 1.53]
                          [Debt-To-Income Ratio Percentage <= 1.07]
                            [Debt-To-Income Ratio Percentage <= 1.0]
                              [Interest Rate Percentage <= 14.65]
                                [Loan Title == Kitchen Floor and Countertop Replacement]
                                  [1]
                                  [0]
                                [1]
                              [1]
                            [0]
                          [Loan Title == Personal loan]
                            [1]
                            [Interest Rate Percentage <= 10.95]
                              [Loan Purpose == home_improvement]
                                [1]
                                [Amount Requested <= 1600]
                                  [1]
                                  [Loan Purpose == debt_consolidation]
                                    [Debt-To-Income Ratio Percentage <= 11.52]
                                      [0]
                                      [Loan Title == working hard]
                                        [0]
                                        [1]
                                    [0]
                              [Interest Rate Percentage <= 12.18]
                                [Debt-To-Income Ratio Percentage <= 14.4]
                                  [Loan Title == Personal Loan]
                                    [0]
                                    [Debt-To-Income Ratio Percentage <= 14.17]
                                      [Monthly PAYMENT <= 697.2]
                                        [Loan Purpose == wedding]
                                          [0]
                                          [Interest Rate Percentage <= 11.99]
                                            [Loan Title == Debt Consolidation]
                                              [0]
                                              [Loan Title == Credit Card Consolidation]
                                                [0]
                                                [Monthly PAYMENT <= 165.74]
                                                  [Interest Rate Percentage <= 11.26]
                                                    [Amount Requested <= 4800]
                                                      [Loan Title == Debt Consolidation Loan]
                                                        [0]
                                                        [1]
                                                      [0]
                                                    [Debt-To-Income Ratio Percentage <= 10.2]
                                                      [Loan Purpose == car]
                                                        [0]
                                                        [Monthly PAYMENT <= 164.86]
                                                          [Amount Requested <= 2400]
                                                            [Loan Title == Parent Attend Navy Induction]
                                                              [1]
                                                              [0]
                                                            [Loan Title == Make it a Merrier Christmas]
                                                              [0]
                                                              [1]
                                                          [0]
                                                      [0]
                                                  [Amount Requested <= 8500]
                                                    [Loan Title == cash]
                                                      [0]
                                                      [1]
                                                    [Monthly PAYMENT <= 297.13]
                                                      [0]
                                                      [FICO_range_lower <= 700]
                                                        [Monthly PAYMENT <= 491.3]
                                                          [0]
                                                          [Interest Rate Percentage <= 11.97]
                                                            [1]
                                                            [Amount Requested <= 16000]
                                                              [Debt-To-Income Ratio Percentage <= 7.17]
                                                                [0]
                                                                [1]
                                                              [0]
                                                        [Interest Rate Percentage <= 11.12]
                                                          [1]
                                                          [Amount Requested <= 13000]
                                                            [Amount Requested <= 10000]
                                                              [Amount Requested <= 9500]
                                                                [1]
                                                                [Loan Title == Personal Restructuring Loan]
                                                                  [1]
                                                                  [0]
                                                              [1]
                                                            [Debt-To-Income Ratio Percentage <= 3.93]
                                                              [0]
                                                              [Debt-To-Income Ratio Percentage <= 10.72]
                                                                [Amount Requested <= 15000]
                                                                  [0]
                                                                  [Loan Title == I am requesting a Consolidation Loan.]
                                                                    [0]
                                                                    [Loan Title == Consolidation for better interest]
                                                                      [0]
                                                                      [1]
                                                                [1]
                                            [Debt-To-Income Ratio Percentage <= 9.85]
                                              [1]
                                              [FICO_range_lower <= 685]
                                                [0]
                                                [Loan Title == credit card debt]
                                                  [0]
                                                  [1]
                                        [FICO_range_lower <= 730]
                                          [Amount Requested <= 23000]
                                            [1]
                                            [0]
                                          [Loan Title == Debt Consolidation]
                                            [Amount Requested <= 24000]
                                              [0]
                                              [1]
                                            [0]
                                      [0]
                                  [Debt-To-Income Ratio Percentage <= 15.26]
                                    [1]
                                    [FICO_range_lower <= 715]
                                      [Monthly PAYMENT <= 196.41]
                                        [Interest Rate Percentage <= 11.54]
                                          [FICO_range_lower <= 700]
                                            [1]
                                            [Amount Requested <= 3000]
                                              [Amount Requested <= 2500]
                                                [0]
                                                [1]
                                              [0]
                                          [Loan Title == Home Maintnance]
                                            [1]
                                            [0]
                                        [Amount Requested <= 18000]
                                          [Loan Title == Consolidating credit cards]
                                            [0]
                                            [1]
                                          [0]
                                      [Interest Rate Percentage <= 11.26]
                                        [1]
                                        [Loan Title == Consolidate current debt and BSN]
                                          [1]
                                          [0]
                                [Interest Rate Percentage <= 12.42]
                                  [FICO_range_lower <= 695]
                                    [0]
                                    [Amount Requested <= 4800]
                                      [1]
                                      [Amount Requested <= 9800]
                                        [0]
                                        [Debt-To-Income Ratio Percentage <= 15.94]
                                          [Amount Requested <= 15200]
                                            [1]
                                            [0]
                                          [1]
                                  [Loan Purpose == car]
                                    [1]
                                    [Loan Purpose == major_purchase]
                                      [Debt-To-Income Ratio Percentage <= 4.49]
                                        [0]
                                        [Amount Requested <= 5550]
                                          [1]
                                          [Debt-To-Income Ratio Percentage <= 13.67]
                                            [Amount Requested <= 7000]
                                              [0]
                                              [Loan Title == Major Purchase]
                                                [0]
                                                [Loan Title == moving away from home]
                                                  [0]
                                                  [1]
                                            [1]
                                      [Loan Title == Home Improvements]
                                        [0]
                                        [Loan Title == debt loan]
                                          [0]
                                          [Debt-To-Income Ratio Percentage <= 2.7]
                                            [Loan Title == Home Improvement Loan]
                                              [0]
                                              [1]
                                            [Loan Title == Debts]
                                              [1]
                                              [Loan Purpose == vacation]
                                                [0]
                                                [Loan Title == Credit Card Refinance]
                                                  [1]
                                                  [Loan Title == consolidation loan]
                                                    [1]
                                                    [Loan Title == personal loan]
                                                      [1]
                                                      [Interest Rate Percentage <= 14.59]
                                                        [Interest Rate Percentage <= 14.35]
                                                          [Loan Purpose == medical]
                                                            [1]
                                                            [Amount Requested <= 3075]
                                                              [Debt-To-Income Ratio Percentage <= 14.54]
                                                                [Debt-To-Income Ratio Percentage <= 5.04]
                                                                  [0]
                                                                  [Debt-To-Income Ratio Percentage <= 10.33]
                                                                    [1]
                                                                    [Amount Requested <= 2500]
                                                                      [Amount Requested <= 1600]
                                                                        [Interest Rate Percentage <= 13.57]
                                                                          [0]
                                                                          [1]
                                                                        [1]
                                                                      [0]
                                                                [Loan Title == Debt Consolidation]
                                                                  [1]
                                                                  [0]
                                                              [Debt-To-Income Ratio Percentage <= 18.0]
                                                                [Debt-To-Income Ratio Percentage <= 17.86]
                                                                  [Loan Title == Consolidate]
                                                                    [0]
                                                                    [Debt-To-Income Ratio Percentage <= 17.75]
                                                                      [Debt-To-Income Ratio Percentage <= 15.48]
                                                                        [Debt-To-Income Ratio Percentage <= 6.52]
                                                                          [Loan Purpose == home_improvement]
                                                                            [0]
                                                                            [Monthly PAYMENT <= 404.97]
                                                                              [FICO_range_lower <= 710]
                                                                                [FICO_range_lower <= 690]
                                                                                  [FICO_range_lower <= 675]
                                                                                    [1]
                                                                                    [Interest Rate Percentage <= 13.11]
                                                                                      [Amount Requested <= 8000]
                                                                                        [1]
                                                                                        [0]
                                                                                      [0]
                                                                                  [1]
                                                                                [Amount Requested <= 10800]
                                                                                  [0]
                                                                                  [1]
                                                                              [1]
                                                                          [Interest Rate Percentage <= 12.86]
                                                                            [Debt-To-Income Ratio Percentage <= 10.37]
                                                                              [Interest Rate Percentage <= 12.53]
                                                                                [0]
                                                                                [Interest Rate Percentage <= 12.69]
                                                                                  [Loan Title == Excellent Credit History]
                                                                                    [0]
                                                                                    [1]
                                                                                  [Amount Requested <= 17000]
                                                                                    [0]
                                                                                    [1]
                                                                              [Amount Requested <= 10000]
                                                                                [1]
                                                                                [Amount Requested <= 12875]
                                                                                  [Loan Title == Credit Card]
                                                                                    [1]
                                                                                    [0]
                                                                                  [1]
                                                                            [FICO_range_lower <= 710]
                                                                              [Monthly PAYMENT <= 168.62]
                                                                                [Monthly PAYMENT <= 135.21]
                                                                                  [Interest Rate Percentage <= 13.16]
                                                                                    [0]
                                                                                    [1]
                                                                                  [0]
                                                                                [Monthly PAYMENT <= 253.58]
                                                                                  [Amount Requested <= 6000]
                                                                                    [Amount Requested <= 5250]
                                                                                      [Interest Rate Percentage <= 14.26]
                                                                                        [Loan Title == Personal Loan]
                                                                                          [0]
                                                                                          [1]
                                                                                        [0]
                                                                                      [0]
                                                                                    [1]
                                                                                  [Debt-To-Income Ratio Percentage <= 6.78]
                                                                                    [1]
                                                                                    [Loan Purpose == debt_consolidation]
                                                                                      [Amount Requested <= 10000]
                                                                                        [Interest Rate Percentage <= 12.99]
                                                                                          [1]
                                                                                          [0]
                                                                                        [Debt-To-Income Ratio Percentage <= 14.58]
                                                                                          [Monthly PAYMENT <= 732.9]
                                                                                            [Debt-To-Income Ratio Percentage <= 14.14]
                                                                                              [Monthly PAYMENT <= 682.08]
                                                                                                [Debt-To-Income Ratio Percentage <= 10.44]
                                                                                                  [Amount Requested <= 12000]
                                                                                                    [0]
                                                                                                    [1]
                                                                                                  [Amount Requested <= 12000]
                                                                                                    [1]
                                                                                                    [0]
                                                                                                [0]
                                                                                              [1]
                                                                                            [1]
                                                                                          [0]
                                                                                      [Debt-To-Income Ratio Percentage <= 14.21]
                                                                                        [Interest Rate Percentage <= 13.48]
                                                                                          [0]
                                                                                          [Monthly PAYMENT <= 682.74]
                                                                                            [Loan Title == New Roof]
                                                                                              [0]
                                                                                              [1]
                                                                                            [0]
                                                                                        [1]
                                                                              [0]
                                                                        [Interest Rate Percentage <= 13.12]
                                                                          [Loan Purpose == other]
                                                                            [0]
                                                                            [Amount Requested <= 11500]
                                                                              [Loan Title == Privacy Needed]
                                                                                [0]
                                                                                [1]
                                                                              [0]
                                                                          [FICO_range_lower <= 665]
                                                                            [0]
                                                                            [FICO_range_lower <= 685]
                                                                              [1]
                                                                              [Interest Rate Percentage <= 13.67]
                                                                                [1]
                                                                                [Amount Requested <= 5000]
                                                                                  [1]
                                                                                  [0]
                                                                      [0]
                                                                  [1]
                                                                [0]
                                                          [Amount Requested <= 4000]
                                                            [Amount Requested <= 1500]
                                                              [0]
                                                              [1]
                                                            [Loan Title == Credit card Consolidation]
                                                              [1]
                                                              [0]
                                                        [Amount Requested <= 2000]
                                                          [1]
                                                          [Interest Rate Percentage <= 15.37]
                                                            [Interest Rate Percentage <= 15.31]
                                                              [Interest Rate Percentage <= 14.84]
                                                                [Loan Purpose == debt_consolidation]
                                                                  [FICO_range_lower <= 675]
                                                                    [Interest Rate Percentage <= 14.74]
                                                                      [Debt-To-Income Ratio Percentage <= 15.89]
                                                                        [Debt-To-Income Ratio Percentage <= 11.1]
                                                                          [Amount Requested <= 2100]
                                                                            [0]
                                                                            [1]
                                                                          [0]
                                                                        [1]
                                                                      [1]
                                                                    [1]
                                                                  [Loan Purpose == other]
                                                                    [1]
                                                                    [Loan Title == Deck]
                                                                      [1]
                                                                      [Loan Title == Refinance credit card down from 29.99]
                                                                        [1]
                                                                        [0]
                                                                [Interest Rate Percentage <= 15.28]
                                                                  [Interest Rate Percentage <= 15.23]
                                                                    [FICO_range_lower <= 690]
                                                                      [Interest Rate Percentage <= 14.96]
                                                                        [0]
                                                                        [Amount Requested <= 5000]
                                                                          [1]
                                                                          [Amount Requested <= 11600]
                                                                            [0]
                                                                            [1]
                                                                      [Amount Requested <= 24250]
                                                                        [1]
                                                                        [0]
                                                                    [0]
                                                                  [FICO_range_lower <= 670]
                                                                    [0]
                                                                    [1]
                                                              [1]
                                                            [Loan Purpose == credit_card]
                                                              [1]
                                                              [Interest Rate Percentage <= 15.7]
                                                                [Loan Title == Wedding]
                                                                  [1]
                                                                  [Loan Title == PAY OFF]
                                                                    [1]
                                                                    [Loan Title == New Kitchen]
                                                                      [1]
                                                                      [0]
                                                                [1]
                    [1]
                  [Debt-To-Income Ratio Percentage <= 18.86]
                    [Loan Title == Personal]
                      [1]
                      [0]
                    [Interest Rate Percentage <= 15.37]
                      [Monthly PAYMENT <= 529.22]
                        [Interest Rate Percentage <= 13.61]
                          [Monthly PAYMENT <= 41.22]
                            [1]
                            [Debt-To-Income Ratio Percentage <= 27.46]
                              [FICO_range_lower <= 675]
                                [Interest Rate Percentage <= 13.43]
                                  [Loan Title == Debt Consolidation Loan]
                                    [1]
                                    [0]
                                  [1]
                                [Loan Title == Personal Loan]
                                  [0]
                                  [Interest Rate Percentage <= 13.22]
                                    [Debt-To-Income Ratio Percentage <= 22.43]
                                      [Debt-To-Income Ratio Percentage <= 21.89]
                                        [Debt-To-Income Ratio Percentage <= 21.53]
                                          [Debt-To-Income Ratio Percentage <= 20.37]
                                            [Debt-To-Income Ratio Percentage <= 20.12]
                                              [Interest Rate Percentage <= 12.12]
                                                [Interest Rate Percentage <= 11.58]
                                                  [Amount Requested <= 2150]
                                                    [0]
                                                    [1]
                                                  [Amount Requested <= 2500]
                                                    [1]
                                                    [Loan Title == Debt Consolidation]
                                                      [1]
                                                      [0]
                                                [Amount Requested <= 10000]
                                                  [1]
                                                  [Debt-To-Income Ratio Percentage <= 18.89]
                                                    [1]
                                                    [0]
                                              [0]
                                            [Monthly PAYMENT <= 326.21]
                                              [Amount Requested <= 4000]
                                                [0]
                                                [1]
                                              [Debt-To-Income Ratio Percentage <= 21.0]
                                                [1]
                                                [0]
                                          [0]
                                        [Loan Title == Home Improvement]
                                          [0]
                                          [1]
                                      [Amount Requested <= 9500]
                                        [Amount Requested <= 8325]
                                          [Monthly PAYMENT <= 265.18]
                                            [Debt-To-Income Ratio Percentage <= 22.83]
                                              [0]
                                              [Loan Purpose == debt_consolidation]
                                                [1]
                                                [Interest Rate Percentage <= 11.86]
                                                  [Loan Title == Personal]
                                                    [0]
                                                    [1]
                                                  [0]
                                            [0]
                                          [1]
                                        [Loan Title == Pay Off High Interest Debt]
                                          [1]
                                          [0]
                                    [1]
                              [1]
                          [Debt-To-Income Ratio Percentage <= 19.67]
                            [1]
                            [Amount Requested <= 12500]
                              [Amount Requested <= 11450]
                                [Debt-To-Income Ratio Percentage <= 19.85]
                                  [1]
                                  [FICO_range_lower <= 675]
                                    [Amount Requested <= 3750]
                                      [1]
                                      [Debt-To-Income Ratio Percentage <= 23.45]
                                        [0]
                                        [Interest Rate Percentage <= 14.59]
                                          [0]
                                          [Interest Rate Percentage <= 15.21]
                                            [1]
                                            [0]
                                    [0]
                                [1]
                              [0]
                        [Interest Rate Percentage <= 10.99]
                          [0]
                          [Interest Rate Percentage <= 14.91]
                            [Debt-To-Income Ratio Percentage <= 19.44]
                              [Amount Requested <= 23000]
                                [Interest Rate Percentage <= 12.53]
                                  [1]
                                  [0]
                                [1]
                              [Loan Title == Consolidation]
                                [0]
                                [Loan Title == No More Credit Cards!!!]
                                  [0]
                                  [Loan Title == Brian's Debt Consolidation]
                                    [0]
                                    [Loan Title == Wedding Exp.]
                                      [0]
                                      [1]
                            [0]
                      [1]
              [FICO_range_lower <= 760]
                [Loan Purpose == home_improvement]
                  [0]
                  [Debt-To-Income Ratio Percentage <= 20.62]
                    [Interest Rate Percentage <= 15.23]
                      [Monthly PAYMENT <= 416.97]
                        [Debt-To-Income Ratio Percentage <= 18.53]
                          [Loan Purpose == medical]
                            [1]
                            [Debt-To-Income Ratio Percentage <= 18.43]
                              [Interest Rate Percentage <= 13.43]
                                [Interest Rate Percentage <= 13.06]
                                  [Debt-To-Income Ratio Percentage <= 8.2]
                                    [0]
                                    [Debt-To-Income Ratio Percentage <= 10.5]
                                      [FICO_range_lower <= 720]
                                        [1]
                                        [Interest Rate Percentage <= 12.61]
                                          [0]
                                          [1]
                                      [Loan Title == Debt Consolidation]
                                        [Amount Requested <= 8000]
                                          [0]
                                          [1]
                                        [0]
                                  [FICO_range_lower <= 695]
                                    [0]
                                    [1]
                                [FICO_range_lower <= 695]
                                  [Amount Requested <= 3600]
                                    [1]
                                    [Loan Title == deb consolidation]
                                      [1]
                                      [Loan Title == Anna's Loan]
                                        [1]
                                        [0]
                                  [0]
                              [1]
                          [0]
                        [FICO_range_lower <= 720]
                          [Loan Title == Debt Consolidation Loan]
                            [1]
                            [0]
                          [Interest Rate Percentage <= 13.99]
                            [Loan Purpose == credit_card]
                              [1]
                              [Monthly PAYMENT <= 439.76]
                                [1]
                                [Debt-To-Income Ratio Percentage <= 14.37]
                                  [0]
                                  [Amount Requested <= 20375]
                                    [Loan Title == Credit Card Consolidation]
                                      [1]
                                      [0]
                                    [1]
                            [1]
                      [Amount Requested <= 18000]
                        [Loan Purpose == credit_card]
                          [0]
                          [Loan Title == Other]
                            [0]
                            [1]
                        [0]
                    [Loan Title == Debt Consolidation]
                      [1]
                      [Debt-To-Income Ratio Percentage <= 22.69]
                        [Amount Requested <= 5500]
                          [0]
                          [Loan Title == Angela Debt Consolidation]
                            [0]
                            [1]
                        [Debt-To-Income Ratio Percentage <= 23.61]
                          [Loan Title ==  consolidation ]
                            [1]
                            [0]
                          [Interest Rate Percentage <= 13.61]
                            [Interest Rate Percentage <= 12.69]
                              [Debt-To-Income Ratio Percentage <= 25.79]
                                [1]
                                [Loan Title == Credit Card Consolidation]
                                  [1]
                                  [0]
                              [0]
                            [1]
                [Interest Rate Percentage <= 12.98]
                  [Amount Requested <= 18000]
                    [Interest Rate Percentage <= 11.12]
                      [0]
                      [Interest Rate Percentage <= 11.49]
                        [1]
                        [0]
                    [Debt-To-Income Ratio Percentage <= 11.99]
                      [1]
                      [Amount Requested <= 20000]
                        [1]
                        [0]
                  [Loan Title == Lending Tree Personal Loan - New Street]
                    [1]
                    [0]
            [1]
        [Loan Purpose == credit_card]
          [Debt-To-Income Ratio Percentage <= 24.64]
            [Interest Rate Percentage <= 18.99]
              [Interest Rate Percentage <= 17.19]
                [Interest Rate Percentage <= 16.32]
                  [Monthly PAYMENT <= 389.26]
                    [Loan Title == Credit Card Loan]
                      [0]
                      [1]
                    [Interest Rate Percentage <= 16.02]
                      [0]
                      [Amount Requested <= 11725]
                        [0]
                        [1]
                  [Loan Title == I can be 18  to debt free please]
                    [1]
                    [0]
                [Loan Title == credit card refi]
                  [0]
                  [Amount Requested <= 13000]
                    [Amount Requested <= 8000]
                      [1]
                      [0]
                    [1]
              [Interest Rate Percentage <= 20.99]
                [0]
                [Amount Requested <= 20000]
                  [0]
                  [1]
            [0]
          [Loan Title == Medical]
            [1]
            [Amount Requested <= 17475]
              [Interest Rate Percentage <= 20.5]
                [Debt-To-Income Ratio Percentage <= 21.93]
                  [Amount Requested <= 16300]
                    [Monthly PAYMENT <= 405.26]
                      [Loan Purpose == home_improvement]
                        [0]
                        [FICO_range_lower <= 725]
                          [Interest Rate Percentage <= 18.55]
                            [FICO_range_lower <= 700]
                              [Debt-To-Income Ratio Percentage <= 17.13]
                                [Debt-To-Income Ratio Percentage <= 15.0]
                                  [Monthly PAYMENT <= 351.53]
                                    [Monthly PAYMENT <= 73.68]
                                      [0]
                                      [Monthly PAYMENT <= 97.96]
                                        [1]
                                        [Monthly PAYMENT <= 348.93]
                                          [Amount Requested <= 8000]
                                            [Loan Purpose == debt_consolidation]
                                              [Debt-To-Income Ratio Percentage <= 12.87]
                                                [Debt-To-Income Ratio Percentage <= 6.85]
                                                  [Interest Rate Percentage <= 17.99]
                                                    [Amount Requested <= 4200]
                                                      [Debt-To-Income Ratio Percentage <= 2.37]
                                                        [1]
                                                        [0]
                                                      [0]
                                                    [1]
                                                  [Interest Rate Percentage <= 16.82]
                                                    [1]
                                                    [Interest Rate Percentage <= 18.21]
                                                      [0]
                                                      [1]
                                                [0]
                                              [Amount Requested <= 7000]
                                                [Loan Title == Consolidation]
                                                  [1]
                                                  [0]
                                                [1]
                                            [Loan Title == Car Loan]
                                              [1]
                                              [0]
                                          [1]
                                    [0]
                                  [Monthly PAYMENT <= 302.44]
                                    [Amount Requested <= 3200]
                                      [0]
                                      [1]
                                    [Loan Title == Pay off Chase Credit Card]
                                      [1]
                                      [0]
                                [Debt-To-Income Ratio Percentage <= 20.51]
                                  [Interest Rate Percentage <= 15.81]
                                    [1]
                                    [Loan Title == Debt Consolidation]
                                      [1]
                                      [0]
                                  [Monthly PAYMENT <= 201.45]
                                    [0]
                                    [Interest Rate Percentage <= 16.07]
                                      [Amount Requested <= 7500]
                                        [1]
                                        [0]
                                      [1]
                              [Loan Title == Unsecured loan]
                                [1]
                                [0]
                            [Loan Title == Debt Consolidation]
                              [Amount Requested <= 8000]
                                [1]
                                [0]
                              [0]
                          [1]
                      [Debt-To-Income Ratio Percentage <= 19.13]
                        [Monthly PAYMENT <= 526.99]
                          [Debt-To-Income Ratio Percentage <= 12.31]
                            [Loan Title == Investment Loan]
                              [0]
                              [1]
                            [Interest Rate Percentage <= 16.89]
                              [1]
                              [0]
                          [Loan Title == mmlloan]
                            [1]
                            [0]
                        [1]
                    [0]
                  [Loan Title == My loan]
                    [1]
                    [Loan Title == Debt Consolidation]
                      [Monthly PAYMENT <= 361.85]
                        [0]
                        [1]
                      [0]
                [0]
              [Monthly PAYMENT <= 790.49]
                [Debt-To-Income Ratio Percentage <= 8.38]
                  [Interest Rate Percentage <= 20.5]
                    [FICO_range_lower <= 725]
                      [Amount Requested <= 18000]
                        [0]
                        [Loan Title == faith]
                          [0]
                          [1]
                      [Amount Requested <= 20000]
                        [1]
                        [0]
                    [0]
                  [Monthly PAYMENT <= 437.92]
                    [Loan Length in Months <= 36]
                      [0]
                      [1]
                    [Monthly PAYMENT <= 671.47]
                      [FICO_range_lower <= 685]
                        [Amount Requested <= 20000]
                          [Interest Rate Percentage <= 18.91]
                            [0]
                            [FICO_range_lower <= 680]
                              [Loan Title == My 2011 Debt Consolidation]
                                [0]
                                [Debt-To-Income Ratio Percentage <= 8.67]
                                  [0]
                                  [1]
                              [0]
                          [0]
                        [Interest Rate Percentage <= 16.49]
                          [0]
                          [Monthly PAYMENT <= 493.73]
                            [1]
                            [Total Amount Funded <= 22250]
                              [FICO_range_lower <= 695]
                                [Amount Requested <= 18500]
                                  [0]
                                  [1]
                                [0]
                              [Loan Title == Debt Consolidation]
                                [0]
                                [1]
                      [Debt-To-Income Ratio Percentage <= 10.85]
                        [0]
                        [Loan Purpose == small_business]
                          [Loan Title == Launching apparel brand w/Patent]
                            [1]
                            [0]
                          [FICO_range_lower <= 675]
                            [Monthly PAYMENT <= 675.23]
                              [1]
                              [Amount Requested <= 19750]
                                [0]
                                [Amount Requested <= 30000]
                                  [Loan Title == Debt Consolidation Loan]
                                    [0]
                                    [Loan Title == Remodelling and Consolidation Loan]
                                      [0]
                                      [1]
                                  [0]
                            [1]
                [Monthly PAYMENT <= 931.09]
                  [Debt-To-Income Ratio Percentage <= 16.94]
                    [0]
                    [Loan Title == 2012loan]
                      [1]
                      [Loan Title == dimples]
                        [1]
                        [Loan Title == Debt Consolidation]
                          [Amount Requested <= 30000]
                            [0]
                            [1]
                          [0]
                  [FICO_range_lower <= 695]
                    [Interest Rate Percentage <= 22.45]
                      [Interest Rate Percentage <= 19.72]
                        [Amount Requested <= 30000]
                          [1]
                          [0]
                        [0]
                      [1]
                    [Amount Requested <= 32000]
                      [0]
                      [1]



```python
print("Pruned Gini tree:")
print_tree(pruned_tree_by_gini.root)
```

    Pruned Gini tree:
    [Interest Rate Percentage <= 10.74]
      [1]
      [0]



```python
print("Original Information Gain tree:")
print_tree(information_gain_decision_tree.root)
```

    Original Information Gain tree:
    [Interest Rate Percentage <= 10.74]
      [Debt-To-Income Ratio Percentage <= 10.97]
        [FICO_range_lower <= 760]
          [Debt-To-Income Ratio Percentage <= 10.54]
            [Loan Title == Debt consolidation]
              [0]
              [Amount Requested <= 20000]
                [Loan Title == personal loan]
                  [0]
                  [Monthly PAYMENT <= 324.07]
                    [Monthly PAYMENT <= 292.01]
                      [Interest Rate Percentage <= 10.62]
                        [FICO_range_lower <= 685]
                          [1]
                          [Monthly PAYMENT <= 286.4]
                            [FICO_range_lower <= 730]
                              [Monthly PAYMENT <= 195.27]
                                [Loan Purpose == other]
                                  [FICO_range_lower <= 700]
                                    [0]
                                    [FICO_range_lower <= 720]
                                      [1]
                                      [Amount Requested <= 4800]
                                        [0]
                                        [1]
                                  [Debt-To-Income Ratio Percentage <= 6.0]
                                    [Monthly PAYMENT <= 187.69]
                                      [Debt-To-Income Ratio Percentage <= 3.0]
                                        [1]
                                        [Loan Title == LoantoLee]
                                          [1]
                                          [0]
                                      [1]
                                    [1]
                                [Monthly PAYMENT <= 248.37]
                                  [FICO_range_lower <= 690]
                                    [1]
                                    [Loan Title == Debt Consolidation]
                                      [1]
                                      [Loan Title == Ring]
                                        [1]
                                        [0]
                                  [1]
                              [Debt-To-Income Ratio Percentage <= 10.48]
                                [Interest Rate Percentage <= 9.32]
                                  [Monthly PAYMENT <= 139.55]
                                    [Interest Rate Percentage <= 7.29]
                                      [FICO_range_lower <= 740]
                                        [Loan Title == needing to pay off credit cards]
                                          [1]
                                          [0]
                                        [Loan Title == Medical]
                                          [0]
                                          [1]
                                      [1]
                                    [Interest Rate Percentage <= 7.74]
                                      [Debt-To-Income Ratio Percentage <= 5.77]
                                        [FICO_range_lower <= 755]
                                          [Interest Rate Percentage <= 6.62]
                                            [1]
                                            [Amount Requested <= 8000]
                                              [Loan Title == Debt Consolidation]
                                                [0]
                                                [1]
                                              [0]
                                          [0]
                                        [1]
                                      [FICO_range_lower <= 755]
                                        [Loan Title == Home Equity Payoff for Refinance]
                                          [1]
                                          [Loan Title == Loan to buy a car]
                                            [1]
                                            [0]
                                        [1]
                                  [1]
                                [0]
                            [0]
                        [1]
                      [Loan Title == Consolidate Debt to Start Business]
                        [0]
                        [1]
                    [Amount Requested <= 11000]
                      [0]
                      [Debt-To-Income Ratio Percentage <= 9.13]
                        [Debt-To-Income Ratio Percentage <= 6.21]
                          [1]
                          [Interest Rate Percentage <= 9.88]
                            [Debt-To-Income Ratio Percentage <= 8.35]
                              [FICO_range_lower <= 735]
                                [0]
                                [Loan Title == Debt Consolidation]
                                  [0]
                                  [1]
                              [1]
                            [0]
                        [1]
                [1]
            [1]
          [Loan Purpose == small_business]
            [Debt-To-Income Ratio Percentage <= 2.14]
              [1]
              [Amount Requested <= 25000]
                [0]
                [1]
            [Loan Title == Scooter loan]
              [0]
              [Interest Rate Percentage <= 7.29]
                [Loan Title == paint loan]
                  [0]
                  [1]
                [FICO_range_lower <= 765]
                  [1]
                  [Loan Purpose == home_improvement]
                    [1]
                    [Amount Requested <= 2650]
                      [0]
                      [Total Amount Funded <= 9600]
                        [Monthly PAYMENT <= 140.31]
                          [Monthly PAYMENT <= 101.1]
                            [1]
                            [0]
                          [1]
                        [Loan Purpose == other]
                          [0]
                          [Interest Rate Percentage <= 7.88]
                            [Amount Requested <= 12000]
                              [0]
                              [1]
                            [Debt-To-Income Ratio Percentage <= 2.34]
                              [Interest Rate Percentage <= 8.07]
                                [1]
                                [0]
                              [1]
        [Loan Purpose == major_purchase]
          [Debt-To-Income Ratio Percentage <= 11.65]
            [0]
            [1]
          [Monthly PAYMENT <= 80.88]
            [Monthly PAYMENT <= 58.26]
              [Interest Rate Percentage <= 9.76]
                [Interest Rate Percentage <= 6.62]
                  [1]
                  [Loan Title == Premier Refinance]
                    [1]
                    [Loan Title == Personal Loan]
                      [1]
                      [0]
                [1]
              [Amount Requested <= 2400]
                [Amount Requested <= 2050]
                  [0]
                  [Interest Rate Percentage <= 9.63]
                    [Debt-To-Income Ratio Percentage <= 18.68]
                      [1]
                      [Amount Requested <= 2200]
                        [1]
                        [0]
                    [0]
                [0]
            [Debt-To-Income Ratio Percentage <= 12.34]
              [Debt-To-Income Ratio Percentage <= 12.24]
                [FICO_range_lower <= 770]
                  [FICO_range_lower <= 725]
                    [Interest Rate Percentage <= 10.39]
                      [Loan Title == GAC Credit Card]
                        [0]
                        [1]
                      [Loan Title == Credit Consolidation]
                        [1]
                        [0]
                    [Interest Rate Percentage <= 8.49]
                      [Debt-To-Income Ratio Percentage <= 11.13]
                        [0]
                        [Amount Requested <= 9000]
                          [Loan Title == Concolidation]
                            [1]
                            [0]
                          [1]
                      [0]
                  [1]
                [0]
              [Debt-To-Income Ratio Percentage <= 12.74]
                [1]
                [Loan Title == Debt Consolidation Loan]
                  [Interest Rate Percentage <= 9.99]
                    [0]
                    [Amount Requested <= 9200]
                      [1]
                      [0]
                  [Loan Purpose == house]
                    [1]
                    [Monthly PAYMENT <= 93.31]
                      [1]
                      [Loan Purpose == credit_card]
                        [Debt-To-Income Ratio Percentage <= 17.71]
                          [Interest Rate Percentage <= 5.79]
                            [0]
                            [1]
                          [Debt-To-Income Ratio Percentage <= 25.29]
                            [Amount Requested <= 6000]
                              [0]
                              [Amount Requested <= 7200]
                                [1]
                                [FICO_range_lower <= 740]
                                  [Amount Requested <= 21500]
                                    [0]
                                    [1]
                                  [Interest Rate Percentage <= 6.92]
                                    [1]
                                    [0]
                            [1]
                        [Amount Requested <= 23000]
                          [Amount Requested <= 17000]
                            [Debt-To-Income Ratio Percentage <= 14.5]
                              [FICO_range_lower <= 705]
                                [1]
                                [FICO_range_lower <= 715]
                                  [Interest Rate Percentage <= 9.91]
                                    [0]
                                    [1]
                                  [Total Amount Funded <= 6600]
                                    [1]
                                    [Debt-To-Income Ratio Percentage <= 13.99]
                                      [Interest Rate Percentage <= 9.88]
                                        [Loan Purpose == debt_consolidation]
                                          [1]
                                          [Debt-To-Income Ratio Percentage <= 13.34]
                                            [0]
                                            [Amount Requested <= 7000]
                                              [0]
                                              [1]
                                        [0]
                                      [1]
                              [Amount Requested <= 15600]
                                [Interest Rate Percentage <= 10.71]
                                  [Interest Rate Percentage <= 9.88]
                                    [Interest Rate Percentage <= 5.99]
                                      [0]
                                      [Debt-To-Income Ratio Percentage <= 28.39]
                                        [Interest Rate Percentage <= 6.03]
                                          [1]
                                          [FICO_range_lower <= 705]
                                            [Interest Rate Percentage <= 7.66]
                                              [1]
                                              [0]
                                            [Interest Rate Percentage <= 6.62]
                                              [Interest Rate Percentage <= 6.39]
                                                [Loan Title == debt_consolidation]
                                                  [0]
                                                  [1]
                                                [0]
                                              [Interest Rate Percentage <= 6.99]
                                                [1]
                                                [Monthly PAYMENT <= 371.3]
                                                  [Amount Requested <= 6950]
                                                    [Monthly PAYMENT <= 187.08]
                                                      [Debt-To-Income Ratio Percentage <= 16.73]
                                                        [Interest Rate Percentage <= 7.88]
                                                          [0]
                                                          [1]
                                                        [Monthly PAYMENT <= 134.55]
                                                          [Amount Requested <= 4000]
                                                            [Debt-To-Income Ratio Percentage <= 20.33]
                                                              [Interest Rate Percentage <= 7.51]
                                                                [1]
                                                                [0]
                                                              [1]
                                                            [0]
                                                          [1]
                                                      [1]
                                                    [Amount Requested <= 11000]
                                                      [Monthly PAYMENT <= 168.49]
                                                        [0]
                                                        [Loan Purpose == debt_consolidation]
                                                          [Amount Requested <= 10000]
                                                            [Monthly PAYMENT <= 311.8]
                                                              [Monthly PAYMENT <= 247.53]
                                                                [Interest Rate Percentage <= 7.51]
                                                                  [0]
                                                                  [Loan Title == Consolidate debt]
                                                                    [0]
                                                                    [1]
                                                                [1]
                                                              [0]
                                                            [1]
                                                          [Monthly PAYMENT <= 251.88]
                                                            [0]
                                                            [Amount Requested <= 8500]
                                                              [1]
                                                              [Loan Title == High Tech Business Startup]
                                                                [1]
                                                                [Loan Title == other]
                                                                  [1]
                                                                  [0]
                                                      [0]
                                                  [Loan Title == Small Business Loan]
                                                    [0]
                                                    [1]
                                        [0]
                                    [Interest Rate Percentage <= 9.91]
                                      [0]
                                      [Loan Title == consolidation]
                                        [1]
                                        [Loan Title == Debt Consolidation]
                                          [1]
                                          [Debt-To-Income Ratio Percentage <= 19.13]
                                            [Interest Rate Percentage <= 10.38]
                                              [FICO_range_lower <= 695]
                                                [0]
                                                [Debt-To-Income Ratio Percentage <= 18.28]
                                                  [1]
                                                  [0]
                                              [0]
                                            [Interest Rate Percentage <= 9.99]
                                              [0]
                                              [Amount Requested <= 8000]
                                                [1]
                                                [Total Amount Funded <= 9900]
                                                  [0]
                                                  [Monthly PAYMENT <= 390.54]
                                                    [1]
                                                    [Loan Title == Debt loan]
                                                      [1]
                                                      [0]
                                  [Loan Title == Debt Consolidation]
                                    [0]
                                    [Loan Title == Home Improvement]
                                      [Amount Requested <= 8000]
                                        [0]
                                        [1]
                                      [1]
                                [1]
                            [1]
                          [Loan Title == Debt consolidation]
                            [1]
                            [0]
      [Interest Rate Percentage <= 15.8]
        [Loan Purpose == small_business]
          [Monthly PAYMENT <= 102.42]
            [1]
            [Debt-To-Income Ratio Percentage <= 17.88]
              [Monthly PAYMENT <= 171.92]
                [0]
                [Debt-To-Income Ratio Percentage <= 15.87]
                  [Debt-To-Income Ratio Percentage <= 11.07]
                    [Monthly PAYMENT <= 194.15]
                      [1]
                      [Debt-To-Income Ratio Percentage <= 6.14]
                        [Loan Length in Months <= 36]
                          [Debt-To-Income Ratio Percentage <= 3.6]
                            [Debt-To-Income Ratio Percentage <= 2.87]
                              [1]
                              [0]
                            [Loan Title == Need cash flow for 3 month. ]
                              [0]
                              [1]
                          [0]
                        [Debt-To-Income Ratio Percentage <= 9.77]
                          [0]
                          [Loan Title == Working Capital for Brewery]
                            [0]
                            [1]
                    [0]
                  [Amount Requested <= 10000]
                    [0]
                    [Amount Requested <= 18000]
                      [1]
                      [Interest Rate Percentage <= 10.99]
                        [1]
                        [0]
              [Interest Rate Percentage <= 11.46]
                [1]
                [0]
          [FICO_range_lower <= 800]
            [Loan Length in Months <= 36]
              [FICO_range_lower <= 660]
                [Interest Rate Percentage <= 13.24]
                  [1]
                  [Debt-To-Income Ratio Percentage <= 24.44]
                    [Amount Requested <= 3600]
                      [0]
                      [Interest Rate Percentage <= 15.33]
                        [Amount Requested <= 8000]
                          [Loan Purpose == other]
                            [0]
                            [Interest Rate Percentage <= 14.11]
                              [Interest Rate Percentage <= 13.36]
                                [1]
                                [0]
                              [Loan Title == My Loan]
                                [0]
                                [Loan Title == Excavator 4 Hire]
                                  [0]
                                  [1]
                          [0]
                        [0]
                    [1]
                [Debt-To-Income Ratio Percentage <= 18.48]
                  [Debt-To-Income Ratio Percentage <= 18.39]
                    [Loan Title == personal]
                      [Interest Rate Percentage <= 14.74]
                        [0]
                        [1]
                      [Debt-To-Income Ratio Percentage <= 0.56]
                        [Loan Purpose == wedding]
                          [0]
                          [Interest Rate Percentage <= 12.69]
                            [1]
                            [Amount Requested <= 23600]
                              [FICO_range_lower <= 680]
                                [Interest Rate Percentage <= 14.11]
                                  [1]
                                  [0]
                                [1]
                              [0]
                        [Debt-To-Income Ratio Percentage <= 1.53]
                          [Debt-To-Income Ratio Percentage <= 1.07]
                            [Debt-To-Income Ratio Percentage <= 1.0]
                              [Interest Rate Percentage <= 14.65]
                                [Loan Title == Kitchen Floor and Countertop Replacement]
                                  [1]
                                  [0]
                                [1]
                              [1]
                            [0]
                          [Loan Title == Personal loan]
                            [1]
                            [Interest Rate Percentage <= 10.95]
                              [Loan Purpose == home_improvement]
                                [1]
                                [Amount Requested <= 1600]
                                  [1]
                                  [Loan Purpose == debt_consolidation]
                                    [Debt-To-Income Ratio Percentage <= 11.52]
                                      [0]
                                      [Loan Title == working hard]
                                        [0]
                                        [1]
                                    [0]
                              [Interest Rate Percentage <= 12.18]
                                [Debt-To-Income Ratio Percentage <= 14.4]
                                  [Loan Title == Personal Loan]
                                    [0]
                                    [Debt-To-Income Ratio Percentage <= 14.17]
                                      [Monthly PAYMENT <= 697.2]
                                        [Loan Purpose == wedding]
                                          [0]
                                          [Interest Rate Percentage <= 11.99]
                                            [Loan Title == Debt Consolidation]
                                              [0]
                                              [Loan Title == Credit Card Consolidation]
                                                [0]
                                                [Monthly PAYMENT <= 165.74]
                                                  [Interest Rate Percentage <= 11.26]
                                                    [Amount Requested <= 4800]
                                                      [Loan Title == Debt Consolidation Loan]
                                                        [0]
                                                        [1]
                                                      [0]
                                                    [Debt-To-Income Ratio Percentage <= 10.2]
                                                      [Loan Purpose == car]
                                                        [0]
                                                        [Monthly PAYMENT <= 164.86]
                                                          [Amount Requested <= 2400]
                                                            [Loan Title == Parent Attend Navy Induction]
                                                              [1]
                                                              [0]
                                                            [Loan Title == Make it a Merrier Christmas]
                                                              [0]
                                                              [1]
                                                          [0]
                                                      [0]
                                                  [Amount Requested <= 8500]
                                                    [Loan Title == cash]
                                                      [0]
                                                      [1]
                                                    [Monthly PAYMENT <= 297.13]
                                                      [0]
                                                      [FICO_range_lower <= 700]
                                                        [Monthly PAYMENT <= 491.3]
                                                          [0]
                                                          [Interest Rate Percentage <= 11.97]
                                                            [1]
                                                            [Amount Requested <= 16000]
                                                              [Debt-To-Income Ratio Percentage <= 7.17]
                                                                [0]
                                                                [1]
                                                              [0]
                                                        [Interest Rate Percentage <= 11.12]
                                                          [1]
                                                          [Amount Requested <= 13000]
                                                            [Amount Requested <= 10000]
                                                              [Amount Requested <= 9500]
                                                                [1]
                                                                [Loan Title == Personal Restructuring Loan]
                                                                  [1]
                                                                  [0]
                                                              [1]
                                                            [Debt-To-Income Ratio Percentage <= 3.93]
                                                              [0]
                                                              [Debt-To-Income Ratio Percentage <= 10.72]
                                                                [Amount Requested <= 15000]
                                                                  [0]
                                                                  [Loan Title == I am requesting a Consolidation Loan.]
                                                                    [0]
                                                                    [Loan Title == Consolidation for better interest]
                                                                      [0]
                                                                      [1]
                                                                [1]
                                            [Debt-To-Income Ratio Percentage <= 9.85]
                                              [1]
                                              [FICO_range_lower <= 685]
                                                [0]
                                                [Loan Title == credit card debt]
                                                  [0]
                                                  [1]
                                        [FICO_range_lower <= 730]
                                          [Amount Requested <= 23000]
                                            [1]
                                            [0]
                                          [Loan Title == Debt Consolidation]
                                            [Amount Requested <= 24000]
                                              [0]
                                              [1]
                                            [0]
                                      [0]
                                  [Debt-To-Income Ratio Percentage <= 15.26]
                                    [1]
                                    [FICO_range_lower <= 715]
                                      [Monthly PAYMENT <= 196.41]
                                        [Interest Rate Percentage <= 11.54]
                                          [FICO_range_lower <= 700]
                                            [1]
                                            [Amount Requested <= 3000]
                                              [Amount Requested <= 2500]
                                                [0]
                                                [1]
                                              [0]
                                          [Loan Title == Home Maintnance]
                                            [1]
                                            [0]
                                        [Amount Requested <= 18000]
                                          [Loan Title == Consolidating credit cards]
                                            [0]
                                            [1]
                                          [0]
                                      [Interest Rate Percentage <= 11.26]
                                        [1]
                                        [Loan Title == Consolidate current debt and BSN]
                                          [1]
                                          [0]
                                [Interest Rate Percentage <= 12.42]
                                  [FICO_range_lower <= 695]
                                    [0]
                                    [Amount Requested <= 4800]
                                      [1]
                                      [Amount Requested <= 9800]
                                        [0]
                                        [Debt-To-Income Ratio Percentage <= 15.94]
                                          [Amount Requested <= 15200]
                                            [1]
                                            [0]
                                          [1]
                                  [Loan Purpose == car]
                                    [1]
                                    [Loan Purpose == major_purchase]
                                      [Debt-To-Income Ratio Percentage <= 4.49]
                                        [0]
                                        [Amount Requested <= 5550]
                                          [1]
                                          [Debt-To-Income Ratio Percentage <= 13.67]
                                            [Amount Requested <= 7000]
                                              [0]
                                              [Loan Title == Major Purchase]
                                                [0]
                                                [Loan Title == moving away from home]
                                                  [0]
                                                  [1]
                                            [1]
                                      [Loan Title == Home Improvements]
                                        [0]
                                        [Loan Title == debt loan]
                                          [0]
                                          [Debt-To-Income Ratio Percentage <= 2.7]
                                            [Loan Title == Home Improvement Loan]
                                              [0]
                                              [1]
                                            [Loan Title == Debts]
                                              [1]
                                              [Loan Purpose == vacation]
                                                [0]
                                                [Loan Title == Credit Card Refinance]
                                                  [1]
                                                  [Loan Title == consolidation loan]
                                                    [1]
                                                    [Loan Title == personal loan]
                                                      [1]
                                                      [Interest Rate Percentage <= 14.59]
                                                        [Interest Rate Percentage <= 14.35]
                                                          [Loan Purpose == medical]
                                                            [1]
                                                            [Amount Requested <= 3075]
                                                              [Debt-To-Income Ratio Percentage <= 14.54]
                                                                [Debt-To-Income Ratio Percentage <= 5.04]
                                                                  [0]
                                                                  [Debt-To-Income Ratio Percentage <= 10.33]
                                                                    [1]
                                                                    [Amount Requested <= 2500]
                                                                      [Amount Requested <= 1600]
                                                                        [Interest Rate Percentage <= 13.57]
                                                                          [0]
                                                                          [1]
                                                                        [1]
                                                                      [0]
                                                                [Loan Title == Debt Consolidation]
                                                                  [1]
                                                                  [0]
                                                              [Debt-To-Income Ratio Percentage <= 18.0]
                                                                [Debt-To-Income Ratio Percentage <= 17.86]
                                                                  [Loan Title == Consolidate]
                                                                    [0]
                                                                    [Debt-To-Income Ratio Percentage <= 17.75]
                                                                      [Debt-To-Income Ratio Percentage <= 15.48]
                                                                        [Debt-To-Income Ratio Percentage <= 6.52]
                                                                          [Loan Purpose == home_improvement]
                                                                            [0]
                                                                            [Monthly PAYMENT <= 404.97]
                                                                              [FICO_range_lower <= 710]
                                                                                [FICO_range_lower <= 690]
                                                                                  [FICO_range_lower <= 675]
                                                                                    [1]
                                                                                    [Interest Rate Percentage <= 13.11]
                                                                                      [Amount Requested <= 8000]
                                                                                        [1]
                                                                                        [0]
                                                                                      [0]
                                                                                  [1]
                                                                                [Amount Requested <= 10800]
                                                                                  [0]
                                                                                  [1]
                                                                              [1]
                                                                          [Interest Rate Percentage <= 12.86]
                                                                            [Debt-To-Income Ratio Percentage <= 10.37]
                                                                              [Interest Rate Percentage <= 12.53]
                                                                                [0]
                                                                                [Interest Rate Percentage <= 12.69]
                                                                                  [Loan Title == Excellent Credit History]
                                                                                    [0]
                                                                                    [1]
                                                                                  [Amount Requested <= 17000]
                                                                                    [0]
                                                                                    [1]
                                                                              [Amount Requested <= 10000]
                                                                                [1]
                                                                                [Amount Requested <= 12875]
                                                                                  [Loan Title == Credit Card]
                                                                                    [1]
                                                                                    [0]
                                                                                  [1]
                                                                            [FICO_range_lower <= 710]
                                                                              [Monthly PAYMENT <= 168.62]
                                                                                [Monthly PAYMENT <= 135.21]
                                                                                  [Interest Rate Percentage <= 13.16]
                                                                                    [0]
                                                                                    [1]
                                                                                  [0]
                                                                                [Monthly PAYMENT <= 253.58]
                                                                                  [Amount Requested <= 6000]
                                                                                    [Amount Requested <= 5250]
                                                                                      [Interest Rate Percentage <= 14.26]
                                                                                        [Loan Title == Personal Loan]
                                                                                          [0]
                                                                                          [1]
                                                                                        [0]
                                                                                      [0]
                                                                                    [1]
                                                                                  [Debt-To-Income Ratio Percentage <= 6.78]
                                                                                    [1]
                                                                                    [Loan Purpose == debt_consolidation]
                                                                                      [Amount Requested <= 10000]
                                                                                        [Interest Rate Percentage <= 12.99]
                                                                                          [1]
                                                                                          [0]
                                                                                        [Debt-To-Income Ratio Percentage <= 14.58]
                                                                                          [Monthly PAYMENT <= 732.9]
                                                                                            [Debt-To-Income Ratio Percentage <= 14.14]
                                                                                              [Monthly PAYMENT <= 682.08]
                                                                                                [Debt-To-Income Ratio Percentage <= 10.44]
                                                                                                  [Amount Requested <= 12000]
                                                                                                    [0]
                                                                                                    [1]
                                                                                                  [Amount Requested <= 12000]
                                                                                                    [1]
                                                                                                    [0]
                                                                                                [0]
                                                                                              [1]
                                                                                            [1]
                                                                                          [0]
                                                                                      [Debt-To-Income Ratio Percentage <= 14.21]
                                                                                        [Interest Rate Percentage <= 13.48]
                                                                                          [0]
                                                                                          [Monthly PAYMENT <= 682.74]
                                                                                            [Loan Title == New Roof]
                                                                                              [0]
                                                                                              [1]
                                                                                            [0]
                                                                                        [1]
                                                                              [0]
                                                                        [Interest Rate Percentage <= 13.12]
                                                                          [Loan Purpose == other]
                                                                            [0]
                                                                            [Amount Requested <= 11500]
                                                                              [Loan Title == Privacy Needed]
                                                                                [0]
                                                                                [1]
                                                                              [0]
                                                                          [FICO_range_lower <= 665]
                                                                            [0]
                                                                            [FICO_range_lower <= 685]
                                                                              [1]
                                                                              [Interest Rate Percentage <= 13.67]
                                                                                [1]
                                                                                [Amount Requested <= 5000]
                                                                                  [1]
                                                                                  [0]
                                                                      [0]
                                                                  [1]
                                                                [0]
                                                          [Amount Requested <= 4000]
                                                            [Amount Requested <= 1500]
                                                              [0]
                                                              [1]
                                                            [Loan Title == Credit card Consolidation]
                                                              [1]
                                                              [0]
                                                        [Amount Requested <= 2000]
                                                          [1]
                                                          [Interest Rate Percentage <= 15.37]
                                                            [Interest Rate Percentage <= 15.31]
                                                              [Interest Rate Percentage <= 14.84]
                                                                [Loan Purpose == debt_consolidation]
                                                                  [FICO_range_lower <= 675]
                                                                    [Interest Rate Percentage <= 14.74]
                                                                      [Debt-To-Income Ratio Percentage <= 15.89]
                                                                        [Debt-To-Income Ratio Percentage <= 11.1]
                                                                          [Amount Requested <= 2100]
                                                                            [0]
                                                                            [1]
                                                                          [0]
                                                                        [1]
                                                                      [1]
                                                                    [1]
                                                                  [Loan Purpose == other]
                                                                    [1]
                                                                    [Loan Title == Deck]
                                                                      [1]
                                                                      [Loan Title == Refinance credit card down from 29.99]
                                                                        [1]
                                                                        [0]
                                                                [Interest Rate Percentage <= 15.28]
                                                                  [Interest Rate Percentage <= 15.23]
                                                                    [FICO_range_lower <= 690]
                                                                      [Interest Rate Percentage <= 14.96]
                                                                        [0]
                                                                        [Amount Requested <= 5000]
                                                                          [1]
                                                                          [Amount Requested <= 11600]
                                                                            [0]
                                                                            [1]
                                                                      [Amount Requested <= 24250]
                                                                        [1]
                                                                        [0]
                                                                    [0]
                                                                  [FICO_range_lower <= 670]
                                                                    [0]
                                                                    [1]
                                                              [1]
                                                            [Loan Purpose == credit_card]
                                                              [1]
                                                              [Interest Rate Percentage <= 15.7]
                                                                [Loan Title == Wedding]
                                                                  [1]
                                                                  [Loan Title == PAY OFF]
                                                                    [1]
                                                                    [Loan Title == New Kitchen]
                                                                      [1]
                                                                      [0]
                                                                [1]
                    [1]
                  [Debt-To-Income Ratio Percentage <= 18.86]
                    [Loan Title == Personal]
                      [1]
                      [0]
                    [Interest Rate Percentage <= 15.37]
                      [Monthly PAYMENT <= 529.22]
                        [Interest Rate Percentage <= 13.61]
                          [Monthly PAYMENT <= 41.22]
                            [1]
                            [Debt-To-Income Ratio Percentage <= 27.46]
                              [FICO_range_lower <= 675]
                                [Interest Rate Percentage <= 13.43]
                                  [Loan Title == Debt Consolidation Loan]
                                    [1]
                                    [0]
                                  [1]
                                [Loan Title == Personal Loan]
                                  [0]
                                  [Interest Rate Percentage <= 13.22]
                                    [Debt-To-Income Ratio Percentage <= 22.43]
                                      [Debt-To-Income Ratio Percentage <= 21.89]
                                        [Debt-To-Income Ratio Percentage <= 21.53]
                                          [Debt-To-Income Ratio Percentage <= 20.37]
                                            [Debt-To-Income Ratio Percentage <= 20.12]
                                              [Interest Rate Percentage <= 12.12]
                                                [Interest Rate Percentage <= 11.58]
                                                  [Amount Requested <= 2150]
                                                    [0]
                                                    [1]
                                                  [Amount Requested <= 2500]
                                                    [1]
                                                    [Loan Title == Debt Consolidation]
                                                      [1]
                                                      [0]
                                                [Amount Requested <= 10000]
                                                  [1]
                                                  [Debt-To-Income Ratio Percentage <= 18.89]
                                                    [1]
                                                    [0]
                                              [0]
                                            [Monthly PAYMENT <= 326.21]
                                              [Amount Requested <= 4000]
                                                [0]
                                                [1]
                                              [Debt-To-Income Ratio Percentage <= 21.0]
                                                [1]
                                                [0]
                                          [0]
                                        [Loan Title == Home Improvement]
                                          [0]
                                          [1]
                                      [Amount Requested <= 9500]
                                        [Amount Requested <= 8325]
                                          [Monthly PAYMENT <= 265.18]
                                            [Debt-To-Income Ratio Percentage <= 22.83]
                                              [0]
                                              [Loan Purpose == debt_consolidation]
                                                [1]
                                                [Interest Rate Percentage <= 11.86]
                                                  [Loan Title == Personal]
                                                    [0]
                                                    [1]
                                                  [0]
                                            [0]
                                          [1]
                                        [Loan Title == Pay Off High Interest Debt]
                                          [1]
                                          [0]
                                    [1]
                              [1]
                          [Debt-To-Income Ratio Percentage <= 19.67]
                            [1]
                            [Amount Requested <= 12500]
                              [Amount Requested <= 11450]
                                [Debt-To-Income Ratio Percentage <= 19.85]
                                  [1]
                                  [FICO_range_lower <= 675]
                                    [Amount Requested <= 3750]
                                      [1]
                                      [Debt-To-Income Ratio Percentage <= 23.45]
                                        [0]
                                        [Interest Rate Percentage <= 14.59]
                                          [0]
                                          [Interest Rate Percentage <= 15.21]
                                            [1]
                                            [0]
                                    [0]
                                [1]
                              [0]
                        [Interest Rate Percentage <= 10.99]
                          [0]
                          [Interest Rate Percentage <= 14.91]
                            [Debt-To-Income Ratio Percentage <= 19.44]
                              [Amount Requested <= 23000]
                                [Interest Rate Percentage <= 12.53]
                                  [1]
                                  [0]
                                [1]
                              [Loan Title == Consolidation]
                                [0]
                                [Loan Title == No More Credit Cards!!!]
                                  [0]
                                  [Loan Title == Brian's Debt Consolidation]
                                    [0]
                                    [Loan Title == Wedding Exp.]
                                      [0]
                                      [1]
                            [0]
                      [1]
              [FICO_range_lower <= 760]
                [Loan Purpose == home_improvement]
                  [0]
                  [Debt-To-Income Ratio Percentage <= 20.62]
                    [Interest Rate Percentage <= 15.23]
                      [Monthly PAYMENT <= 416.97]
                        [Debt-To-Income Ratio Percentage <= 18.53]
                          [Loan Purpose == medical]
                            [1]
                            [Debt-To-Income Ratio Percentage <= 18.43]
                              [Interest Rate Percentage <= 13.43]
                                [Interest Rate Percentage <= 13.06]
                                  [Debt-To-Income Ratio Percentage <= 8.2]
                                    [0]
                                    [Debt-To-Income Ratio Percentage <= 10.5]
                                      [FICO_range_lower <= 720]
                                        [1]
                                        [Interest Rate Percentage <= 12.61]
                                          [0]
                                          [1]
                                      [Loan Title == Debt Consolidation]
                                        [Amount Requested <= 8000]
                                          [0]
                                          [1]
                                        [0]
                                  [FICO_range_lower <= 695]
                                    [0]
                                    [1]
                                [FICO_range_lower <= 695]
                                  [Amount Requested <= 3600]
                                    [1]
                                    [Loan Title == deb consolidation]
                                      [1]
                                      [Loan Title == Anna's Loan]
                                        [1]
                                        [0]
                                  [0]
                              [1]
                          [0]
                        [FICO_range_lower <= 720]
                          [Loan Title == Debt Consolidation Loan]
                            [1]
                            [0]
                          [Interest Rate Percentage <= 13.99]
                            [Loan Purpose == credit_card]
                              [1]
                              [Monthly PAYMENT <= 439.76]
                                [1]
                                [Debt-To-Income Ratio Percentage <= 14.37]
                                  [0]
                                  [Amount Requested <= 20375]
                                    [Loan Title == Credit Card Consolidation]
                                      [1]
                                      [0]
                                    [1]
                            [1]
                      [Amount Requested <= 18000]
                        [Loan Purpose == credit_card]
                          [0]
                          [Loan Title == Other]
                            [0]
                            [1]
                        [0]
                    [Loan Title == Debt Consolidation]
                      [1]
                      [Debt-To-Income Ratio Percentage <= 22.69]
                        [Amount Requested <= 5500]
                          [0]
                          [Loan Title == Angela Debt Consolidation]
                            [0]
                            [1]
                        [Debt-To-Income Ratio Percentage <= 23.61]
                          [Loan Title ==  consolidation ]
                            [1]
                            [0]
                          [Interest Rate Percentage <= 13.61]
                            [Interest Rate Percentage <= 12.69]
                              [Debt-To-Income Ratio Percentage <= 25.79]
                                [1]
                                [Loan Title == Credit Card Consolidation]
                                  [1]
                                  [0]
                              [0]
                            [1]
                [Interest Rate Percentage <= 12.98]
                  [Amount Requested <= 18000]
                    [Interest Rate Percentage <= 11.12]
                      [0]
                      [Interest Rate Percentage <= 11.49]
                        [1]
                        [0]
                    [Debt-To-Income Ratio Percentage <= 11.99]
                      [1]
                      [Amount Requested <= 20000]
                        [1]
                        [0]
                  [Loan Title == Lending Tree Personal Loan - New Street]
                    [1]
                    [0]
            [1]
        [Loan Purpose == credit_card]
          [Debt-To-Income Ratio Percentage <= 24.64]
            [Interest Rate Percentage <= 18.99]
              [Interest Rate Percentage <= 17.19]
                [Interest Rate Percentage <= 16.32]
                  [Monthly PAYMENT <= 389.26]
                    [Loan Title == Credit Card Loan]
                      [0]
                      [1]
                    [Interest Rate Percentage <= 16.02]
                      [0]
                      [Amount Requested <= 11725]
                        [0]
                        [1]
                  [Loan Title == I can be 18  to debt free please]
                    [1]
                    [0]
                [Loan Title == credit card refi]
                  [0]
                  [Amount Requested <= 13000]
                    [Amount Requested <= 8000]
                      [1]
                      [0]
                    [1]
              [Interest Rate Percentage <= 20.99]
                [0]
                [Amount Requested <= 20000]
                  [0]
                  [1]
            [0]
          [Loan Title == Medical]
            [1]
            [Amount Requested <= 17475]
              [Interest Rate Percentage <= 20.5]
                [Debt-To-Income Ratio Percentage <= 21.93]
                  [Amount Requested <= 16300]
                    [Monthly PAYMENT <= 405.26]
                      [Loan Purpose == home_improvement]
                        [0]
                        [FICO_range_lower <= 725]
                          [Interest Rate Percentage <= 18.55]
                            [FICO_range_lower <= 700]
                              [Debt-To-Income Ratio Percentage <= 17.13]
                                [Debt-To-Income Ratio Percentage <= 15.0]
                                  [Monthly PAYMENT <= 351.53]
                                    [Monthly PAYMENT <= 73.68]
                                      [0]
                                      [Monthly PAYMENT <= 97.96]
                                        [1]
                                        [Monthly PAYMENT <= 348.93]
                                          [Amount Requested <= 8000]
                                            [Loan Purpose == debt_consolidation]
                                              [Debt-To-Income Ratio Percentage <= 12.87]
                                                [Debt-To-Income Ratio Percentage <= 6.85]
                                                  [Interest Rate Percentage <= 17.99]
                                                    [Amount Requested <= 4200]
                                                      [Debt-To-Income Ratio Percentage <= 2.37]
                                                        [1]
                                                        [0]
                                                      [0]
                                                    [1]
                                                  [Interest Rate Percentage <= 16.82]
                                                    [1]
                                                    [Interest Rate Percentage <= 18.21]
                                                      [0]
                                                      [1]
                                                [0]
                                              [Amount Requested <= 7000]
                                                [Loan Title == Consolidation]
                                                  [1]
                                                  [0]
                                                [1]
                                            [Loan Title == Car Loan]
                                              [1]
                                              [0]
                                          [1]
                                    [0]
                                  [Monthly PAYMENT <= 302.44]
                                    [Amount Requested <= 3200]
                                      [0]
                                      [1]
                                    [Loan Title == Pay off Chase Credit Card]
                                      [1]
                                      [0]
                                [Debt-To-Income Ratio Percentage <= 20.51]
                                  [Interest Rate Percentage <= 15.81]
                                    [1]
                                    [Loan Title == Debt Consolidation]
                                      [1]
                                      [0]
                                  [Monthly PAYMENT <= 201.45]
                                    [0]
                                    [Interest Rate Percentage <= 16.07]
                                      [Amount Requested <= 7500]
                                        [1]
                                        [0]
                                      [1]
                              [Loan Title == Unsecured loan]
                                [1]
                                [0]
                            [Loan Title == Debt Consolidation]
                              [Amount Requested <= 8000]
                                [1]
                                [0]
                              [0]
                          [1]
                      [Debt-To-Income Ratio Percentage <= 19.13]
                        [Monthly PAYMENT <= 526.99]
                          [Debt-To-Income Ratio Percentage <= 12.31]
                            [Loan Title == Investment Loan]
                              [0]
                              [1]
                            [Interest Rate Percentage <= 16.89]
                              [1]
                              [0]
                          [Loan Title == mmlloan]
                            [1]
                            [0]
                        [1]
                    [0]
                  [Loan Title == My loan]
                    [1]
                    [Loan Title == Debt Consolidation]
                      [Monthly PAYMENT <= 361.85]
                        [0]
                        [1]
                      [0]
                [0]
              [Monthly PAYMENT <= 790.49]
                [Debt-To-Income Ratio Percentage <= 8.38]
                  [Interest Rate Percentage <= 20.5]
                    [FICO_range_lower <= 725]
                      [Amount Requested <= 18000]
                        [0]
                        [Loan Title == faith]
                          [0]
                          [1]
                      [Amount Requested <= 20000]
                        [1]
                        [0]
                    [0]
                  [Monthly PAYMENT <= 437.92]
                    [Loan Length in Months <= 36]
                      [0]
                      [1]
                    [Monthly PAYMENT <= 671.47]
                      [FICO_range_lower <= 685]
                        [Amount Requested <= 20000]
                          [Interest Rate Percentage <= 18.91]
                            [0]
                            [FICO_range_lower <= 680]
                              [Loan Title == My 2011 Debt Consolidation]
                                [0]
                                [Debt-To-Income Ratio Percentage <= 8.67]
                                  [0]
                                  [1]
                              [0]
                          [0]
                        [Interest Rate Percentage <= 16.49]
                          [0]
                          [Monthly PAYMENT <= 493.73]
                            [1]
                            [Total Amount Funded <= 22250]
                              [FICO_range_lower <= 695]
                                [Amount Requested <= 18500]
                                  [0]
                                  [1]
                                [0]
                              [Loan Title == Debt Consolidation]
                                [0]
                                [1]
                      [Debt-To-Income Ratio Percentage <= 10.85]
                        [0]
                        [Loan Purpose == small_business]
                          [Loan Title == Launching apparel brand w/Patent]
                            [1]
                            [0]
                          [FICO_range_lower <= 675]
                            [Monthly PAYMENT <= 675.23]
                              [1]
                              [Amount Requested <= 19750]
                                [0]
                                [Amount Requested <= 30000]
                                  [Loan Title == Debt Consolidation Loan]
                                    [0]
                                    [Loan Title == Remodelling and Consolidation Loan]
                                      [0]
                                      [1]
                                  [0]
                            [1]
                [Monthly PAYMENT <= 931.09]
                  [Debt-To-Income Ratio Percentage <= 16.94]
                    [0]
                    [Loan Title == 2012loan]
                      [1]
                      [Loan Title == dimples]
                        [1]
                        [Loan Title == Debt Consolidation]
                          [Amount Requested <= 30000]
                            [0]
                            [1]
                          [0]
                  [FICO_range_lower <= 695]
                    [Interest Rate Percentage <= 22.45]
                      [Interest Rate Percentage <= 19.72]
                        [Amount Requested <= 30000]
                          [1]
                          [0]
                        [0]
                      [1]
                    [Amount Requested <= 32000]
                      [0]
                      [1]



```python
print("Pruned Information Gain tree:")
print_tree(pruned_tree_by_error.root)
```

    Pruned Information Gain tree:
    [Interest Rate Percentage <= 10.74]
      [Debt-To-Income Ratio Percentage <= 10.97]
        [FICO_range_lower <= 760]
          [Debt-To-Income Ratio Percentage <= 10.54]
            [Loan Title == Debt consolidation]
              [0]
              [Amount Requested <= 20000]
                [Loan Title == personal loan]
                  [0]
                  [Monthly PAYMENT <= 324.07]
                    [Monthly PAYMENT <= 292.01]
                      [Interest Rate Percentage <= 10.62]
                        [FICO_range_lower <= 685]
                          [1]
                          [Monthly PAYMENT <= 286.4]
                            [FICO_range_lower <= 730]
                              [Monthly PAYMENT <= 195.27]
                                [Loan Purpose == other]
                                  [0]
                                  [1]
                                [Monthly PAYMENT <= 248.37]
                                  [0]
                                  [1]
                              [1]
                            [0]
                        [1]
                      [1]
                    [Amount Requested <= 11000]
                      [0]
                      [Debt-To-Income Ratio Percentage <= 9.13]
                        [Debt-To-Income Ratio Percentage <= 6.21]
                          [1]
                          [Interest Rate Percentage <= 9.88]
                            [Debt-To-Income Ratio Percentage <= 8.35]
                              [0]
                              [1]
                            [0]
                        [1]
                [1]
            [1]
          [1]
        [Loan Purpose == major_purchase]
          [1]
          [Monthly PAYMENT <= 80.88]
            [Monthly PAYMENT <= 58.26]
              [1]
              [Amount Requested <= 2400]
                [Amount Requested <= 2050]
                  [0]
                  [Interest Rate Percentage <= 9.63]
                    [1]
                    [0]
                [0]
            [Debt-To-Income Ratio Percentage <= 12.34]
              [Debt-To-Income Ratio Percentage <= 12.24]
                [FICO_range_lower <= 770]
                  [0]
                  [1]
                [0]
              [Debt-To-Income Ratio Percentage <= 12.74]
                [1]
                [Loan Title == Debt Consolidation Loan]
                  [0]
                  [Loan Purpose == house]
                    [1]
                    [Monthly PAYMENT <= 93.31]
                      [1]
                      [Loan Purpose == credit_card]
                        [1]
                        [Amount Requested <= 23000]
                          [Amount Requested <= 17000]
                            [Debt-To-Income Ratio Percentage <= 14.5]
                              [FICO_range_lower <= 705]
                                [1]
                                [FICO_range_lower <= 715]
                                  [0]
                                  [Total Amount Funded <= 6600]
                                    [1]
                                    [Debt-To-Income Ratio Percentage <= 13.99]
                                      [Interest Rate Percentage <= 9.88]
                                        [1]
                                        [0]
                                      [1]
                              [Amount Requested <= 15600]
                                [Interest Rate Percentage <= 10.71]
                                  [Interest Rate Percentage <= 9.88]
                                    [Interest Rate Percentage <= 5.99]
                                      [0]
                                      [Debt-To-Income Ratio Percentage <= 28.39]
                                        [Interest Rate Percentage <= 6.03]
                                          [1]
                                          [FICO_range_lower <= 705]
                                            [0]
                                            [Interest Rate Percentage <= 6.62]
                                              [0]
                                              [Interest Rate Percentage <= 6.99]
                                                [1]
                                                [Monthly PAYMENT <= 371.3]
                                                  [Amount Requested <= 6950]
                                                    [Monthly PAYMENT <= 187.08]
                                                      [Debt-To-Income Ratio Percentage <= 16.73]
                                                        [Interest Rate Percentage <= 7.88]
                                                          [0]
                                                          [1]
                                                        [Monthly PAYMENT <= 134.55]
                                                          [Amount Requested <= 4000]
                                                            [Debt-To-Income Ratio Percentage <= 20.33]
                                                              [0]
                                                              [1]
                                                            [0]
                                                          [1]
                                                      [1]
                                                    [Amount Requested <= 11000]
                                                      [Monthly PAYMENT <= 168.49]
                                                        [0]
                                                        [Loan Purpose == debt_consolidation]
                                                          [Amount Requested <= 10000]
                                                            [Monthly PAYMENT <= 311.8]
                                                              [Monthly PAYMENT <= 247.53]
                                                                [0]
                                                                [1]
                                                              [0]
                                                            [1]
                                                          [0]
                                                      [0]
                                                  [1]
                                        [0]
                                    [Interest Rate Percentage <= 9.91]
                                      [0]
                                      [Loan Title == consolidation]
                                        [1]
                                        [Loan Title == Debt Consolidation]
                                          [1]
                                          [Debt-To-Income Ratio Percentage <= 19.13]
                                            [0]
                                            [Interest Rate Percentage <= 9.99]
                                              [0]
                                              [Amount Requested <= 8000]
                                                [1]
                                                [0]
                                  [1]
                                [1]
                            [1]
                          [0]
      [Interest Rate Percentage <= 15.8]
        [Loan Purpose == small_business]
          [Monthly PAYMENT <= 102.42]
            [1]
            [0]
          [FICO_range_lower <= 800]
            [Loan Length in Months <= 36]
              [FICO_range_lower <= 660]
                [0]
                [Debt-To-Income Ratio Percentage <= 18.48]
                  [Debt-To-Income Ratio Percentage <= 18.39]
                    [Loan Title == personal]
                      [0]
                      [Debt-To-Income Ratio Percentage <= 0.56]
                        [1]
                        [Debt-To-Income Ratio Percentage <= 1.53]
                          [0]
                          [Loan Title == Personal loan]
                            [1]
                            [Interest Rate Percentage <= 10.95]
                              [0]
                              [Interest Rate Percentage <= 12.18]
                                [Debt-To-Income Ratio Percentage <= 14.4]
                                  [Loan Title == Personal Loan]
                                    [0]
                                    [Debt-To-Income Ratio Percentage <= 14.17]
                                      [1]
                                      [0]
                                  [1]
                                [Interest Rate Percentage <= 12.42]
                                  [FICO_range_lower <= 695]
                                    [0]
                                    [Amount Requested <= 4800]
                                      [1]
                                      [0]
                                  [Loan Purpose == car]
                                    [1]
                                    [Loan Purpose == major_purchase]
                                      [Debt-To-Income Ratio Percentage <= 4.49]
                                        [0]
                                        [1]
                                      [Loan Title == Home Improvements]
                                        [0]
                                        [Loan Title == debt loan]
                                          [0]
                                          [Debt-To-Income Ratio Percentage <= 2.7]
                                            [1]
                                            [Loan Title == Debts]
                                              [1]
                                              [Loan Purpose == vacation]
                                                [0]
                                                [Loan Title == Credit Card Refinance]
                                                  [1]
                                                  [Loan Title == consolidation loan]
                                                    [1]
                                                    [Loan Title == personal loan]
                                                      [1]
                                                      [Interest Rate Percentage <= 14.59]
                                                        [Interest Rate Percentage <= 14.35]
                                                          [Loan Purpose == medical]
                                                            [1]
                                                            [Amount Requested <= 3075]
                                                              [Debt-To-Income Ratio Percentage <= 14.54]
                                                                [1]
                                                                [0]
                                                              [Debt-To-Income Ratio Percentage <= 18.0]
                                                                [Debt-To-Income Ratio Percentage <= 17.86]
                                                                  [Loan Title == Consolidate]
                                                                    [0]
                                                                    [Debt-To-Income Ratio Percentage <= 17.75]
                                                                      [Debt-To-Income Ratio Percentage <= 15.48]
                                                                        [Debt-To-Income Ratio Percentage <= 6.52]
                                                                          [Loan Purpose == home_improvement]
                                                                            [0]
                                                                            [Monthly PAYMENT <= 404.97]
                                                                              [FICO_range_lower <= 710]
                                                                                [FICO_range_lower <= 690]
                                                                                  [FICO_range_lower <= 675]
                                                                                    [1]
                                                                                    [Interest Rate Percentage <= 13.11]
                                                                                      [1]
                                                                                      [0]
                                                                                  [1]
                                                                                [0]
                                                                              [1]
                                                                          [Interest Rate Percentage <= 12.86]
                                                                            [1]
                                                                            [FICO_range_lower <= 710]
                                                                              [Monthly PAYMENT <= 168.62]
                                                                                [0]
                                                                                [Monthly PAYMENT <= 253.58]
                                                                                  [1]
                                                                                  [Debt-To-Income Ratio Percentage <= 6.78]
                                                                                    [1]
                                                                                    [Loan Purpose == debt_consolidation]
                                                                                      [Amount Requested <= 10000]
                                                                                        [0]
                                                                                        [Debt-To-Income Ratio Percentage <= 14.58]
                                                                                          [Monthly PAYMENT <= 732.9]
                                                                                            [Debt-To-Income Ratio Percentage <= 14.14]
                                                                                              [Monthly PAYMENT <= 682.08]
                                                                                                [Debt-To-Income Ratio Percentage <= 10.44]
                                                                                                  [1]
                                                                                                  [Amount Requested <= 12000]
                                                                                                    [1]
                                                                                                    [0]
                                                                                                [0]
                                                                                              [1]
                                                                                            [1]
                                                                                          [0]
                                                                                      [Debt-To-Income Ratio Percentage <= 14.21]
                                                                                        [0]
                                                                                        [1]
                                                                              [0]
                                                                        [1]
                                                                      [0]
                                                                  [1]
                                                                [0]
                                                          [0]
                                                        [Amount Requested <= 2000]
                                                          [1]
                                                          [Interest Rate Percentage <= 15.37]
                                                            [Interest Rate Percentage <= 15.31]
                                                              [Interest Rate Percentage <= 14.84]
                                                                [1]
                                                                [0]
                                                              [1]
                                                            [0]
                    [1]
                  [Debt-To-Income Ratio Percentage <= 18.86]
                    [0]
                    [Interest Rate Percentage <= 15.37]
                      [Monthly PAYMENT <= 529.22]
                        [Interest Rate Percentage <= 13.61]
                          [Monthly PAYMENT <= 41.22]
                            [1]
                            [Debt-To-Income Ratio Percentage <= 27.46]
                              [FICO_range_lower <= 675]
                                [Interest Rate Percentage <= 13.43]
                                  [Loan Title == Debt Consolidation Loan]
                                    [1]
                                    [0]
                                  [1]
                                [Loan Title == Personal Loan]
                                  [0]
                                  [Interest Rate Percentage <= 13.22]
                                    [Debt-To-Income Ratio Percentage <= 22.43]
                                      [Debt-To-Income Ratio Percentage <= 21.89]
                                        [Debt-To-Income Ratio Percentage <= 21.53]
                                          [Debt-To-Income Ratio Percentage <= 20.37]
                                            [0]
                                            [1]
                                          [0]
                                        [1]
                                      [Amount Requested <= 9500]
                                        [Amount Requested <= 8325]
                                          [0]
                                          [1]
                                        [0]
                                    [1]
                              [1]
                          [Debt-To-Income Ratio Percentage <= 19.67]
                            [1]
                            [Amount Requested <= 12500]
                              [Amount Requested <= 11450]
                                [Debt-To-Income Ratio Percentage <= 19.85]
                                  [1]
                                  [FICO_range_lower <= 675]
                                    [Amount Requested <= 3750]
                                      [1]
                                      [0]
                                    [0]
                                [1]
                              [0]
                        [Interest Rate Percentage <= 10.99]
                          [0]
                          [Interest Rate Percentage <= 14.91]
                            [1]
                            [0]
                      [1]
              [FICO_range_lower <= 760]
                [Loan Purpose == home_improvement]
                  [0]
                  [Debt-To-Income Ratio Percentage <= 20.62]
                    [0]
                    [Loan Title == Debt Consolidation]
                      [1]
                      [0]
                [1]
            [1]
        [0]

