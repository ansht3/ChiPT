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